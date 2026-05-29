import streamlit as st
from dotenv import load_dotenv
from src.embedder import get_or_create_vector_store
from src.chain import get_chain
from langchain_core.messages import HumanMessage, AIMessage
import time

load_dotenv()

# ─────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Apex Coaching Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────
# CSS — Same on local + deployed
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── BASE ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #FFFBF5 !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    visibility: hidden !important;
    display: none !important;
}

/* ── BLOCK CONTAINER ── */
.block-container {
    max-width: 860px !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 1.5rem 2rem 10rem 2rem !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background-color: #FEF3C7 !important;
    border-right: 1px solid #FDE68A !important;
    min-width: 260px !important;
}
[data-testid="stSidebar"] * { color: #92400E !important; }

[data-testid="stSidebar"] .stTextInput input {
    background: #FFF8E7 !important;
    border: 1px solid #FCD34D !important;
    border-radius: 10px !important;
    color: #92400E !important;
    font-size: 13px !important;
    padding: 10px !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: #D97706 !important;
    opacity: 0.5 !important;
}

/* Sidebar selectbox */
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background: #D97706 !important;
    border-radius: 10px !important;
    border: 1px solid #B45309 !important;
    color: white !important;
}
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background: #D97706 !important;
    color: white !important;
}
[data-testid="stSidebar"] svg { fill: white !important; }

/* Sidebar buttons */
[data-testid="stSidebar"] div.stButton > button {
    background: #D97706 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 700 !important;
    width: 100% !important;
}
[data-testid="stSidebar"] div.stButton > button:hover {
    background: #B45309 !important;
}

