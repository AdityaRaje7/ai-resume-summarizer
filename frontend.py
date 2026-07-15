import streamlit as st
import requests
import json  # Moved to the top for best practices

# 1. Setting up page configuration
st.set_page_config(
    page_title="AI Resume Summarizer",
    page_icon="📄",
    layout="centered"
)  

# 2. Build the header of the app
st.title("🤖 AI Resume Summarizer")
st.markdown("Upload your resume in PDF format, and let our AI engine extract the text for you!")
st.divider()

# 3. Create a file uploader widget
uploaded_file = st.file_uploader("Drag and drop your file here", type=["pdf"])

# 4. Action Button Logic
if uploaded_file is not None:
    # If the user uploads a file, show the button to extract text
    if st.button("Extract Resume Text", type="primary"):
        
        # Show a spinner while processing
        with st.spinner("Extracting and analyzing text..."):
            
            # Step A: Prepare the file for sending to the backend
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            
            try:
                # Step B: Make API call to our local server (Forced IPv4 for Windows 11)
                response = requests.post(
                    "https://ai-resume-backend-5p9v.onrender.com/api/v1/extract-text",
                    files=files
                )
                
                # Step C: Handle the successful response from the backend
                if response.status_code == 200:
                    data = response.json()
                    st.success("AI analysis completed successfully!")

                    # Step D: Try to parse the AI's JSON output safely
                    try:
                        ai_data = json.loads(data.get("ai_analysis", "{}"))

                        # Display metric cards
                        st.subheader(f"Candidate: {ai_data.get('name', 'Unknown')}")

                        col1, col2 = st.columns(2)
                        with col1:
                            # Convert to string just in case the AI returns an integer (e.g., 5 instead of "5")
                            st.metric("Years of Experience", str(ai_data.get("experience", "N/A")))
                        with col2:
                            # Convert to string just in case the AI returns a list instead of comma-separated text
                            skills_text = str(ai_data.get("skills", "Not Found"))
                            st.info("**Core Skills:**\n" + skills_text)

                        st.write("---")
                        st.write("**Summary Verdict:**")
                        st.write(ai_data.get('summary', 'No summary provided.'))
                        
                    except json.JSONDecodeError:
                        st.warning("The AI returned data, but it wasn't formatted correctly. Please try again.")
                        # Show raw text so the user can at least see what the AI said
                        st.text(data.get("ai_analysis"))
                
                # Step E: Handle backend errors (like uploading an empty PDF)
                else:
                    error_detail = response.json().get("detail", "Unknown API Error")
                    st.error(f"Backend Error: {error_detail}")

            # Step F: Handle connection failures (Backend server is offline)
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Failed: Cannot reach the backend server. Is Uvicorn running on 127.0.0.1:8000?")