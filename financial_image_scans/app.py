import streamlit as st
from src.image_loader import load_images_to_list_sources
from src.financial_analyzer import analyze_financial_documents
from PIL import Image
import os

# Page Config
st.set_page_config(
    page_title="Financial Image Scans",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 AI-Powered Financial Image Scans")
st.markdown("""
Upload financial document images (Annual Reports, Balance Sheets, Earnings Reports) 
to extract key insights, analyze charts, and generate structured summaries.

**Output Includes:** Key Financial Metrics, Income & Expenses, Balance Sheet, 
Credit Quality, Strategic Updates, Market Conditions & Shareholder Info.
""")

# Sidebar for API Key if not set in env
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Google API Key", type="password", help="Get your API key from https://aistudio.google.com/app/apikey")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.success("✅ API Key Set")
    
    st.markdown("---")
    st.info("📌 **Supported Inputs:**\n- Local Images (JPG, PNG)\n- Image URLs")
    
    st.markdown("---")
    st.markdown("### 📋 Output Guidelines")
    st.markdown("""
    The analysis will include:
    - Key Financial Metrics
    - Income and Expenses
    - Balance Sheet Highlights
    - Credit Quality
    - Strategic Updates
    - Market Conditions
    - Shareholder Info
    """)

# Main Input Area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. 📤 Upload Images")
    upload_method = st.radio("Select Input Method", ["Local Files", "URLs"], horizontal=True)
    
    uploaded_images = []

    if upload_method == "Local Files":
        uploaded_files = st.file_uploader(
            "Choose financial document images", 
            type=['jpg', 'jpeg', 'png'], 
            accept_multiple_files=True,
            help="Upload images of balance sheets, income statements, earnings reports, etc."
        )
        if uploaded_files:
            for file in uploaded_files:
                img = Image.open(file)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                uploaded_images.append(img)
            st.success(f"✅ {len(uploaded_images)} image(s) loaded via PIL.")

    elif upload_method == "URLs":
        url_input = st.text_area(
            "Enter Image URLs (one per line)", 
            placeholder="https://example.com/financial-report.jpg",
            height=100
        )
        if url_input:
            urls = [line.strip() for line in url_input.split('\n') if line.strip()]
            source_dicts = [{'type': 'url', 'value': url} for url in urls]
            try:
                uploaded_images = load_images_to_list_sources(source_dicts)
                st.success(f"✅ {len(uploaded_images)} image(s) loaded from URLs via PIL.")
            except Exception as e:
                st.error(f"❌ Error loading URLs: {e}")

    # Display Thumbnails
    if uploaded_images:
        st.subheader("🖼️ Loaded Images Preview")
        cols = st.columns(min(len(uploaded_images), 3))  # Max 3 columns for better layout
        for idx, img in enumerate(uploaded_images):
            with cols[idx % 3]:
                st.image(img, caption=f"Image {idx+1}", width='stretch')

with col2:
    st.subheader("2. ⚙️ Analysis Settings")
    
    user_role = st.selectbox(
        "🎯 Target Audience",
        ["Investor", "Financial Analyst", "Auditor", "General"],
        help="Tailor the summary for your specific role"
    )
    
    focus_areas = st.multiselect(
        "📊 Focus Areas (Optional)",
        ["Key Metrics", "Balance Sheet", "Cash Flow", "Risks", "Charts/Graphs", "All"],
        default=["All"],
        help="Select specific areas to focus on in the analysis"
    )
    
    custom_prompt = st.text_area(
        "💬 Custom Instructions (Optional)",
        placeholder="e.g., Focus specifically on cash flow trends, risk factors, and compare with previous quarter...",
        height=100
    )
    
    # Combine role and focus areas into prompt
    focus_text = ", ".join(focus_areas) if focus_areas else "All sections"
    final_prompt = f"Tailor the summary for a {user_role}. Focus on: {focus_text}. {custom_prompt}"

    analyze_btn = st.button("🔍 Scan & Analyze Documents", type="primary", disabled=not uploaded_images, use_container_width=True)

# Output Area
if analyze_btn:
    with st.spinner("🤖 Analyzing financial data and charts..."):
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("❌ Please provide a Google API Key in the sidebar.")
        else:
            result = analyze_financial_documents(uploaded_images, final_prompt)
            
            # Check if result contains error
            if result.startswith("Error"):
                st.error(f"❌ {result}")
            else:
                st.subheader("📄 Financial Summary Report")
                st.markdown(result)
                
                # Download Option
                st.download_button(
                    label="📥 Download Summary",
                    data=result,
                    file_name="financial_summary.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
                # Success Message
                st.success("✅ Analysis complete! Review the summary above or download for later.")

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini Multimodal AI & PIL | Aligned with Financial Report Analysis Requirements")

# Additional Info Section
with st.expander("ℹ️ How to Use This Tool"):
    st.markdown("""
    ### Step-by-Step Guide:
    1. **Upload Images**: Select local files or paste URLs of financial documents
    2. **Configure Settings**: Choose your role (Investor, Analyst, Auditor)
    3. **Add Custom Instructions**: Specify any particular focus areas
    4. **Analyze**: Click the scan button to generate insights
    5. **Review & Download**: Read the summary or download for sharing
    
    ### Supported Documents:
    - Annual Reports
    - Balance Sheets
    - Income Statements
    - Earnings Reports
    - Cash Flow Statements
    - Financial Charts & Graphs
    
    ### Output Sections:
    - Key Financial Metrics (Revenue, Net Income, EPS, Growth Trends)
    - Income and Expenses
    - Balance Sheet Highlights (Assets, Liabilities, Equity)
    - Credit Quality (Risk Ratios, Non-Performing Loans)
    - Strategic and Operational Updates
    - Market Conditions and Outlook
    - Shareholder Information (Dividends, Stock Performance)
    """)
