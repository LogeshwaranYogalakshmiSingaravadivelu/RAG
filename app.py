import streamlit as st
from rag_chain_of_thought import rag_chatbot_pipeline
import time

st.set_page_config(page_title="Professor Q&A Bot", page_icon="🤖")

st.title("📚 Professor Feedback Chatbot")
st.markdown("Ask a question about Professor Tejas Parikh based on TRACE survey data.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field at the bottom
user_input = st.chat_input("Ask a question about the professor...")

# Display existing chat history (from top to bottom)
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

    # Show "thinking..." below it
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("🤖 Thinking...")

    # 🔁 Get answer + optional summary
    answer, summary = rag_chatbot_pipeline(user_input, history=st.session_state.chat_history)

    # Animate the reply
    full_response = ""
    for word in answer.split():
        full_response += word + " "
        placeholder.markdown(full_response)
        time.sleep(0.03)

    # Save to session
    st.session_state.chat_history.append({"user": user_input, "bot": answer})

    # Show summary if available
    if summary:
        with st.expander("🧠 Memory Summary (used as context)"):
            st.markdown(summary)


