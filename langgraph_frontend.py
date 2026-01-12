import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph_chatbot import build_graph


st.set_page_config(page_title="LangGraph Chat", layout="centered")
st.title("🤖 LangGraph Streaming Chat")


if "chatbot" not in st.session_state:
    st.session_state.chatbot = build_graph()

chatbot = st.session_state.chatbot


if "message_history" not in st.session_state:
    st.session_state.message_history = []

for msg in st.session_state.message_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


user_input = st.chat_input("Ask something...")

if user_input:
  
    st.session_state.message_history.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.message_history.append(
        {"role": "assistant", "content": ""}
    )

    assistant_placeholder = st.empty()
    full_response = ""

   
    for chunk, _ in chatbot.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": 1}},
        stream_mode="messages"
    ):
        if chunk.content:
            full_response += chunk.content
            st.session_state.message_history[-1]["content"] = full_response
            assistant_placeholder.markdown(full_response)

    # final render
    with st.chat_message("assistant"):
        st.write(full_response)

 
