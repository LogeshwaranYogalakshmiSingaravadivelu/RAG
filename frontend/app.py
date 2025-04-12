import streamlit as st
import time
import requests

st.set_page_config(page_title="Professor Q&A Bot", page_icon="🤖")

st.title("📚 Professor Feedback Chatbot")
st.markdown("Ask a question about any professor based on TRACE survey data.")

@st.cache_data
def get_professors():
    try:
        response = requests.get("http://rag-api:8000/professors")  # Use your RAG API service name or IP
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Failed to load professor list: {e}")
        return []


# Professor selection dropdown
professors = get_professors()
selected_prof = st.selectbox("👩‍🏫 Select Professor", professors)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field at the bottom
user_input = st.chat_input("Ask a question about the professor...")

# Display existing chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(chat["bot"])

# Handle new input
if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Show "thinking..." message
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🤖 Thinking...")

    # 🔁 Pass full history and selected professor
    try:
        response = requests.post(
            "http://rag-api:8000/rag/ask",  # Update this URL based on your deployment
            json={
                "question": user_input,
                "history": st.session_state.chat_history,
                "professor": selected_prof
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        answer = result.get("answer", "⚠️ No answer received.")
        summary = result.get("summary", None)
    except Exception as e:
        answer = f"❌ Error: {str(e)}"
        summary = None

    # Animate assistant's reply
    full_response = ""
    for word in answer.split():
        full_response += word + " "
        placeholder.markdown(full_response)
        time.sleep(0.03)

    # Save to chat history
    st.session_state.chat_history.append({"user": user_input, "bot": answer})

    # Show memory summary if available
    if summary:
        with st.expander("🧠 Memory Summary (used as context)"):
            st.markdown(summary)
