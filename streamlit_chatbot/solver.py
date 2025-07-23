import streamlit as st
from openai import OpenAI
import random
import base64
import datetime
import time
import json
import os
from dotenv import load_dotenv
load_dotenv()


# Set up OpenAI API
OPENAI_API_KEY = os.getenv("your openai api key")
client = OpenAI(api_key=OPENAI_API_KEY)


MEMORY_FILE = "chat_memory.json"

# Initialize or load long-term memory
def initialize_session_state():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            st.session_state.messages = json.load(f)
    else:
        st.session_state.messages = []

# Save chat to file
def save_chat():
    if st.session_state.messages:
        with open(MEMORY_FILE, "w") as f:
            json.dump(st.session_state.messages, f, indent=2)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_{timestamp}.txt"
        content = "\n\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
        b64 = base64.b64encode(content.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Chat History</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.markdown(
            """
            <script>
                var elem = window.parent.document.querySelector('.main');
                if(elem){ elem.scrollTo({ top: elem.scrollHeight, behavior: 'smooth' }); }
            </script>
            """,
            unsafe_allow_html=True
        )

# Get OpenAI response
def get_openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Add emojis
def add_emojis(text):
    emojis = ["💡", "😄", "🤖", "🧠", "✨", "✅", "📌", "📚", "👍"]
    lines = text.split("\n")
    enhanced = [f"{random.choice(emojis)} {line}" if line.strip() else line for line in lines]
    return "\n".join(enhanced)

# Typewriter animation at bottom
def typewriter_display(text, speed=0.01):
    placeholder = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.markdown(f"<div style='font-size: 1rem; line-height: 1.6;'>{displayed_text}</div>", unsafe_allow_html=True)
        time.sleep(speed)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
html, body, [class*="css"]  { font-family: 'Poppins', sans-serif; }
body, .stApp { background-color: #000000; color: white; }
.stButton>button { background: linear-gradient(to right, #06b6d4, #3b82f6); color: white; border-radius: 0.5rem; font-weight: bold; transition: all 0.3s ease; }
.stButton>button:hover { background: linear-gradient(to right, #3b82f6, #06b6d4); }
.stTextInput>div>div>input { background-color: #1f2937; color: white; border: 1px solid #3b82f6; border-radius: 0.5rem; }
.chat-bubble { animation: fadeIn 0.1s ease-in-out; }
@keyframes fadeIn { from {opacity: 0; transform: translateY(10px);} to {opacity: 1; transform: translateY(0);} }
.mascot { animation: float 3s ease-in-out infinite; }
@keyframes float { 0% { transform: translateY(0);} 50% { transform: translateY(-5px);} 100% { transform: translateY(0);} }
.chat-row { display: flex; flex-direction: row; align-items: flex-start; margin-bottom: 1rem; }
.chat-left { justify-content: flex-start; }
.chat-right { justify-content: flex-start; }
.chat-content { max-width: 70%; }
.chat-avatar { width: 32px; height: 32px; border-radius: 50%; margin-right: 0.5rem; }
.chat-reactions { margin-top: 4px; font-size: 1rem; opacity: 0.7; }
</style>
""", unsafe_allow_html=True)

# Main
def main():
    st.set_page_config(page_title="Constantine AI Assistant", page_icon="🧠", layout="wide")

    base_context = """
    You are Constantine AI Assistant — smart, friendly, and creative. You help users make decisions, give advice, and explore ideas.
    You always consider:
    - Human psychology (e.g., indecision, pros/cons, emotions)
    - Common sense reasoning
    - Popular culture references
    - Motivational and encouraging tone
    - Current knowledge from 2024
    """

    st.markdown(f"""
        <div style='display:flex;align-items:center;gap:1rem'>
            <img class='mascot' src='https://cdn-icons-png.flaticon.com/512/4712/4712034.png' width='50'>
            <h2 style='color:#93c5fd;'>🧠 Constantine AI Assistant</h2>
        </div>
        <p style='color:#a5b4fc;'>{random.choice(["Hi there!","Welcome!","Hello, I’m Constantine, your smart assistant!","Ready to decide smartly?"])}</p>
    """, unsafe_allow_html=True)

    initialize_session_state()
    st.markdown("<hr>", unsafe_allow_html=True)
    mode = st.selectbox("Choose assistant mode:", ["Auto Detect", "Decision Helper", "Advice Giver", "Creative Ideas", "General Chat"])

    if user_input := st.chat_input("Type your question, dilemma, or idea here..."):
        st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": datetime.datetime.now().isoformat()})

        if mode == "Decision Helper":
            context = f"You are Constantine AI Assistant, a decision-making guide. Help the user choose.\nUser said: '{user_input}'. Give pros/cons, suggestions, and a final verdict."
        elif mode == "Advice Giver":
            context = f"You are Constantine AI Assistant, a wise and friendly advisor.\nUser said: '{user_input}'. Offer helpful suggestions and reasoning."
        elif mode == "Creative Ideas":
            context = f"You are Constantine AI Assistant, a creative brainstorming partner.\nUser input: '{user_input}'. Return 3–5 fun, useful, or clever ideas."
        elif mode == "General Chat":
            context = f"You are Constantine AI Assistant. The user says: '{user_input}'. Respond with helpful or friendly conversation."
        else:
            if any(q in user_input.lower() for q in ["?", "should", "what", "how", "do i", "can i"]):
                context = f"You are Constantine AI Assistant. The user has a question or decision to make.\nUser said: '{user_input}'. Answer with logic, clarity, and friendliness."
            else:
                context = f"User said: '{user_input}'. Respond with something smart, friendly, or helpful."

        final_prompt = base_context + "\n\n" + context
        response = get_openai_response(final_prompt)
        response = add_emojis(response)
        st.session_state.messages.append({"role": "assistant", "content": response, "timestamp": datetime.datetime.now().isoformat()})
        save_chat()

        st.markdown("<hr>", unsafe_allow_html=True)
        with st.chat_message("assistant"):
            typewriter_display(response)

        st.markdown(
            """
            <script>
                var elem = window.parent.document.querySelector('.main');
                if(elem){ elem.scrollTo({ top: elem.scrollHeight, behavior: 'smooth' }); }
            </script>
            """, unsafe_allow_html=True
        )

    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                avatar_url = 'https://cdn-icons-png.flaticon.com/512/4712/4712034.png'
                name = "Constantine"
                name_color = "#60a5fa"
            else:
                avatar_url = 'https://cdn-icons-png.flaticon.com/512/149/149071.png'
                name = "You"
                name_color = "#a3e635"

            st.markdown(f"<div style='font-weight:bold; color:{name_color}'>{name}</div>", unsafe_allow_html=True)
            st.write(message["content"])

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🎲 Still can’t decide?")
    options_input = st.text_input("Enter your choices (comma separated)")
    col1, col2 = st.columns([1, 1])
    if col1.button("Pick one for me!"):
        options = [opt.strip() for opt in options_input.split(",") if opt.strip()]
        if len(options) >= 2:
            choice = random.choice(options)
            st.success(f"✅ I pick: **{choice}**")
        else:
            st.warning("Please enter at least two choices.")

    if col2.button("🎲 Random"):
        sample_options = ["Pizza or Burger", "Study or Nap", "Go Out or Stay In", "Read or Watch", "Cat or Dog"]
        random_option = random.choice(sample_options)
        st.info(f"Try this dilemma: **{random_option}**")

    st.markdown("---")
    st.caption("Built with ❤️ and OpenAI | Constantine AI Assistant 🧠")

if __name__ == "__main__":
    main()



