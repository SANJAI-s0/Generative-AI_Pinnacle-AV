import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import re
import os
import shutil
import kagglehub

def download_dataset():
    print("Dataset not found locally. Attempting to download from Kaggle using kagglehub...")
    try:
        # Download to cache
        cache_path = kagglehub.dataset_download("abhi8923shriv/sentiment-analysis-dataset")
        source_csv = os.path.join(cache_path, "training.1600000.processed.noemoticon.csv")
        
        # Ensure local Dataset folder exists
        os.makedirs('Dataset', exist_ok=True)
        target_csv = os.path.join('Dataset', "training.1600000.processed.noemoticon.csv")
        
        # Copy to local Dataset folder
        print(f"Copying {source_csv} to {target_csv}...")
        shutil.copy(source_csv, target_csv)
        print("Dataset successfully stored in 'Dataset/'")
        return target_csv
    except Exception as e:
        print(f"Error downloading or storing dataset: {e}")
        return None

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_lstm_model(vocab_size, max_len):
    model = Sequential([
        Embedding(vocab_size, 128, input_length=max_len),
        Bidirectional(LSTM(64)),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def main():
    dataset_path = 'Dataset/training.1600000.processed.noemoticon.csv'
    if not os.path.exists(dataset_path):
        dataset_path = download_dataset()
        if not dataset_path:
            return

    print("Loading data...")
    cols = ['target', 'ids', 'date', 'flag', 'user', 'text']
    df = pd.read_csv(dataset_path, encoding='latin-1', header=None, names=cols)
    
    # Preprocessing
    df['target'] = df['target'].replace(4, 1)
    df = df.sample(20000, random_state=42) # Sample for demonstration
    df['clean_text'] = df['text'].apply(clean_text)
    
    # Tokenization
    max_words = 10000
    max_len = 100
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(df['clean_text'])
    sequences = tokenizer.texts_to_sequences(df['clean_text'])
    X = pad_sequences(sequences, maxlen=max_len)
    y = df['target'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Building LSTM model...")
    model = build_lstm_model(max_words, max_len)
    
    print("Summary of LSTM model:")
    model.summary()
    
    # In a real scenario, we would call model.fit here.
    # print("Training...")
    # model.fit(X_train, y_train, epochs=3, batch_size=64, validation_split=0.1)

if __name__ == "__main__":
    main()
