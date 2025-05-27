import streamlit as st
from src.question_handler import classify_question, handle_descriptive, run_what_if_scenario, handle_reset, handle_continue,handle_optimization
from rapidfuzz import fuzz


# 🔧 Page config
st.set_page_config(page_title="LogiFlow Chat", page_icon="🤖", layout="wide")

# 🧠 Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "thinking" not in st.session_state:
    st.session_state.thinking = False
# 🧶 Main handler
def is_greeting(text):
    greetings = ["hi", "hello", "hey", "greetings", "hola", "howdy", "yo", "sup", "good morning", "good evening"]
    text = text.lower()
    for greet in greetings:
        if fuzz.token_set_ratio(text, greet) >= 80:
            return True
    return False

def handle_question():
    question = st.session_state.input_text.strip()
    if not question:
        return

    st.session_state.thinking = True
    st.session_state.messages.append({"role": "user", "text": question})
    st.session_state.input_text = ""

    try:
        question_type = classify_question(question)
        
        if question_type == "reset":
            response = handle_reset() 

        elif question_type == "greeting":
            response = "👋 Hello! I’m your AI assistant for supply chain planning. How can I help you today?"

        elif question_type == "continue":
            response = handle_continue()

        elif question_type == "descriptive":
            response = handle_descriptive(question)

        elif question_type == "optimization":
            response = handle_optimization(question)

        elif question_type == "what-if":
            summary = run_what_if_scenario(question)
            response = (
                summary
                + "\n\nAll set! I’ve applied that change. "
                + "Would you like to keep exploring this scenario, or should we switch back to the original numbers? "
                + "Just say ‘keep going’ or ‘reset.’"
            )

        else:
            response = "❓ I couldn't determine the question type. Please try again."

    except Exception as e: 
        response = "🧠 Hmm, I wasn’t able to process that. Try rephrasing it."
        print("Error:", e)
        import traceback; traceback.print_exc()

    st.session_state.messages.append({"role": "bot", "text": response})
    st.session_state.thinking = False

# 🌈 CSS
st.markdown("""
    <style>
        .main { background-color: #F8F9FA; }
        .chat-container { max-width: 800px; margin: auto; }
        .message { padding: 1rem; border-radius: 10px; margin-bottom: 1rem; font-size: 16px; line-height: 1.5; }
        .user { background-color: #f0f4ff; text-align: right; border: 1px solid #d6e1ff; }
        .bot { background-color: #e6f5ea; text-align: left; border: 1px solid #bfe5d0; }
        .avatar { font-size: 20px; font-weight: bold; margin-bottom: 0.2rem; }
        .footer { text-align: center; margin-top: 30px; color: gray; font-size: 13px; }
        .sticky-header {
            position: sticky;
            top: 0;
            background-color: #F8F9FA;
            z-index: 1000;
            padding-top: 10px;
            padding-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
    </style>
""", unsafe_allow_html=True)



st.markdown("""
<div class='chat-container' style='text-align: center; padding-top: 1rem;'>
    <div style='display: inline-flex; flex-direction: column; align-items: center; gap: 0.5rem;'>
        <h1 style='margin: 0; font-size: 40px;'>🤖 LogiFlow AI Assistant</h1>
        <p style='color: #5D6D7E; font-size: 15px; margin: 0;'>Optimize Logistics. Streamline Operations.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 💬 Chat history
with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role = msg["role"]
        bubble_class = "user" if role == "user" else "bot"
        icon = "👩‍💼" if role == "user" else "🤖"
        st.markdown(f"<div class='message {bubble_class}'><div class='avatar'>{icon}</div>{msg['text']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 🖋️ Text input
# 🖋️ Text input with embedded SVG Enter icon
# 🖋️ Text input with SVG icon inside
# 🖋️ Input box with SVG enter icon inside (streamlit-compatible)

st.markdown("""
<style>
.input-container {
    position: relative;
    max-width: 800px;
    margin: 1rem auto 0 auto; /* changed from 2rem top */
   
}

/* 🔧 Prevent overflow clipping */
[data-baseweb="input"] {
    min-height: 60px !important;
    border: none !important;
    box-shadow: none !important;
    overflow: visible !important;
}

/* ✅ Main input style */
input[type="text"] {
    min-height: 60px !important;
    font-size: 17px !important;
    padding: 14px 45px 14px 20px !important;
    border-radius: 6px !important;
    border: 1px solid #D1D9E6 !important;
    box-sizing: border-box;
    transition: border 0.3s ease, box-shadow 0.3s ease;
    background-color: #f4f6f9 !important;
}

/* ✨ Focus blue border + soft glow */
input[type="text"]:focus {
    border: 1px solid #8AC8FF !important;
    box-shadow: 0 0 6px rgba(0, 123, 255, 0.4) !important;
    outline: none !important;
}

/* ✅ Suppress red invalid border */
input[type="text"]:focus:invalid {
    border: 1px solid #8AC8FF !important;
    box-shadow: 0 0 6px rgba(0, 123, 255, 0.4) !important;
}

/* 🧠 Enter icon */
.enter-icon {
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-178%);
    font-size: 20px;
    opacity: 0.3;
    pointer-events: none;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    st.text_input(
        label="💬 Enter a query for analysis or insights",
        key="input_text",
        placeholder="Type your question here..",
        on_change=handle_question
    )
    if st.session_state.get("thinking", False):
        st.markdown("""
            <div style='text-align: left; padding-top: 5px; font-size: 14px; color: #888; max-width: 800px; margin: 0 auto;'>
                🤖 Thinking...
            </div>
        """, unsafe_allow_html=True)
        st.write("Thinking state:", st.session_state.thinking)
    st.markdown('<span class="enter-icon">⏎</span>', unsafe_allow_html=True)
   
    st.markdown('</div>', unsafe_allow_html=True)

# 📅 Footer
st.markdown("""
    <div class='footer'>🚀 Built with Streamlit | AI-powered Logistics Assistant</div>
""", unsafe_allow_html=True)