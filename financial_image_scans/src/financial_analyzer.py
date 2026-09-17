import os
import google.generativeai as genai
from PIL import Image
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

# Configure API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("Warning: GOOGLE_API_KEY not found in .env")

# Define the system prompt based on PDF Output Guidelines
SYSTEM_PROMPT = """
You are an expert Financial Analyst AI. Your task is to analyze financial document images 
(Annual Reports, Balance Sheets, Earnings Reports) and provide a structured summary.

You must analyze text data AND any graphs/charts present in the images.

Follow these Output Guidelines strictly for your summary:
1. **Key Financial Metrics**: Highlight revenue, net income, EPS, growth trends vs previous periods.
2. **Income and Expenses**: Summarize Net Interest Income, Fee Income, Operating Expenses, etc.
3. **Balance Sheet Highlights**: Assets, Liabilities, Equity, Loans, Deposits.
4. **Credit Quality**: Cost of risk, Non-performing loans, forbearance ratios.
5. **Strategic and Operational Updates**: Sustainability, digital capabilities, awards, partnerships.
6. **Market Conditions and Outlook**: Macro factors, risks, challenges, management outlook.
7. **Shareholder Info**: Dividends or stock performance if applicable.

Tailor the insights to be concise and actionable for investors, analysts, or auditors.
If specific data is missing, state that it was not visible in the provided images.
"""

def analyze_financial_documents(images: List[Image.Image], user_prompt: Optional[str] = None) -> str:
    """
    Sends PIL images to the Multimodal LLM for financial analysis.
    """
    if not GOOGLE_API_KEY:
        return "Error: API Key not configured. Please set GOOGLE_API_KEY in your .env file."

    try:
        # UPDATED: Using gemini-2.5-flash (confirmed available for your API key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Construct the full prompt
        full_prompt = SYSTEM_PROMPT
        if user_prompt:
            full_prompt += f"\n\nUser Specific Request: {user_prompt}"
        else:
            full_prompt += "\n\nUser Specific Request: Please provide a comprehensive summary based on the standard output guidelines."

        # Generate Content using images and text
        response = model.generate_content([full_prompt] + images)
        
        return response.text

    except Exception as e:
        return f"Error during analysis: {str(e)}"
