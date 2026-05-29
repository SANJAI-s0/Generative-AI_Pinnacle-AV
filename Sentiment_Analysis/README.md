# Sentiment Analysis Using BERT, LSTM, GRU, and RNN

[![GitHub License](https://img.shields.io/github/license/SANJAI-s0/Sentiment_Analysis_Using_BERT-LSTM-GRU-RNN)](https://github.com/SANJAI-s0/Sentiment_Analysis_Using_BERT-LSTM-GRU-RNN/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/SANJAI-s0/Sentiment_Analysis_Using_BERT-LSTM-GRU-RNN)](https://github.com/SANJAI-s0/Sentiment_Analysis_Using_BERT-LSTM-GRU-RNN/stargazers)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)

A comparative analysis of modern and traditional deep learning architectures for sentiment classification on the Sentiment140 dataset.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Dataset Details](#-dataset-details)
- [Automatic Dataset Setup](#-automatic-dataset-setup)
- [Workflow](#-workflow)
- [Models Architectures](#-models-architectures)
- [Installation and Setup](#-installation-and-setup)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [Results & Comparison](#-results--comparison)
- [License](#-license)

---

## 🔍 Project Overview
This project focuses on identifying the sentiment (Positive or Negative) of Twitter messages. We evaluate multiple deep learning models to compare their performance, training time, and accuracy:
1. **BERT (Bidirectional Encoder Representations from Transformers)** - State-of-the-art transformer based approach.
2. **LSTM (Long Short-Term Memory)** - Captures long-term dependencies in text.
3. **GRU (Gated Recurrent Unit)** - A faster alternative to LSTM with similar gating mechanisms.
4. **RNN (Recurrent Neural Network)** - The foundational sequence model.

---

## 📊 Dataset Details
The **Sentiment140** dataset contains 1,600,000 tweets extracted using the Twitter API.
- **Source**: [Kaggle Sentiment140](https://www.kaggle.com/datasets/abhi8923shriv/sentiment-analysis-dataset)
- **Labels**: 
    - `0` -> **Negative**
    - `4` -> **Positive**
- **Features**: Tweet ID, Date, User, and the actual Text.

---

## 📥 Automatic Dataset Setup
Since the dataset is large (~145MB), this repository includes an automated download and organization system:
- **Automatic Retrieval**: Uses `kagglehub` to download the latest version directly from Kaggle.
- **Local Persistence**: The notebook and scripts automatically copy the downloaded CSV to a root-level `Dataset/` folder for easy access and consistency.

---

## ⚙️ Workflow
The project follows a modular pipeline for data processing and model evaluation:

```mermaid
graph TD
    A[Data Acquisition: Sentiment140 Dataset] --> B[Data Cleaning & Mapping]
    B --> B1[Mapping Labels: 0-Neg, 4-Pos]
    B --> B2[Text Preprocessing: Regex, Stopwords]
    
    B1 --> C[Exploratory Data Analysis - EDA]
    C --> D[Data Splitting: Train/Val/Test]
    
    D --> E1[BERT Tokenization]
    D --> E2[Sequence Padding & Tokenization]
    
    E1 --> F1[Model 1: BERT Fine-Tuning]
    E2 --> F2[Model 2: RNN]
    E2 --> F3[Model 3: LSTM]
    E2 --> F4[Model 4: GRU]
    
    F1 --> G[Comparative Evaluation]
    F2 --> G
    F3 --> G
    F4 --> G
    
    G --> H[Final Analysis & Visualization]
```

*(Workflow defined in [Flow/sentiment_flow.mmd](Flow/sentiment_flow.mmd))*

---

## 📂 Project Structure
```text
Sentiment_Analysis_Using_BERT-LSTM-GRU-RNN/
├── Dataset/                   # Dataset folder (auto-created)
├── Flow/
│   └── sentiment_flow.mmd     # Mermaid workflow diagram
├── Sentiment_Analysis_Comparative_Study.ipynb  # Main research notebook
├── train_models.py           # Modular training script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files to ignore (Data, Models, etc.)
├── LICENSE                    # MIT License
└── README.md                  # Project documentation
```

---

## 🚀 Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SANJAI-s0/Sentiment_Analysis_Using_BERT-LSTM-GRU-RNN.git
   cd Sentiment_Analysis_Using_BERT-LSTM-GRU-RNN
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Analysis:**
   - Open the `.ipynb` file in Jupyter or VS Code.
   - Or run the script: `python train_models.py`

---

## 🧠 Models Architectures

### 1. BERT
- Framework: HuggingFace Transformers (PyTorch).
- Pre-trained: `bert-base-uncased`.
- Fine-tuned with a linear classifier layer.

### 2. Recurrent Architectures (RNN, LSTM, GRU)
- Framework: TensorFlow/Keras.
- Hidden Layers: Bidirectional configurations.
- Dropout for regularization to avoid overfitting.

---

## 📈 Results & Comparison
| Model | Accuracy | F1-Score | Training Time |
|-------|----------|----------|---------------|
| BERT  | ~91%     | TBD      | High          |
| LSTM  | ~84%     | TBD      | Medium        |
| GRU   | ~83%     | TBD      | Medium        |
| RNN   | ~76%     | TBD      | Low           |

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact
**Sanjai** - [GitHub Profile](https://github.com/SANJAI-s0)

Project Link: [https://github.com/SANJAI-s0/Sentiment_Analysis_Using_BERT-LSTM-GRU-RNN](https://github.com/SANJAI-s0/Sentiment_Analysis_Using_BERT-LSTM-GRU-RNN)
