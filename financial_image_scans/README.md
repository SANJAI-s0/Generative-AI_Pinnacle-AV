# 📊 AI-Powered Financial Image Scans

<!-- Badges -->
<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/python-%3E%3D3.8-blue?logo=python&logoColor=white" />
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-UI-brightgreen?logo=streamlit&logoColor=white" />
  <img alt="Google Gemini" src="https://img.shields.io/badge/Google%20Gemini-2.5-yellow?logo=google&logoColor=white" />
  <img alt="API Key" src="https://img.shields.io/badge/Requires%20API%20Key-Yes-red" />
  <img alt="License" src="https://img.shields.io/badge/License-See%20LICENSE-lightgrey" />
  <!-- Replace the two placeholders below with your actual GitHub repo badges when you have CI/test set up
  <img alt="Build (placeholder)" src="https://img.shields.io/badge/build-pending-lightgrey" />
  <img alt="Coverage (placeholder)" src="https://img.shields.io/badge/coverage-n/a-lightgrey" />
  -->
</p>

An AI-powered tool that analyzes financial document images (Annual Reports, Balance Sheets, Earnings Reports) to extract key insights, analyze charts/graphs, and generate structured summaries tailored to specific user roles.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Features](#features)
- [Output Guidelines](#output-guidelines)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#step-1-clone-download-project)
- [Usage](#usage)
- [Sample Input](#sample-input)
- [Sample Output](#sample-output)
- [Testing Procedure](#testing-procedure)
- [Configuration](#configuration)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#-troubleshooting)
- [Dependencies](#-dependencies)
- [Security Notes](#-security-notes)
- [License](#-license)
- [Contributing](#-contributing)
- [Support](#-support)
- [Project Alignment](#-project-alignment)

---

## 🎯 Problem Statement
Financial professionals, investors, and decision-makers often struggle to quickly extract relevant insights from lengthy and complex financial documents. These documents are filled with jargon, dense numerical data, and intricate details, making it challenging to identify key takeaways efficiently.

This solution addresses these challenges by:
- ✅ Scanning and capturing relevant financial document images
- ✅ Extracting and highlighting critical information (metrics, trends, risks)
- ✅ Summarizing complex content into concise, actionable insights
- ✅ Analyzing graphs and charts within documents
- ✅ Tailoring outputs for investors, analysts, or auditors

---

## ✨ Features

| Feature               | Description                                                                         |
|-----------------------|-------------------------------------------------------------------------------------|
| Multi-Source Input    | Load images from local filesystem or URLs using PIL library                         |
| Multimodal AI Analysis| Analyzes both text data AND visual charts/graphs using Google Gemini 2.5            |
| Role-Based Insights   | Tailors summaries for Investors, Financial Analysts, Auditors, or General users     |
| Structured Output     | Generates 7 key sections as per industry standards (see Output Guidelines)          |
| Focus Area Selection  | Customize analysis to focus on specific areas (Metrics, Balance Sheet, Risks, etc.) |
| Download Reports      | Export analysis summaries as Markdown files for sharing                             |
| Interactive UI        | Clean Streamlit interface with real-time previews and error handling                |

---

## 📋 Output Guidelines

The tool generates comprehensive reports covering all sections specified in the requirements:

1. Key Financial Metrics – Revenue, Net Income, EPS, Growth Trends, Financial Ratios
2. Income and Expenses – Net Interest Income, Fee Income, Operating Expenses
3. Balance Sheet Highlights – Assets, Liabilities, Equity, Loans, Deposits
4. Credit Quality – Cost of Risk, Non-Performing Loans, Forbearance Ratios
5. Strategic and Operational Updates – Sustainability, Digital Capabilities, Partnerships
6. Market Conditions and Outlook – Macro Factors, Risks, Management Commentary
7. Shareholder Information – Dividends, Stock Performance, Capital Position

---

## 🏗️ Project Structure

```
financial_image_scans/
│
├── .env                      # API keys (GOOGLE_API_KEY)
├── .env.example              # Example environment file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── check_models.py           # Script to verify available Gemini models
├── app.py                    # Main Streamlit application
│
└── src/
    ├── __init__.py           # Package initializer
    ├── image_loader.py       # PIL-based image loading (Local & URL)
    └── financial_analyzer.py # AI analysis logic with Gemini API
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google API Key (Free tier available)

### Step 1: Clone/Download Project
```bash
git clone https://github.com/SANJAI-s0/financial_image_scans.git
```

### Step 2: Navigate to Project Directory
```bash
cd financial_image_scans
```

### Step 3: Create Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure API Key
```bash
# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
# Edit .env and add your API key
# Get your key from: https://aistudio.google.com/app/apikey
```

> Example `.env` file format:
```bash
GOOGLE_API_KEY=your_api_key_here
```

---

## 🎮 Usage

### Step 1: Launch Application
```bash
streamlit run app.py
```

### Step 2: Upload Images
- Local Files: Click "Browse Files" and select financial document images (JPG, PNG)
- URLs: Paste direct image URLs (one per line)

### Step 3: Configure Analysis
- Select Target Audience (Investor, Analyst, Auditor, General)
- Choose Focus Areas (Key Metrics, Balance Sheet, Risks, Charts, etc.)
- Add Custom Instructions (optional)

### Step 4: Generate Report
- Click "🔍 Scan & Analyze Documents"
- Review the structured summary
- Download report using "📥 Download Summary" button

---

## 📸 Sample Input

### Supported Document Types
- Annual Reports
- Balance Sheets
- Income Statements
- Cash Flow Statements
- Earnings Reports
- Financial Charts & Graphs

### Example Image Sources
- Screenshots from company investor relations pages
- PDF exports converted to images
- Public financial report URLs

## 📄 Sample Output

```markdown
### Financial Summary Report - ABN AMRO Bank (Q3 2024)

**Key Financial Metrics**
- Net Profit: EUR 690 million (down from EUR 759 million in Q3 2023)
- Earnings Per Share (EPS): EUR 0.78
- Return on Equity: 11.6%
- Cost/Income Ratio: 59.2%
- CET1 Ratio (Basel III): 14.1%

**Income and Expenses**
- Net Interest Income: EUR 1,638 million (↑ 7% YoY)
- Fee and Commission Income: EUR 478 million (↑ 8% YoY)
- Operating Expenses: EUR 1,334 million (↑ 9% YoY)

**Balance Sheet Highlights**
- Total Assets: EUR 403.8 billion
- Loans to Customers: EUR 259.6 billion
- Client Deposits: EUR 224.5 billion

**Credit Quality**
- Cost of Risk: -2 basis points
- Forbearance Ratio: 2.0%
- Non-Performing Loans: 1.9%

**Strategic Updates**
- EUR 1 billion investment in climate-focused projects
- Enhanced fraud prevention tools in mobile app
- "Best Benelux Broker" award (3rd consecutive year)

**Market Conditions**
- Dutch housing market: +4% from Q2 2024, +11% YoY
- Low unemployment and declining inflation
- Regulatory caution (Basel IV implementation)

**Shareholder Info**
- Strong capital position maintained
- Dividend policy aligned with profitability
```

---

## 🧪 Testing Procedure

### Test 1: Verify Model Access

```bash
python check_models.py
```

> Expected output: List of available Gemini models (should include `gemini-2.5-flash`)

### Test 2: Local Image Upload
Launch app: `streamlit run app.py`
Select "Local Files"
Upload a financial report image
Verify thumbnail preview appears

### Test 3: URL Image Input
Select "URLs" option
Paste a direct image link
Verify image loads successfully

### Test 4: AI Analysis
Upload a clear financial table or chart image
Select audience: "Financial Analyst"
Click "Scan & Analyze Documents"
Verify all 7 output sections are generated

### Test 5: Download Report
After analysis completes
Click "Download Summary"
Verify `.md` file downloads correctly

---

## ⚙️ Configuration

### Available Gemini Models

Based on API key access, you can use:
- `gemini-2.5-flash` ✅ (Recommended - Fast & Cost-effective)
- `gemini-2.5-pro` ✅ (More powerful for complex analysis)
- `gemini-pro-latest` ✅ (Stable alternative)

To change the model, edit `src/financial_analyzer.py` line 52:

```bash
model = genai.GenerativeModel('gemini-2.5-flash')
```

### Environment Variables

```
| Variable         | Description              | Required |
|------------------|--------------------------|----------|
| `GOOGLE_API_KEY` | Google Gemini API Key    | Yes      |
```

---

## 🐛 Troubleshooting

```
| Issue                    | Solution                                                                      |
|--------------------------|-------------------------------------------------------------------------------|
| 404 Model Not Found      | Run `python check_models.py` and update model name in `financial_analyzer.py` |
| API Key Invalid          | Regenerate key at https://aistudio.google.com/app/apikey                      |
| Image Not Loading        | Ensure URL ends in `.jpg`/`.png` or check local file path                     |
| Analysis Timeout         | Reduce image size (<4MB) or use clearer crop of financial data                |
| Missing Output Sections  | Check image clarity; AI may not read blurry text                              |
| Rate Limit Exceeded      | Wait 60 seconds between requests or upgrade API tier                          |
| PIL Import Error         | Run `pip install Pillow`                                                      |
| Streamlit Port Conflict  | Run `streamlit run app.py --server.port 8502`                                 |
```

---

## 📦 Dependencies

```
| Package               | Version | Purpose                         |
|-----------------------|---------|---------------------------------|
| `streamlit`           | Latest  | Web UI Framework                |
| `Pillow`              | Latest  | Image Processing (PIL)          |
| `requests`            | Latest  | URL Image Fetchin               |
| `google-generativeai` | Latest  | Google Gemini AI API            |
| `python-dotenv`       | Latest  | Environment Variable Management |
```

---

## 🔒 Security Notes
- API Keys: Never commit `.env` file to version control
- Image Data: Images are processed in-memory and not stored permanently
- Rate Limits: Free tier has usage limits; monitor API dashboard
- Production: Use environment variables, not hardcoded keys

---

## 📝 License
This project is created for educational purposes. Please comply with:
- Google Gemini API Terms of Service
- Data privacy regulations for financial information
- Copyright restrictions on uploaded documents

---

## 🤝 Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/Enhancement`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/Enhancement`)
5. Open Pull Request

---

## 📞 Support
For issues or questions:
1. Check the Troubleshooting section above
2. Review Google Gemini API documentation: https://ai.google.dev/
3. Check Streamlit documentation: https://docs.streamlit.io/

---

## 🎓 Project Alignment

This project fulfills all requirements from the Financial Report Analysis Problem Statement:

```
| Requirement                                | Status          |
|--------------------------------------------|-==--------------|
| Scan and capture financial document images | ✅ Implemented |
| Extract key metrics, trends, and risks     | ✅ Implemented |
| Summarize for specific user roles          | ✅ Implemented |
| Analyze graphs and charts                  | ✅ Implemented |
| Support local and URL image inputs         | ✅ Implemented |
| Use PIL library to store images in list    | ✅ Implemented |
| Follow output guidelines (7 sections)      | ✅ Implemented |
| Provide actionable insights                | ✅ Implemented |
```

---

<Built with ❤️ using Google Gemini AI>
