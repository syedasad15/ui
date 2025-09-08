import streamlit as st
import datetime
import uuid

st.set_page_config(page_title="Judiciary GPT", layout="wide")

# ================= Custom CSS =================
st.markdown(
    """
    <style>
    /* Hide Streamlit default header & footer */
    header, footer {visibility: hidden;}

    /* Page container */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 1000px;
        margin: 0 auto;
    }

    /* Header row */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .signout-btn {
        background-color: rgba(239,68,68,0.9);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
    }
    .signout-btn:hover {background-color: rgba(239,68,68,1);}

    /* Chat area */
    .chat-area {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        height: 65vh;
        overflow-y: auto;
        padding: 0.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        background: rgba(255,255,255,0.02);
    }

    .msg-user {
        text-align: right;
        background: rgba(59,130,246,0.2);
        padding: 10px 14px;
        border-radius: 12px;
        margin: 6px 0;
        color: white;
        max-width: 70%;
        margin-left: auto;
    }

    .msg-assistant {
        text-align: left;
        background: rgba(255,255,255,0.08);
        padding: 10px 14px;
        border-radius: 12px;
        margin: 6px 0;
        color: white;
        max-width: 70%;
    }

    .msg-timestamp {
        font-size: 10px;
        color: gray;
        margin-top: 4px;
    }

    /* Bottom input bar */
    .chatbox {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.8rem;
    }

    .plus-btn {
        background: rgba(255,255,255,0.1);
        color: white;
        border: none;
        padding: 10px;
        border-radius: 8px;
        font-size: 18px;
        cursor: pointer;
    }

    .send-btn {
        background: rgba(59,130,246,0.9);
        color: white;
        border: none;
        padding: 12px 22px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 15px;
        font-weight: 500;
    }
    .send-btn:hover {background: rgba(59,130,246,1);}
    </style>
    """,
    unsafe_allow_html=True,
)

# ================= Session State =================
if "chats" not in st.session_state:
    st.session_state.chats = [
        {
            "id": "1",
            "title": "Sample Chat",
            "messages": [
                {"id": "m1", "sender": "user", "content": "Hello JudgeGPT", "timestamp": datetime.datetime.now()},
                {"id": "m2", "sender": "assistant", "content": "Hi 👋 I am Judiciary GPT.", "timestamp": datetime.datetime.now()},
            ],
            "lastUpdated": datetime.datetime.now(),
        }
    ]
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "1"


# ================= Helper =================
def get_current_chat():
    return next((c for c in st.session_state.chats if c["id"] == st.session_state.current_chat), None)


# ================= Sidebar =================
with st.sidebar:
    st.markdown(
        """
        <div style="padding:12px; border-bottom:1px solid rgba(255,255,255,0.1);">
            <p style="margin:0; font-weight:bold; font-size:16px; color:white;">👤 User Name</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("➕  New Chat", use_container_width=True):
        cid = str(uuid.uuid4())
        st.session_state.chats.insert(0, {
            "id": cid,
            "title": "New conversation",
            "messages": [],
            "lastUpdated": datetime.datetime.now(),
        })
        st.session_state.current_chat = cid

    st.text_input("🔍 Search chats", key="chat_search", placeholder="Search chats...")

    filtered = [c for c in st.session_state.chats if st.session_state.chat_search.lower() in c["title"].lower()]
    for chat in filtered:
        if st.button(f"💬 {chat['title']}", key=chat["id"], use_container_width=True):
            st.session_state.current_chat = chat["id"]


# ================= Main =================
# Title row
st.markdown(
    """
    <div class="app-header">
        <h2 style="margin:0; color:white;">⚖️ Judiciary GPT</h2>
        <button class="signout-btn">🚪 Sign Out</button>
    </div>
    """,
    unsafe_allow_html=True,
)

# Chat Messages
current_chat = get_current_chat()
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

if current_chat and current_chat["messages"]:
    for msg in current_chat["messages"]:
        if msg["sender"] == "user":
            st.markdown(
                f"""
                <div class="msg-user">
                    {msg["content"]}
                    <div class="msg-timestamp">{msg["timestamp"].strftime('%H:%M')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="msg-assistant">
                    {msg["content"]}
                    <div class="msg-timestamp">{msg["timestamp"].strftime('%H:%M')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.markdown(
        "<div style='text-align:center; padding:20px; color:rgba(255,255,255,0.6);'>"
        "Welcome back! Start a new conversation or select one from the sidebar."
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)  # close chat-area

# Bottom Chatbox
st.markdown(
    """
    <div class="chatbox">
        <button class="plus-btn">➕</button>
        <textarea placeholder="✍️ Message Judiciary GPT..." rows="3" style="
            flex-grow:1;
            border-radius:8px;
            border:1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.05);
            color:white;
            padding:10px;
            font-size:14px;
            resize:none;
        "></textarea>
        <button class="send-btn">📨 Send</button>
    </div>
    """,
    unsafe_allow_html=True,
)
