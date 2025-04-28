# app.py

import streamlit as st
from backend.rag_pipeline import rag_answer, detect_stage  # ✅ NEW import

print("🔄 1. Script started - Initializing...")

# -----------------------------
# Streamlit Page Config
st.set_page_config(page_title="PayShield AI 💳🛡️", page_icon="💳", layout="wide")
print("⚙️ 2. Page config set")

st.title("💳 PayShield AI — Your Payment API Advisor 🛡️")
print("📛 3. Title displayed")

# -----------------------------
# Utility Function: Render Answer (with code formatting)
def render_markdown_answer(answer_text):
    if "```" in answer_text:
        st.markdown(answer_text, unsafe_allow_html=True)
    else:
        st.markdown(answer_text)

# -----------------------------
# Session State Setup
print("\n🔍 4. Checking session state...")
if "chat_history" not in st.session_state:
    print("   ➡️ chat_history not found - initializing")
    st.session_state.chat_history = []

if "selected_api" not in st.session_state:
    print("   ➡️ selected_api not found - initializing to None")
    st.session_state.selected_api = None

if "api_selected" not in st.session_state:
    print("   ➡️ api_selected not found - initializing to False")
    st.session_state.api_selected = False

if "show_typing" not in st.session_state:
    st.session_state.show_typing = False

print(f"\n📊 CURRENT STATE: api_selected={st.session_state.api_selected}, selected_api={st.session_state.selected_api}")
print(f"📜 Chat history length: {len(st.session_state.chat_history)}")

# -----------------------------
# Reset Conversation Button
st.sidebar.title("⚙️ Options")
if st.sidebar.button("🔄 Reset Conversation"):
    print("\n♻️ Reset button clicked - clearing session state")
    st.session_state.chat_history = []
    st.session_state.selected_api = None
    st.session_state.api_selected = False
    st.session_state.show_typing = False
    st.rerun()

# -----------------------------
# Chat History Display
print("\n🖥️ 5. Displaying chat history...")
for role, message in st.session_state.chat_history:
    print(f"   - Displaying {role} message: {message[:50]}...")
    if role == "user":
        with st.chat_message("user"):
            st.markdown(message)
    else:
        with st.chat_message("assistant"):
            render_markdown_answer(message)

# -----------------------------
# API Selection Form (only if not selected)
print("\n🔘 6. Checking API selection status...")
if not st.session_state.api_selected:
    print("   ➡️ API not selected yet - showing selection form")
    with st.form("api_selection_form", clear_on_submit=True):
        st.subheader("🔍 Please select your preferred Payment API:")
        api_choice = st.selectbox(
            "Which one do you want to proceed with?",
            ["Select One", "Stripe", "Adyen"]
        )
        print(f"   - User selected (in form): {api_choice}")

        submit_button = st.form_submit_button("Submit")
        print(f"   - Form submit button pressed: {submit_button}")

        if submit_button:
            print("   ➡️ Form submitted!")
            if api_choice != "Select One":
                st.session_state.selected_api = api_choice.lower()
                st.session_state.api_selected = True
                print(f"   ✅ API selected: {api_choice} - updating state")
                st.success(f"✅ You selected {api_choice}. Now you can ask technical questions about {api_choice} integration!")
                st.info("ℹ️ Please type your technical question about your selected API now.")
                print("   🔄 Triggering rerun after API selection")
                st.rerun()
            else:
                st.warning("⚠️ Please select a valid API to proceed.")
                print("   ❌ No valid API selected")
else:
    print("   ➡️ API already selected - skipping selection form")

# -----------------------------
# Chat Input and Processing
print("\n💬 7. Setting up chat input...")
user_query = st.chat_input("Ask me anything about setting up payments...")
print(f"   - Current user query: {user_query}")

if user_query:
    print("\n🎯 8. Processing user query...")
    st.session_state.chat_history.append(("user", user_query))
    print(f"   - Added user query to history: {user_query[:50]}...")

    with st.chat_message("user"):
        st.markdown(user_query)
    print("   - Displayed user message in chat")

    st.session_state.show_typing = True

    with st.spinner("🤔 Assistant is thinking..."):
        print("   - Showing typing animation...")

        previous_chats = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.chat_history])[-500:]

        # ✨✨✨ DETECT the STATE intelligently ✨✨✨
        detected_stage = detect_stage(user_query, previous_chats)
        print(f"🧠 SYSTEM DECIDED STAGE: {detected_stage.upper()}")

        # Now call rag_answer dynamically
        answer = rag_answer(
            user_query,
            user_selected_api=st.session_state.selected_api,
            previous_chats=previous_chats,
        )
        print(f"   - Received answer: {answer[:50]}...")

    with st.chat_message("assistant"):
        render_markdown_answer(answer)
    print("   - Displayed assistant message in chat")

    st.session_state.chat_history.append(("assistant", answer))
    print("   - Added assistant response to history")

print("\n🏁 9. Script execution complete (for this cycle)")
