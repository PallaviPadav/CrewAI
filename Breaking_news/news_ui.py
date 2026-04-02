import streamlit as st
from main import generate_news

st.set_page_config(page_title="Breaking News Generator", layout="wide")

st.title("📰 AI Breaking News Generator")

# User input
topic = st.text_input("Enter News Topic")
    
# Add more sidebar controls if needed
st.markdown("### LLM Settings")
temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

# Add some spacing
st.markdown("---")

# Button
if st.button("Generate News"):
    if topic:
        with st.spinner("Fetching latest news... ⏳"):
            content, filename = generate_news(topic, temperature)

        st.success("News Generated Successfully!")

        # Display output
        st.markdown("### 🧾 Generated News")
        st.markdown(content)

        # Download button
        st.download_button(
            label="📥 Download as Markdown",
            data=content,
            file_name=filename,
            mime="text/markdown"
        )
    else:
        st.warning("Please enter a topic")