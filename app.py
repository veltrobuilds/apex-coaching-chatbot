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
# FIXED PRODUCTION CSS — Chat Input Visibility Patched
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #FFFBF5 !important;
}

/* ── CRITICAL SCROLL ENGINE FIX ── */
html, body, .stApp, .stAppViewContainer, .main, [data-testid="stAppViewWithSidebar"], .st-emotion-cache-1jicfl2, .st-emotion-cache-z5fcl4 {
    overflow-y: auto !important;
    overflow-x: hidden !important;
    height: auto !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 12rem !important;
    max-width: 85% !important;
    margin: 0 auto !important;
}

/* HIDE STREAMLIT PLATFORM OVERLAYS */
#MainMenu, footer, header, .stDeployButton {
    visibility: hidden !important;
    display: none !important;
}

/* ── SIDEBAR INTERFACE NODES ── */
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
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background: #FFF8E7 !important;
    border-radius: 10px !important;
    border: 1px solid #FCD34D !important;
}

/* Sidebar Primary CTA Buttons */
div.stButton > button:first-child {
    background: #D97706 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 700 !important;
    width: 100% !important;
}
div.stButton > button:first-child:hover { background: #B45309 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #D97706 !important;
    border: 1px solid #FDE68A !important;
}

/* ── BRANDING TOPBAR STRIP ── */
.topbar {
    background: white;
    border-bottom: 1px solid #FDE68A;
    padding: 14px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: -20px;
    margin-bottom: 24px;
    border-radius: 12px;
    box-shadow: 0 1px 4px rgba(217,119,6,0.02);
}
.topbar-title { font-size: 16px; font-weight: 700; color: #1C1917; }
.topbar-sub { font-size: 11px; color: #A8A29E; margin-top: 2px; }

.badge {
    font-size: 10px; padding: 6px 12px; border-radius: 999px; font-family: monospace;
    display: inline-flex; align-items: center; gap: 6px;
}
.badge-green { background: #F0FDF4; color: #16A34A; border: 1px solid #BBF7D0; }
.badge-speed { background: #FEF3C7; color: #D97706; border: 1px solid #FDE68A; }

/* WELCOME BOX CONFIG */
.welcome-box { text-align: center; padding: 32px 20px; }
.welcome-icon-wrap {
    width: 54px; height: 54px; background: #D97706; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto;
}
.welcome-title { font-size: 24px; font-weight: 700; color: #1C1917; margin-bottom: 6px; }
.welcome-sub { font-size: 13.5px; color: #A8A29E; }

.chip-btn button {
    background: #FEF3C7 !important; color: #92400E !important;
    border: 1px solid #FDE68A !important; border-radius: 999px !important;
    font-size: 13px !important; font-weight: 600 !important;
}

/* ── PURE CUSTOM RAW HTML CHAT CONTAINER CELLS ── */
.custom-chat-row {
    display: flex;
    width: 100%;
    margin-bottom: 16px;
    gap: 12px;
}
.row-user { flex-direction: row-reverse; }
.row-bot { flex-direction: row; }

.custom-avatar-circle {
    width: 32px;
    height: 32px;
    background-color: #D97706 !important;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.custom-msg-bubble {
    max-width: 75%;
    padding: 12px 16px;
    font-size: 14px;
    line-height: 1.6;
}

/* User Message bubble */
.bubble-user {
    background-color: #D97706 !important;
    color: #FFFFFF !important;
    border-radius: 14px 14px 2px 14px !important;
    text-align: left;
}
.bubble-user-text {
    color: #FFFFFF !important;
    font-weight: 500 !important;
}

/* Assistant Bot bubble */
.bubble-bot {
    background-color: #FFFFFF !important;
    color: #44403C !important;
    border: 1px solid #FDE68A !important;
    border-radius: 14px 14px 14px 2px !important;
    box-shadow: 0 1px 4px rgba(217,119,6,0.04) !important;
}
.bubble-bot-text {
    color: #44403C !important;
}

.custom-meta {
    font-size: 9.5px;
    color: #A8A29E;
    font-family: monospace;
    margin-top: 5px;
}
.meta-user { text-align: right; color: #EAE6D9 !important; }

/* ══════════════════════════════════════════════════
   ✅ NUCLEAR CHAT INPUT FIX — Bottom bar + textarea
   ══════════════════════════════════════════════════ */

/* 1. Bottom strip ka dark background hatao */
[data-testid="stBottom"] {
    background-color: #FFFBF5 !important;
}
[data-testid="stBottom"] > div {
    background-color: #FFFBF5 !important;
}

/* 2. Chat input outer wrapper */
[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #FDE68A !important;
    border-radius: 999px !important;
    padding: 4px 10px !important;
}

/* 3. Textarea — text visible karo */
[data-testid="stChatInput"] textarea {
    color: #B45309 !important;
    -webkit-text-fill-color: #B45309 !important;
    background-color: #FFFFFF !important;
    caret-color: #D97706 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}

/* 4. Placeholder color */
[data-testid="stChatInput"] textarea::placeholder {
    color: #D97706 !important;
    -webkit-text-fill-color: #D97706 !important;
    opacity: 0.6 !important;
}

/* 5. Focus state glow */
[data-testid="stChatInput"]:focus-within {
    border-color: #D97706 !important;
    box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.15) !important;
}

/* DYNAMIC ACTIVE ASYNC WAVE DOTS */
.typing-box { display: flex; align-items: center; gap: 4px; padding: 4px 6px; width: 44px; }
.typing-dot {
    width: 5px; height: 5px; border-radius: 50%; background-color: #D97706;
    animation: waveBounce 0.8s infinite ease-in-out;
}
.typing-dot:nth-child(2) { animation-delay: 0.15s; }
.typing-dot:nth-child(3) { animation-delay: 0.3s; }
@keyframes waveBounce {
    0%, 100% { transform: translateY(0); opacity: 0.4; }
    50% { transform: translateY(-4px); opacity: 1; }
}

.veltro-footer {
    text-align: center; font-size: 10px; color: #D1C4A0; font-family: monospace;
    padding: 14px; border-top: 1px solid #FDE68A; margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# SIDEBAR BUILD
# ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 APEX AI")
    st.markdown('<div style="font-size:9px; letter-spacing:2px; color:#D97706; margin-top:-10px; margin-bottom:16px; font-family:monospace;">POWERED BY VELTRO</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown('<div style="font-size:9px; letter-spacing:2px; margin-bottom:10px; font-family:monospace;">ASK ABOUT</div>', unsafe_allow_html=True)
    topics = ["📚 Courses & Fees", "⏰ Batch Timings", "📝 Admissions", "👨‍🏫 Faculty & Results", "🏠 Hostel & Facilities"]
    for topic in topics:
        st.markdown(f'<div style="padding:4px 6px; font-size:12px; color:#92400E;">• {topic}</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown('<div style="font-size:9px; letter-spacing:2px; margin-bottom:10px; font-family:monospace;">BOOK FREE DEMO</div>', unsafe_allow_html=True)
    st.text_input("Name", placeholder="Your name", label_visibility="collapsed", key="sb_name")
    st.text_input("Phone", placeholder="+91 phone number", label_visibility="collapsed", key="sb_phone")
    st.selectbox("Course", ["Select course", "JEE Main / Advanced", "NEET", "Foundation (8-10)"], label_visibility="collapsed", key="sb_course")
    st.button("Secure Free Demo Seat →", key="sb_submit")

    st.divider()
    if st.button("🗑 Reset Conversation", key="sb_reset"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.show_welcome = True
        st.rerun()

    st.markdown('<div style="font-size:9px; color:#D1C4A0; font-family:monospace; text-align:center; margin-top:16px;">veltro.build@gmail.com</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# TOPBAR BRANDING BLOCKS
# ─────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">Apex Coaching Assistant</div>
        <div class="topbar-sub">AI-powered · Answers from official knowledge base</div>
    </div>
    <div style="display:flex; gap:8px; align-items:center;">
        <span class="badge badge-speed">⚡ ~0.1s</span>
        <span class="badge badge-green">
            <span style="width:6px; height:6px; border-radius:50%; background:#22C55E; display:inline-block;"></span>
            Online
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# PERSISTENT ARRAYS TRACK INITIALIZATION
# ─────────────────────────────────────────────────────
if "messages" not in st.session_state: st.session_state.messages = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "show_welcome" not in st.session_state: st.session_state.show_welcome = True

if "chain" not in st.session_state:
    with st.spinner("Loading knowledge base..."):
        try:
            vector_store = get_or_create_vector_store("data/coaching_faq.txt")
            st.session_state.chain = get_chain(vector_store)
        except Exception as e:
            st.error(f"Initialization Failed: {str(e)}")

# ─────────────────────────────────────────────────────
# WELCOME BOARD ENGINE & ACTION CHIPS
# ─────────────────────────────────────────────────────
if st.session_state.show_welcome and not st.session_state.messages:
    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-icon-wrap"><div class="welcome-icon">🎓</div></div>
        <div class="welcome-title">Hi! I'm Apex's AI Assistant</div>
        <div class="welcome-sub">Ask me anything about courses, fees, admissions, or timings</div>
    </div>
    """, unsafe_allow_html=True)

    chips = ["📚 Courses offered?", "💰 Fee structure?", "⏰ Batch timings?", "🏆 Results 2024?"]
    cols = st.columns(4)

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

if st.session_state.get("active_processing", False):
    target_query = st.session_state.messages[-1]["content"]
    current_ts = st.session_state.messages[-1]["time"]
    try:
        response = st.session_state.chain.invoke({"input": target_query, "chat_history": st.session_state.chat_history})
        answer = response["answer"]
        st.session_state.messages.append({"role": "assistant", "content": answer, "time": current_ts})
        st.session_state.chat_history.extend([HumanMessage(content=target_query), AIMessage(content=answer)])
    except Exception as e:
        st.error(f"Inference Failure: {str(e)}")
    st.session_state.active_processing = False
    st.rerun()

# ─────────────────────────────────────────────────────
# DISPATCH RE-PAINT: CHAT HISTORY DISPLAY LOOP
# ─────────────────────────────────────────────────────
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="custom-chat-row row-user">
            <div class="custom-avatar-circle">🧑‍🎓</div>
            <div class="custom-msg-bubble bubble-user">
                <div class="bubble-user-text">{message["content"]}</div>
                <div class="custom-meta meta-user">You · {message.get('time','')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="custom-chat-row row-bot">
            <div class="custom-avatar-circle">👨‍🏫</div>
            <div class="custom-msg-bubble bubble-bot">
                <div class="bubble-bot-text">{message["content"]}</div>
                <div class="custom-meta">Apex AI · {message.get('time','')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# LIVE INPUT TERMINAL CONTROLLER INTERFACE
# ─────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about Apex Coaching..."):
    st.session_state.show_welcome = False
    msg_time = time.strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": msg_time})

    # Render user query instantly
    st.markdown(f"""
    <div class="custom-chat-row row-user">
        <div class="custom-avatar-circle">🧑‍🎓</div>
        <div class="custom-msg-bubble bubble-user">
            <div class="bubble-user-text">{prompt}</div>
            <div class="custom-meta meta-user">You · {msg_time}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Typing wave indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown(f"""
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
        typing_placeholder.empty()

        st.session_state.messages.append({"role": "assistant", "content": answer, "time": msg_time})
        st.session_state.chat_history.extend([HumanMessage(content=prompt), AIMessage(content=answer)])
    except Exception as e:
        typing_placeholder.empty()
        st.error(f"Inference Error: {str(e)}")

    st.rerun()

# ── ENDCAP FOOTER LAYOUT ──────────────────────────────
st.markdown('<div class="veltro-footer">Powered by Veltro AI</div>', unsafe_allow_html=True)