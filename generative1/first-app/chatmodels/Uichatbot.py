import streamlit as st
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from chatbot import model, new_history, SYSTEM_PROMPT, EXIT_WORDS, PERSONAS

st.set_page_config(page_title="AI Agent", page_icon="💬", layout="centered")

CUSTOM = "Custom"
CUSTOM_META = {
    "emoji": "✏️",
    "title": "Custom Agent",
    "tagline": "Apne rules, apni personality.",
    "accent": "#0E9AA7",
    "welcome": "Namaste! Sidebar mein jo personality likhi hai, main ab wahi hoon.",
}

# ---------- Static styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700&family=Figtree:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap');

    html, body, [class*="css"], .stMarkdown, textarea, input {
        font-family: 'Figtree', sans-serif;
    }
    code, pre, [data-testid="stCode"] * { font-family: 'JetBrains Mono', monospace !important; }

    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
    .stApp { background: #F5F6FA; }
    .block-container { padding-top: 2rem; max-width: 780px; }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] { background: #171C2B; }
    [data-testid="stSidebar"] * { color: #E7EAF3; }
    [data-testid="stSidebar"] .side-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.35rem; font-weight: 700; margin-bottom: 2px;
    }
    [data-testid="stSidebar"] .side-sub { color: #98A1B8; font-size: 0.85rem; margin-bottom: 18px; }
    [data-testid="stSidebar"] .side-label { font-weight: 600; margin: 6px 0 8px 0; }

    /* persona picker rows */
    [data-testid="stSidebar"] div[role="radiogroup"] { gap: 6px; }
    [data-testid="stSidebar"] label[data-baseweb="radio"] {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 10px 14px;
        width: 100%;
        margin: 0;
        transition: background 0.15s ease;
    }
    [data-testid="stSidebar"] label[data-baseweb="radio"]:hover { background: rgba(255,255,255,0.10); }
    [data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child { display: none; }
    [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) { background: var(--accent); }
    [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) * { color: #fff; font-weight: 600; }

    [data-testid="stSidebar"] textarea { background: #0F1320; color: #E7EAF3; border-radius: 10px; }
    [data-testid="stSidebar"] .stButton button {
        background: transparent;
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 12px;
        width: 100%;
        font-weight: 600;
    }
    [data-testid="stSidebar"] .stButton button:hover { border-color: var(--accent); color: #fff; background: var(--accent); }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.10); }

    /* ---------- Header ---------- */
    .hero { display: flex; align-items: center; gap: 16px; margin-bottom: 22px; }
    .hero .badge {
        width: 56px; height: 56px; border-radius: 16px;
        background: var(--accent);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.7rem; flex-shrink: 0;
    }
    .hero h1 {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 2rem; font-weight: 700; margin: 0; color: #161B2E; line-height: 1.1;
    }
    .hero p { margin: 4px 0 0 0; color: #5C6580; }
    .hero .chip {
        margin-left: auto; font-size: 0.8rem; color: #5C6580;
        border: 1px solid #DCE1EC; background: #fff;
        padding: 4px 10px; border-radius: 999px; white-space: nowrap;
    }

    /* ---------- Messages ---------- */
    [data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid #E4E8F0;
        border-left: 4px solid var(--accent);
        border-radius: 4px 18px 18px 18px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: none;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: var(--accent);
        border: none;
        border-radius: 18px 4px 18px 18px;
        flex-direction: row-reverse;
        margin-left: 12%;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] li {
        color: #fff; text-align: right;
    }

    /* ---------- Input ---------- */
    [data-testid="stChatInput"] {
        border-radius: 16px;
        border: 1px solid #D5DBE7;
        background: #fff;
    }
    [data-testid="stChatInput"]:focus-within { border-color: var(--accent); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar: persona choices ----------
options = list(PERSONAS.keys()) + [CUSTOM]

with st.sidebar:
    st.markdown("<div class='side-title'>AI Agent</div>", unsafe_allow_html=True)
    st.markdown("<div class='side-sub'>Personality chuno, phir chat karo.</div>", unsafe_allow_html=True)
    st.markdown("<div class='side-label'>Persona</div>", unsafe_allow_html=True)

    choice = st.radio(
        "Persona",
        options,
        format_func=lambda p: f"{(PERSONAS.get(p) or CUSTOM_META)['emoji']}   {p}",
        label_visibility="collapsed",
        key="persona_choice",
    )

    if choice == CUSTOM:
        meta = CUSTOM_META
        system_prompt = st.text_area(
            "Apni personality likho",
            value="You are a ",
            height=120,
            key="custom_prompt",
            help="Ctrl+Enter dabao ya bahar click karo, chat naye prompt ke saath restart hogi.",
        ).strip() or SYSTEM_PROMPT
    else:
        meta = PERSONAS[choice]
        system_prompt = meta["prompt"]
        st.caption(system_prompt)

    # Persona / prompt badla to nayi chat shuru
    signature = (choice, system_prompt)
    if st.session_state.get("signature") != signature:
        st.session_state.signature = signature
        st.session_state.messages = new_history(system_prompt)

    st.write("")
    if st.button("+ New chat"):
        st.session_state.messages = new_history(system_prompt)
        st.rerun()

    st.divider()
    st.caption("Persona badalne par chat reset hoti hai. Type exit, quit ya bye to end the chat.")

# ---------- Accent colour for the chosen persona ----------
st.markdown(f"<style>:root {{ --accent: {meta['accent']}; }}</style>", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown(
    f"""
    <div class="hero">
        <div class="badge">{meta['emoji']}</div>
        <div>
            <h1>{meta['title']}</h1>
            <p>{meta['tagline']}</p>
        </div>
        <div class="chip">{model.model} on Ollama</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- History ----------
history = [m for m in st.session_state.messages if not isinstance(m, SystemMessage)]

if not history:
    with st.chat_message("assistant", avatar=meta["emoji"]):
        st.write(meta["welcome"])

for msg in history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=meta["emoji"]):
            st.write(msg.content)

# ---------- New message ----------
prompt = st.chat_input("Apna message yahan likho...")

if prompt:
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=meta["emoji"]):
        if prompt.strip().lower() in EXIT_WORDS:
            reply = "Goodbye!"
            st.write(reply)
            st.session_state.messages.append(AIMessage(content=reply))
        else:
            def stream_reply():
                for chunk in model.stream(st.session_state.messages):
                    yield chunk.content

            try:
                reply = st.write_stream(stream_reply())
                st.session_state.messages.append(AIMessage(content=reply))
            except Exception as e:
                st.session_state.messages.pop()  # unanswered user message hata do
                st.error(
                    f"Model se connect nahi ho paya. Check karo ki Ollama chal raha hai "
                    f"aur {model.model} pulled hai.\n\nDetails: {e}"
                )