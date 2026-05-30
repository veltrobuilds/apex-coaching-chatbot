import streamlit as st
from dotenv import load_dotenv
from src.embedder import get_or_create_vector_store
from src.chain import get_chain
from langchain_core.messages import HumanMessage, AIMessage
from datetime import datetime
import pytz

load_dotenv()

def get_ist_time():
    return datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%I:%M %p")

# ── 1. PAGE CONFIG ──
st.set_page_config(
    page_title="Apex Coaching Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 2. ULTIMATE CSS OVERRIDES FOR SIDEBAR & RESPONSIVE CHIPS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #FFFBF5 !important;
}

/* Hiding default Streamlit UI stuff except sidebar controller */
#MainMenu,
footer,
.stDeployButton,
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    visibility: hidden !important;
    display: none !important;
}

/* Centralized main container */
.block-container {
    max-width: 860px !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 2rem 1.5rem 10rem 1.5rem !important;
}

/* Sidebar design */
[data-testid="stSidebar"] {
    background-color: #FEF3C7 !important;
    border-right: 1px solid #FDE68A !important;
}
[data-testid="stSidebar"] * { color: #92400E !important; }

/* ── PROBLEM 1 FIXED: ENFORCING SIDEBAR TOGGLE BUTTON VISIBILITY ── */
[data-testid="stSidebarCollapseButton"] {
    visibility: visible !important;
    display: flex !important;
    background-color: #D97706 !important;
    color: white !important;
    border-radius: 0 10px 10px 0 !important;
    position: fixed !important;
    top: 50% !important;
    left: 0 !important;
    transform: translateY(-50%) !important;
    z-index: 999999 !important;
    box-shadow: 2px 2px 10px rgba(217,119,6,0.3) !important;
    width: 32px !important;
    height: 52px !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease-in-out !important;
}
[data-testid="stSidebarCollapseButton"]:hover {
    background-color: #B45309 !important;
}
[data-testid="stSidebarCollapseButton"] svg {
    fill: white !important;
    stroke: white !important;
    width: 18px !important;
    height: 18px !important;
}

/* Topbar header */
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

/* Welcome Text Block */
.welcome-box { text-align: center; padding: 20px 20px 10px; }
.welcome-icon-wrap {
    width: 54px; height: 54px; background: #D97706; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; margin: 0 auto 12px;
}
.welcome-title { font-size: 22px; font-weight: 700; color: #1C1917; margin-bottom: 6px; }
.welcome-sub { font-size: 13px; color: #A8A29E; }

/* Pure Orange Global Button Override */
div.stButton > button {
    background-color: #D97706 !important;
    color: white !important;
    border: 1px solid #B45309 !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.15s ease-in-out !important;
    box-shadow: 0 2px 6px rgba(217,119,6,0.15) !important;
}
div.stButton > button:hover {
    background-color: #B45309 !important;
    border-color: #92400E !important;
}

/* Chat Field styling */
[data-testid="stBottom"], [data-testid="stBottom"] > div {
    background-color: #FFFBF5 !important;
}
[data-testid="stChatInput"] {
    border: 1.5px solid #FDE68A !important;
    border-radius: 30px !important;
}

/* Chat Layout structure */
.custom-chat-row { display: flex; width: 100%; margin-bottom: 16px; gap: 10px; }
.row-user { flex-direction: row-reverse; }
.row-bot { flex-direction: row; }
.custom-avatar-circle {
    width: 34px; height: 34px; background-color: #D97706; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0;
}
.custom-msg-bubble { max-width: 72%; padding: 12px 16px; font-size: 14px; line-height: 1.65; }
.bubble-user { background-color: #D97706; color: white; border-radius: 16px 16px 4px 16px; }
.bubble-bot { background-color: white; color: #44403C; border: 1px solid #FDE68A; border-radius: 16px 16px 16px 4px; }
.custom-meta { font-size: 9px; color: #A8A29E; font-family: monospace; margin-top: 5px; }

/* Typing Effect */
.typing-box { display: flex; align-items: center; gap: 5px; padding: 4px 2px; }
.typing-dot { width: 6px; height: 6px; border-radius: 50%; background: #D97706; animation: wave 0.8s infinite ease-in-out; }
.typing-dot:nth-child(2) { animation-delay: 0.15s; }
.typing-dot:nth-child(3) { animation-delay: 0.30s; }
@keyframes wave { 0%, 100% { transform: translateY(0); opacity: 0.4; } 50% { transform: translateY(-5px); opacity: 1; } }

.veltro-footer { text-align: center; font-size: 10px; color: #D1C4A0; font-family: monospace; padding: 16px; border-top: 1px solid #FDE68A; margin-top: 32px; }

/* ── PROBLEM 2 FIXED: CSS FLEX PATTERN FOR TOTAL PHONE SCREEN FULL COVER RESPONSIVENESS ── */
@media (max-width:768px){

.block-container{
    padding-left:16px !important;
    padding-right:16px !important;
}

div.stButton{
    width:100% !important;
}

div.stButton > button{
    width:100% !important;
    display:block !important;
    min-height:60px !important;
}

.custom-msg-bubble{
    max-width:95% !important;
}

}
</style>
""", unsafe_allow_html=True)

# ── 3. SIDEBAR ELEMENT ──
with st.sidebar:
    st.markdown("## 🎓 APEX AI")
    st.markdown('<div style="font-size:9px;letter-spacing:2px;color:#D97706;margin-top:-10px;margin-bottom:16px;font-family:monospace;">POWERED BY VELTRO</div>', unsafe_allow_html=True)
    st.divider()
    
    st.markdown('<div style="font-size:9px;letter-spacing:2px;margin-bottom:10px;font-family:monospace;">ASK ABOUT</div>', unsafe_allow_html=True)
    for topic in ["📚 Courses & Fees", "⏰ Batch Timings", "📝 Admissions", "👨‍🏫 Faculty & Results", "🏠 Hostel & Facilities"]:
        st.markdown(f'<div style="padding:4px 6px;font-size:12px;color:#92400E;">• {topic}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown('<div style="font-size:9px;letter-spacing:2px;margin-bottom:10px;font-family:monospace;">BOOK FREE DEMO</div>', unsafe_allow_html=True)
    st.text_input("Name", placeholder="Your name", label_visibility="collapsed", key="sb_name")
    st.text_input("Phone", placeholder="+91 phone number", label_visibility="collapsed", key="sb_phone")
    st.selectbox("Course", ["Select course", "JEE Main / Advanced", "NEET", "Class 11 / 12", "Foundation (8-10)"], label_visibility="collapsed", key="sb_course")
    st.button("Secure Free Demo Seat →", key="sb_submit")
    
    st.divider()
    if st.button("🗑 Reset Conversation", key="sb_reset"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.show_welcome = True
        st.rerun()

# ── 4. APP TOPBAR ──
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

# ── 5. PERSISTENT STATES ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if "chain" not in st.session_state:
    try:
        vector_store = get_or_create_vector_store("data/coaching_faq.txt")
        st.session_state.chain = get_chain(vector_store)
    except Exception:
        st.session_state.chain = None

# ── 6. WELCOME LAYOUT & SMART HORIZONTAL CHIPS ──
if st.session_state.show_welcome and not st.session_state.messages:
    st.markdown("""
    <div class="welcome-box">
      <div class="welcome-icon-wrap">🎓</div>
      <div class="welcome-title">Hi! I'm Apex's AI Assistant</div>
      <div class="welcome-sub">Ask me anything about courses, fees, admissions, or timings</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    chips = [
        "📚 Courses offered?",
        "💰 Fee structure?",
        "⏰ Batch timings?",
        "🏆 Results 2025?"
    ]

    for i, chip in enumerate(chips):
        if st.button(
            chip,
            key=f"chip_{i}",
            use_container_width=True
        ):
            st.session_state.show_welcome = False
            msg_time = get_ist_time()

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": chip,
                    "time": msg_time
                }
            )

            st.session_state.active_processing = True
            st.rerun()
            
# ── 7. DATA PIPELINE ──
if st.session_state.get("active_processing", False):
    target = st.session_state.messages[-1]["content"]
    ts = st.session_state.messages[-1]["time"]
    if st.session_state.chain is not None:
        try:
            response = st.session_state.chain.invoke({"input": target, "chat_history": st.session_state.chat_history})
            answer = response["answer"]
            st.session_state.messages.append({"role": "assistant", "content": answer, "time": ts})
            st.session_state.chat_history.extend([HumanMessage(content=target), AIMessage(content=answer)])
        except Exception:
            st.warning("Knowledge base temporarily unavailable.")
    st.session_state.active_processing = False
    st.rerun()

# ── 8. RENDER CHAT ──
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="custom-chat-row row-user">
          <div class="custom-avatar-circle">🧑‍🎓</div>
          <div class="custom-msg-bubble bubble-user">
            <div>{message["content"]}</div>
            <div class="custom-meta" style="text-align:right; color:rgba(255,255,255,0.6)">You · {message.get("time","")}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="custom-chat-row row-bot">
          <div class="custom-avatar-circle">👨‍🏫</div>
          <div class="custom-msg-bubble bubble-bot">
            <div>{message["content"]}</div>
            <div class="custom-meta">Apex AI · {message.get("time","")}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── 9. SYSTEM BOTTOM INPUT ──
if prompt := st.chat_input("Ask about Apex Coaching..."):
    st.session_state.show_welcome = False
    msg_time = get_ist_time()
    st.session_state.messages.append({"role": "user", "content": prompt, "time": msg_time})

    st.markdown(f"""
    <div class="custom-chat-row row-user">
      <div class="custom-avatar-circle">🧑‍🎓</div>
      <div class="custom-msg-bubble bubble-user">
        <div>{prompt}</div>
        <div class="custom-meta" style="text-align:right; color:rgba(255,255,255,0.6)">You · {msg_time}</div>
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

    if st.session_state.chain is not None:
        try:
            response = st.session_state.chain.invoke({"input": prompt, "chat_history": st.session_state.chat_history})
            answer = response["answer"]
            typing_ph.empty()
            st.session_state.messages.append({"role": "assistant", "content": answer, "time": msg_time})
            st.session_state.chat_history.extend([HumanMessage(content=prompt), AIMessage(content=answer)])
        except Exception as e:
            typing_ph.empty()
            st.error(f"Error: {str(e)}")
    else:
        typing_ph.empty()
        st.error("Knowledge base load nahi ho paya.")

    st.rerun()

st.markdown('<div class="veltro-footer">Powered by Veltro AI</div>', unsafe_allow_html=True)
