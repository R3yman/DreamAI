import streamlit as st
from langserve import RemoteRunnable

# Initialize the RemoteRunnable
remote_chain = RemoteRunnable("http://localhost:8000/chain/")

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("Chat with AI")

# Display conversation history
for entry in st.session_state.history:
    if entry["role"] == "user":
        st.text_area(f'You:', entry["content"], height=75, key=f'user_{entry["content"]}')
    else:
        st.text_area(f'AI:', entry["content"], height=75, key=f'ai_{entry["content"]}')

# Create a form for user input at the bottom
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You:")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_input:
    # Append user message to history
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # Get AI response
    ai_response = remote_chain.invoke({"input": user_input},
                                      {"configurable": {"session_id": 'unused'}})
    
    # Append AI response to history
    st.session_state.history.append({"role": "ai", "content": ai_response})
    
    # Clear the input field by reloading the form with an empty input
    st.experimental_rerun()

# Note: Remove the following line to avoid infinite loop issues.
# st.experimental_rerun()