/* Sidebar collapse button */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: #D97706 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    z-index: 999999 !important;
}
[data-testid="collapsedControl"]:hover { background: #B45309 !important; }

/* ── TOPBAR ── */
.topbar {
    background: white;
    border: 1px solid #FDE68A;
    border-radius: 12px;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
    box-shadow: 0 1px 4px rgba(217,119,6,0.06);
}
.topbar-title { font-size: 15px; font-weight: 700; color: #1C1917; }
.topbar-sub { font-size: 11px; color: #A8A29E; margin-top: 2px; }
.badge {
    font-size: 10px; padding: 5px 12px; border-radius: 999px;
    font-family: monospace; display: inline-flex; align-items: center; gap: 6px;
}
.badge-green { background: #F0FDF4; color: #16A34A; border: 1px solid #BBF7D0; }
.badge-speed { background: #FEF3C7; color: #D97706; border: 1px solid #FDE68A; }

/* ── WELCOME ── */
.welcome-box { text-align: center; padding: 32px 20px 24px; }
.welcome-icon-wrap {
    width: 54px; height: 54px; background: #D97706; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 12px;
}
.welcome-title { font-size: 22px; font-weight: 700; color: #1C1917; margin-bottom: 6px; }
.welcome-sub { font-size: 13px; color: #A8A29E; }

/* ── CHIP BUTTONS ── */
.chip-btn button {
    background: #FFF7ED !important;
    color: #92400E !important;
    border: 1px solid #FDE68A !important;
    border-radius: 999px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    width: 100% !important;
    padding: 8px 12px !important;
    transition: all 0.2s !important;
}
.chip-btn button:hover {
    background: #FED7AA !important;
    border-color: #F97316 !important;
}

/* ── CHAT BUBBLES ── */
.custom-chat-row {
    display: flex; width: 100%;
    margin-bottom: 16px; gap: 10px;
}
.row-user { flex-direction: row-reverse; }
.row-bot { flex-direction: row; }

.custom-avatar-circle {
    width: 34px; height: 34px;
    background-color: #D97706 !important;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}

.custom-msg-bubble {
    max-width: 72%;
    padding: 12px 16px;
    font-size: 14px; line-height: 1.65;
    word-break: break-word;
}
.bubble-user {
    background-color: #D97706 !important;
    color: #FFFFFF !important;
    border-radius: 16px 16px 4px 16px !important;
}
.bubble-user-text { color: #FFFFFF !important; font-weight: 500 !important; }
.bubble-bot {
    background-color: #FFFFFF !important;
    color: #44403C !important;
    border: 1px solid #FDE68A !important;
    border-radius: 16px 16px 16px 4px !important;
    box-shadow: 0 1px 4px rgba(217,119,6,0.06) !important;
}
.bubble-bot-text { color: #44403C !important; }
.custom-meta {
    font-size: 9px; color: #A8A29E;
    font-family: monospace; margin-top: 5px;
}
.meta-user { text-align: right; color: rgba(255,255,255,0.6) !important; }

/* ── TYPING DOTS ── */
.typing-box { display: flex; align-items: center; gap: 5px; padding: 4px 2px; }
.typing-dot {
    width: 6px; height: 6px; border-radius: 50%; background: #D97706;
    animation: waveBounce 0.8s infinite ease-in-out;
}
.typing-dot:nth-child(2) { animation-delay: 0.15s; }
.typing-dot:nth-child(3) { animation-delay: 0.30s; }
@keyframes waveBounce {
    0%, 100% { transform: translateY(0); opacity: 0.4; }
    50% { transform: translateY(-5px); opacity: 1; }
}

/* ── CHAT INPUT — works on deployed too ── */

/* Remove dark bottom bar background */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div {
    background-color: #FFFBF5 !important;
    border-top: 1px solid #FDE68A !important;
}

/* Input container */
[data-testid="stChatInput"],
div[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #FDE68A !important;
    border-radius: 999px !important;
    padding: 4px 12px !important;
    box-shadow: 0 1px 8px rgba(217,119,6,0.08) !important;
}

/* Textarea text color */
[data-testid="stChatInput"] textarea,
div[data-testid="stChatInput"] textarea {
    color: #92400E !important;
    -webkit-text-fill-color: #92400E !important;
    background-color: transparent !important;
    caret-color: #D97706 !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
}

/* Placeholder */
[data-testid="stChatInput"] textarea::placeholder,
div[data-testid="stChatInput"] textarea::placeholder {
    color: #D97706 !important;
    -webkit-text-fill-color: #D97706 !important;
    opacity: 0.55 !important;
}

/* Focus glow */
[data-testid="stChatInput"]:focus-within {
    border-color: #F97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.12) !important;
}

/* Send button */
[data-testid="stChatInput"] button,
div[data-testid="stChatInput"] button {
    background: #D97706 !important;
    border-radius: 50% !important;
    color: white !important;
    border: none !important;
}

/* ── FOOTER ── */
.veltro-footer {
    text-align: center; font-size: 10px; color: #D1C4A0;
    font-family: monospace; padding: 16px;
    border-top: 1px solid #FDE68A; margin-top: 32px;
}

/* ── MOBILE ── */
@media (max-width: 768px) {
    .block-container { padding: 1rem 1rem 8rem !important; }
    .custom-msg-bubble { max-width: 88% !important; font-size: 13px !important; }
    .welcome-title { font-size: 18px !important; }
    .topbar { flex-direction: column; align-items: flex-start; gap: 10px; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 APEX AI")
    st.markdown(
        '<div style="font-size:9px;letter-spacing:2px;color:#D97706;'
        'margin-top:-10px;margin-bottom:16px;font-family:monospace;">'
        'POWERED BY VELTRO</div>', unsafe_allow_html=True
    )
    st.divider()

    st.markdown(
        '<div style="font-size:9px;letter-spacing:2px;margin-bottom:10px;'
        'font-family:monospace;">ASK ABOUT</div>', unsafe_allow_html=True
    )
    for topic in ["📚 Courses & Fees", "⏰ Batch Timings", "📝 Admissions",
                  "👨‍🏫 Faculty & Results", "🏠 Hostel & Facilities"]:
        st.markdown(
            f'<div style="padding:4px 6px;font-size:12px;color:#92400E;">• {topic}</div>',
            unsafe_allow_html=True
        )
    st.divider()

    st.markdown(
        '<div style="font-size:9px;letter-spacing:2px;margin-bottom:10px;'
        'font-family:monospace;">BOOK FREE DEMO</div>', unsafe_allow_html=True
    )
    st.text_input("Name", placeholder="Your name", label_visibility="collapsed", key="sb_name")
    st.text_input("Phone", placeholder="+91 phone number", label_visibility="collapsed", key="sb_phone")
    st.selectbox("Course",
        ["Select course", "JEE Main / Advanced", "NEET", "Class 11 / 12", "Foundation (8-10)"],
        label_visibility="collapsed", key="sb_course"
    )
    st.button("Secure Free Demo Seat →", key="sb_submit")

    st.divider()
    if st.button("🗑 Reset Conversation", key="sb_reset"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.show_welcome = True
        st.rerun()

    st.markdown(
        '<div style="font-size:9px;color:#D1C4A0;font-family:monospace;'
        'text-align:center;margin-top:16px;">veltro.build@gmail.com</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────
# TOPBAR
# ─────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div>
    <div class="topbar-title">Apex Coaching Assistant</div>
    <div class="topbar-sub">AI-powered · Answers from official knowledge base</div>
  </div>
  <div style="display:flex;gap:8px;align-items:center;">
    <span class="badge badge-speed">⚡ ~0.1s</span>
    <span class="badge badge-green">
      <span style="width:6px;height:6px;border-radius:50%;background:#22C55E;display:inline-block;"></span>
      Online
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if "chain" not in st.session_state:
    with st.spinner("Loading knowledge base..."):
        try:
            vector_store = get_or_create_vector_store("data/coaching_faq.txt")
            st.session_state.chain = get_chain(vector_store)
        except Exception:
            st.session_state.chain = None

# ─────────────────────────────────────────────────────
# WELCOME + CHIPS
# ─────────────────────────────────────────────────────
if st.session_state.show_welcome and not st.session_state.messages:
    st.markdown("""
    <div class="welcome-box">
      <div class="welcome-icon-wrap">🎓</div>
      <div class="welcome-title">Hi! I'm Apex's AI Assistant</div>
      <div class="welcome-sub">Ask me anything about courses, fees, admissions, or timings</div>
    </div>
    """, unsafe_allow_html=True)

    chips = ["📚 Courses offered?", "💰 Fee structure?", "⏰ Batch timings?", "🏆 Results 2025?"]
    cols = st.columns(4, gap="small")
    for i, chip in enumerate(chips):
        with cols[i]:
            st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
            if st.button(chip, key=f"chip_{i}"):
                st.session_state.show_welcome = False
                msg_time = time.strftime("%I:%M %p")
                st.session_state.messages.append({"role": "user", "content": chip, "time": msg_time})
                st.session_state.active_processing = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# CHIP PROCESSING
# ─────────────────────────────────────────────────────
if st.session_state.get("active_processing", False):
    target = st.session_state.messages[-1]["content"]
    ts = st.session_state.messages[-1]["time"]
    try:
        response = st.session_state.chain.invoke({
            "input": target,
            "chat_history": st.session_state.chat_history
        })
        answer = response["answer"]
        st.session_state.messages.append({"role": "assistant", "content": answer, "time": ts})
        st.session_state.chat_history.extend([HumanMessage(content=target), AIMessage(content=answer)])
    except Exception:
        st.warning("Knowledge base temporarily unavailable.")
    st.session_state.active_processing = False
    st.rerun()

# ─────────────────────────────────────────────────────
# CHAT HISTORY DISPLAY
# ─────────────────────────────────────────────────────
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="custom-chat-row row-user">
          <div class="custom-avatar-circle">🧑‍🎓</div>
          <div class="custom-msg-bubble bubble-user">
            <div class="bubble-user-text">{message["content"]}</div>
            <div class="custom-meta meta-user">You · {message.get("time","")}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="custom-chat-row row-bot">
          <div class="custom-avatar-circle">👨‍🏫</div>
          <div class="custom-msg-bubble bubble-bot">
            <div class="bubble-bot-text">{message["content"]}</div>
            <div class="custom-meta">Apex AI · {message.get("time","")}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about Apex Coaching..."):
    st.session_state.show_welcome = False
    msg_time = time.strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": msg_time})

    st.markdown(f"""
    <div class="custom-chat-row row-user">
      <div class="custom-avatar-circle">🧑‍🎓</div>
      <div class="custom-msg-bubble bubble-user">
        <div class="bubble-user-text">{prompt}</div>
        <div class="custom-meta meta-user">You · {msg_time}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    typing_ph = st.empty()
    typing_ph.markdown("""
    <div class="custom-chat-row row-bot">
      <div class="custom-avatar-circle">👨‍🏫</div>
      <div class="custom-msg-bubble bubble-bot">
        <div class="typing-box">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        response = st.session_state.chain.invoke({
            "input": prompt,
            "chat_history": st.session_state.chat_history
        })
        answer = response["answer"]
        typing_ph.empty()
        st.session_state.messages.append({"role": "assistant", "content": answer, "time": msg_time})
        st.session_state.chat_history.extend([HumanMessage(content=prompt), AIMessage(content=answer)])
    except Exception as e:
        typing_ph.empty()
        st.error(f"Error: {str(e)}")

    st.rerun()

# ─────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────
st.markdown('<div class="veltro-footer">Powered by Veltro AI</div>', unsafe_allow_html=True)