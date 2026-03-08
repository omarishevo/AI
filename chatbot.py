"""
AI Chatbot — Powered by Claude (Anthropic API)
A sleek, production-grade Streamlit chatbot application.
"""

import streamlit as st
import anthropic
import time
import json
from datetime import datetime

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nova · AI Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

  /* ── Global ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0A0A0F;
    color: #E8E8F0;
  }
  .stApp { background: #0A0A0F; }
  section[data-testid="stSidebar"] {
    background: #111118 !important;
    border-right: 1px solid #1E1E2E;
  }
  section[data-testid="stSidebar"] * { color: #C8C8D8 !important; }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── Chat container ── */
  .chat-wrapper {
    max-width: 820px;
    margin: 0 auto;
    padding: 2rem 1.5rem 10rem;
  }

  /* ── Header ── */
  .chat-header {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid #1E1E2E;
    margin-bottom: 2rem;
  }
  .chat-header .logo {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #A78BFA, #60A5FA, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.4rem;
  }
  .chat-header .tagline {
    font-size: 0.9rem;
    color: #6B6B8A;
    font-weight: 300;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* ── Messages ── */
  .msg-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 1.6rem;
    animation: fadeSlide 0.25s ease-out;
  }
  @keyframes fadeSlide {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .msg-row.user   { flex-direction: row-reverse; }
  .msg-row.user .bubble {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    color: #fff;
    border-radius: 18px 4px 18px 18px;
    margin-left: auto;
  }
  .msg-row.assistant .bubble {
    background: #14141F;
    border: 1px solid #1E1E2E;
    color: #DDE0F0;
    border-radius: 4px 18px 18px 18px;
  }
  .bubble {
    padding: 0.85rem 1.2rem;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.65;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
    margin-top: 2px;
  }
  .avatar.user-av {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    color: white;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
  }
  .avatar.bot-av {
    background: linear-gradient(135deg, #A78BFA22, #60A5FA22);
    border: 1px solid #2E2E4E;
    color: #A78BFA;
  }
  .msg-time {
    font-size: 0.7rem;
    color: #44445A;
    margin-top: 4px;
    text-align: right;
  }
  .msg-row.user .msg-time { text-align: right; }

  /* ── Typing indicator ── */
  .typing-indicator {
    display: flex; align-items: center; gap: 5px;
    padding: 0.7rem 1rem;
    background: #14141F;
    border: 1px solid #1E1E2E;
    border-radius: 4px 18px 18px 18px;
    width: fit-content;
  }
  .typing-dot {
    width: 7px; height: 7px;
    background: #6B6B9A;
    border-radius: 50%;
    animation: typingBounce 1.2s infinite;
  }
  .typing-dot:nth-child(2) { animation-delay: 0.2s; }
  .typing-dot:nth-child(3) { animation-delay: 0.4s; }
  @keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-6px); opacity: 1; }
  }

  /* ── Empty state ── */
  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
  }
  .empty-state .spark {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 20px #A78BFA44);
  }
  .empty-state h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #C8C8E8;
    margin-bottom: 0.5rem;
  }
  .empty-state p {
    font-size: 0.9rem;
    color: #55556A;
    max-width: 400px;
    margin: 0 auto 2rem;
  }

  /* ── Suggestion chips ── */
  .chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 1rem;
  }
  .chip {
    background: #14141F;
    border: 1px solid #2E2E4E;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.82rem;
    color: #9898B8;
    cursor: pointer;
    transition: all 0.2s;
  }
  .chip:hover {
    border-color: #A78BFA;
    color: #A78BFA;
    background: #A78BFA11;
  }

  /* ── Input area ── */
  .input-dock {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, #0A0A0F 70%, transparent);
    padding: 1rem 1.5rem 1.5rem;
    z-index: 100;
  }
  .input-inner {
    max-width: 820px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 10px;
    background: #14141F;
    border: 1px solid #2E2E4E;
    border-radius: 16px;
    padding: 0.6rem 0.6rem 0.6rem 1.2rem;
    box-shadow: 0 0 40px #A78BFA11;
  }
  .stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    color: #E8E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.4rem 0 !important;
    box-shadow: none !important;
  }
  .stTextInput > div > div > input::placeholder { color: #44445A !important; }
  .stTextInput > div { border: none !important; background: transparent !important; }

  /* ── Send button ── */
  .stButton > button {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.4rem !important;
    font-size: 0.9rem !important;
    transition: opacity 0.2s !important;
    white-space: nowrap;
  }
  .stButton > button:hover { opacity: 0.85 !important; }

  /* ── Sidebar elements ── */
  .sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #A78BFA, #60A5FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
  }
  .sidebar-sub {
    font-size: 0.72rem;
    color: #44445A !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.2rem;
  }
  .persona-card {
    background: #1A1A28;
    border: 1px solid #2E2E4E;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: border-color 0.2s;
  }
  .persona-card.active { border-color: #A78BFA; background: #A78BFA11; }
  .persona-card .pname {
    font-weight: 600;
    font-size: 0.88rem;
    color: #C8C8E8 !important;
  }
  .persona-card .pdesc {
    font-size: 0.76rem;
    color: #55556A !important;
    margin-top: 2px;
  }
  .stat-pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: #1A1A28; border: 1px solid #2E2E4E;
    border-radius: 8px; padding: 4px 10px;
    font-size: 0.76rem; color: #9898B8 !important;
    margin: 2px;
  }
  .stSelectbox > div, .stSlider, .stTextArea { color: #C8C8D8 !important; }

  /* ── Code blocks in chat ── */
  .bubble code {
    background: #0D0D1A;
    border: 1px solid #2E2E4E;
    border-radius: 4px;
    padding: 1px 5px;
    font-size: 0.85em;
    font-family: 'Courier New', monospace;
    color: #A78BFA;
  }
  .bubble pre {
    background: #0D0D1A;
    border: 1px solid #2E2E4E;
    border-radius: 8px;
    padding: 1rem;
    overflow-x: auto;
    margin: 0.5rem 0;
  }
  .bubble pre code {
    background: transparent;
    border: none;
    padding: 0;
    color: #A5D6A7;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: #0A0A0F; }
  ::-webkit-scrollbar-thumb { background: #2E2E4E; border-radius: 10px; }

  /* ── Divider ── */
  hr { border-color: #1E1E2E !important; }
</style>
""", unsafe_allow_html=True)


# ── Personas ───────────────────────────────────────────────────────────────────
PERSONAS = {
    "✦ Nova (General)": {
        "icon": "✦",
        "desc": "Helpful all-rounder",
        "system": (
            "You are Nova, a sharp, friendly, and knowledgeable AI assistant. "
            "You give clear, concise, and accurate answers. You are warm but professional. "
            "Format code blocks with proper markdown. Use bullet points for lists. "
            "When uncertain, say so clearly."
        )
    },
    "💻 Code Expert": {
        "icon": "💻",
        "desc": "Senior software engineer",
        "system": (
            "You are an expert software engineer with deep knowledge across all programming languages, "
            "frameworks, and best practices. You write clean, efficient, well-commented code. "
            "You explain technical concepts clearly. Always provide working code examples. "
            "Prefer best practices and modern approaches."
        )
    },
    "📊 Data Analyst": {
        "icon": "📊",
        "desc": "Data science & analytics",
        "system": (
            "You are a seasoned data scientist and analyst. You excel at interpreting data, "
            "suggesting statistical approaches, writing Python/R code for analysis, "
            "and explaining insights clearly to both technical and non-technical audiences. "
            "You recommend appropriate visualizations, models, and tools."
        )
    },
    "✍️ Writing Coach": {
        "icon": "✍️",
        "desc": "Creative & professional writing",
        "system": (
            "You are an expert writing coach and editor with experience in creative writing, "
            "technical documentation, and professional communication. "
            "You help improve clarity, tone, structure, and style. "
            "You can write, edit, rewrite, or give detailed feedback on any piece of writing."
        )
    },
    "🧠 Research Assistant": {
        "icon": "🧠",
        "desc": "Deep research & analysis",
        "system": (
            "You are a meticulous research assistant with broad academic knowledge. "
            "You synthesize information thoroughly, cite reasoning clearly, "
            "provide balanced perspectives, and flag areas of uncertainty. "
            "You structure your responses with clear headings and logical flow."
        )
    },
    "🩺 Health Advisor": {
        "icon": "🩺",
        "desc": "Health & wellness info",
        "system": (
            "You are a knowledgeable health information assistant. You provide clear, "
            "evidence-based health information while always reminding users to consult "
            "qualified healthcare professionals for personal medical advice. "
            "You are empathetic, clear, and thorough."
        )
    },
}

SUGGESTIONS = [
    "Explain how neural networks work",
    "Write a Python script to analyze CSV data",
    "What are the best practices for REST APIs?",
    "Help me write a professional email",
    "What causes malaria outbreaks?",
    "Summarize the latest trends in AI",
]

# ── Session State ──────────────────────────────────────────────────────────────
if "messages"        not in st.session_state: st.session_state.messages        = []
if "persona"         not in st.session_state: st.session_state.persona         = "✦ Nova (General)"
if "total_tokens"    not in st.session_state: st.session_state.total_tokens    = 0
if "total_messages"  not in st.session_state: st.session_state.total_messages  = 0
if "pending_input"   not in st.session_state: st.session_state.pending_input   = ""
if "api_key"         not in st.session_state: st.session_state.api_key         = ""


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-brand'>✦ Nova</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-sub'>AI Assistant · Powered by Claude</div>", unsafe_allow_html=True)

    # API Key input
    api_key_input = st.text_input(
        "🔑 Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-api...",
        help="Get your API key from console.anthropic.com"
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

    st.markdown("---")

    # Persona selector
    st.markdown("**🎭 Persona**")
    for persona_name, persona_data in PERSONAS.items():
        is_active = st.session_state.persona == persona_name
        card_class = "persona-card active" if is_active else "persona-card"
        st.markdown(f"""
        <div class='{card_class}'>
          <div class='pname'>{persona_name}</div>
          <div class='pdesc'>{persona_data['desc']}</div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"Select", key=f"p_{persona_name}", use_container_width=True):
            st.session_state.persona = persona_name
            st.rerun()

    st.markdown("---")

    # Model settings
    st.markdown("**⚙️ Settings**")
    model_choice = st.selectbox(
        "Model",
        ["claude-sonnet-4-5", "claude-opus-4-5", "claude-haiku-4-5-20251001"],
        index=0,
        help="Select the Claude model to use"
    )
    max_tokens = st.slider("Max Response Tokens", 256, 4096, 1024, 128)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05,
                            help="Higher = more creative, Lower = more precise")

    st.markdown("---")

    # Stats
    st.markdown("**📈 Session Stats**")
    col1, col2 = st.columns(2)
    col1.markdown(f"<div class='stat-pill'>💬 {st.session_state.total_messages}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='stat-pill'>🔤 {st.session_state.total_tokens:,}</div>", unsafe_allow_html=True)

    st.markdown("")

    # Export chat
    if st.session_state.messages:
        chat_export = json.dumps([
            {"role": m["role"], "content": m["content"], "time": m.get("time","")}
            for m in st.session_state.messages
        ], indent=2)
        st.download_button(
            "⬇️ Export Chat (JSON)",
            data=chat_export,
            file_name=f"nova_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages       = []
        st.session_state.total_tokens   = 0
        st.session_state.total_messages = 0
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;color:#33334A;text-align:center;'>"
        "Nova v2.0 · Built with Streamlit<br>Powered by Anthropic Claude"
        "</div>",
        unsafe_allow_html=True
    )


# ── Main Chat Area ─────────────────────────────────────────────────────────────
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='chat-header'>
  <div class='logo'>Nova</div>
  <div class='tagline'>Your intelligent companion · Ask anything</div>
</div>
""", unsafe_allow_html=True)

# API Key guard
if not st.session_state.api_key:
    st.markdown("""
    <div class='empty-state'>
      <div class='spark'>🔑</div>
      <h3>API Key Required</h3>
      <p>Enter your Anthropic API key in the sidebar to start chatting with Nova.</p>
      <p style='font-size:0.8rem;color:#33334A;'>
        Get your key at <b style='color:#A78BFA;'>console.anthropic.com</b>
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


def render_message(role, content, timestamp=""):
    """Render a single chat message with avatar and bubble."""
    avatar_html = (
        "<div class='avatar user-av'>You</div>"
        if role == "user"
        else f"<div class='avatar bot-av'>{PERSONAS[st.session_state.persona]['icon']}</div>"
    )
    time_html = f"<div class='msg-time'>{timestamp}</div>" if timestamp else ""

    # Escape content for safe HTML embedding
    import html as html_mod
    safe_content = html_mod.escape(content)
    # Restore markdown-style code blocks
    import re
    safe_content = re.sub(r"```(\w*)\n(.*?)```", lambda m:
        f"<pre><code>{m.group(2)}</code></pre>", safe_content, flags=re.DOTALL)
    safe_content = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe_content)

    if role == "user":
        st.markdown(f"""
        <div class='msg-row user'>
          {avatar_html}
          <div>
            <div class='bubble'>{safe_content}</div>
            {time_html}
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='msg-row assistant'>
          {avatar_html}
          <div>
            <div class='bubble'>{safe_content}</div>
            {time_html}
          </div>
        </div>""", unsafe_allow_html=True)


# ── Message History ────────────────────────────────────────────────────────────
if not st.session_state.messages:
    # Empty state with suggestions
    st.markdown(f"""
    <div class='empty-state'>
      <div class='spark'>✦</div>
      <h3>How can I help you today?</h3>
      <p>I'm {st.session_state.persona} — ask me anything.</p>
    </div>
    <div class='chips-row'>
    {"".join(f"<div class='chip'>{s}</div>" for s in SUGGESTIONS)}
    </div>
    """, unsafe_allow_html=True)

    # Clickable suggestion buttons (invisible but functional)
    cols = st.columns(3)
    for i, suggestion in enumerate(SUGGESTIONS):
        if cols[i % 3].button(suggestion, key=f"sug_{i}", use_container_width=True):
            st.session_state.pending_input = suggestion
            st.rerun()
else:
    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"], msg.get("time", ""))


# ── Chat Input ─────────────────────────────────────────────────────────────────
st.markdown("</div>", unsafe_allow_html=True)  # close chat-wrapper

st.markdown("<div class='input-dock'><div class='input-inner'>", unsafe_allow_html=True)
input_col, btn_col = st.columns([10, 1])

with input_col:
    user_input = st.text_input(
        label="chat_input",
        label_visibility="collapsed",
        placeholder=f"Message {st.session_state.persona}...",
        value=st.session_state.pending_input,
        key="chat_input_field"
    )

with btn_col:
    send = st.button("Send ➤", key="send_btn")

st.markdown("</div></div>", unsafe_allow_html=True)

# ── Handle Submission ──────────────────────────────────────────────────────────
if (send or st.session_state.pending_input) and (user_input or st.session_state.pending_input):
    query = user_input or st.session_state.pending_input
    st.session_state.pending_input = ""

    # Add user message
    ts = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": query, "time": ts})
    st.session_state.total_messages += 1

    # Call Claude API
    try:
        client = anthropic.Anthropic(api_key=st.session_state.api_key)

        # Build message history
        api_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        system_prompt = PERSONAS[st.session_state.persona]["system"]

        # Stream response
        full_response = ""
        with st.spinner(""):
            st.markdown("""
            <div class='msg-row assistant' id='typing'>
              <div class='avatar bot-av'>✦</div>
              <div class='typing-indicator'>
                <div class='typing-dot'></div>
                <div class='typing-dot'></div>
                <div class='typing-dot'></div>
              </div>
            </div>""", unsafe_allow_html=True)

            with client.messages.stream(
                model=model_choice,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=api_messages,
            ) as stream:
                for text in stream.text_stream:
                    full_response += text

            # Get token usage
            final_msg = stream.get_final_message()
            tokens_used = (final_msg.usage.input_tokens + final_msg.usage.output_tokens
                           if hasattr(final_msg, "usage") else 0)
            st.session_state.total_tokens += tokens_used

        # Store assistant response
        ts_resp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "time": ts_resp
        })
        st.session_state.total_messages += 1
        st.rerun()

    except anthropic.AuthenticationError:
        st.error("❌ Invalid API key. Please check your Anthropic API key in the sidebar.")
        st.session_state.messages.pop()

    except anthropic.RateLimitError:
        st.error("⚠️ Rate limit reached. Please wait a moment and try again.")
        st.session_state.messages.pop()

    except anthropic.APIError as e:
        st.error(f"⚠️ API error: {str(e)}")
        st.session_state.messages.pop()

    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.session_state.messages.pop()
