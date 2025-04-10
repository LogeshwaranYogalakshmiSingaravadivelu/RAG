import streamlit as st
from rag_chain_of_thought import rag_chatbot_pipeline
import time
import psycopg2
from config.settings import DB_CONFIG

st.set_page_config(page_title="Professor Q&A Bot", page_icon="🤖")

st.title("📚 Professor Feedback Chatbot")
st.markdown("Ask a question about any professor based on TRACE survey data.")

# 🔄 Load professor names from PostgreSQL
@st.cache_data
def get_professors_from_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT instructor_name FROM course_info")
    rows = cursor.fetchall()
    conn.close()
    return sorted([row[0] for row in rows if row[0]])

# Professor selection dropdown
professors = get_professors_from_db()
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
    answer, summary = rag_chatbot_pipeline(user_input, history=st.session_state.chat_history, professor=selected_prof)

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
