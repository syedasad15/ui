import streamlit as st
import datetime
import uuid

st.set_page_config(page_title="Judiciary GPT", layout="wide")

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
if "attached_files" not in st.session_state:
    st.session_state.attached_files = []
if "is_web_search" not in st.session_state:
    st.session_state.is_web_search = False
if "show_add_options" not in st.session_state:
    st.session_state.show_add_options = False


# ================= Helper =================
def get_current_chat():
    return next((c for c in st.session_state.chats if c["id"] == st.session_state.current_chat), None)


# ================= Sidebar =================
with st.sidebar:
    # User Info
    st.markdown(
        """
        <div style="padding:12px; border-bottom:1px solid rgba(255,255,255,0.1);">
            <p style="margin:0; font-weight:bold; font-size:16px; color:white;">👤 User Name</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # New Chat Button
    if st.button("➕  New Chat", use_container_width=True):
        cid = str(uuid.uuid4())
        st.session_state.chats.insert(0, {
            "id": cid,
            "title": "New conversation",
            "messages": [],
            "lastUpdated": datetime.datetime.now(),
        })
        st.session_state.current_chat = cid

    # Search
    st.text_input("🔍 Search chats", key="chat_search", placeholder="Search chats...")

    # Chat History
    filtered = [c for c in st.session_state.chats if st.session_state.chat_search.lower() in c["title"].lower()]
    for chat in filtered:
        if st.button(f"💬 {chat['title']}", key=chat["id"], use_container_width=True):
            st.session_state.current_chat = chat["id"]


# ================= Main =================
col_header, col_signout = st.columns([8, 1])
with col_header:
    st.markdown("<h2 style='color:white;'>⚖️ Judiciary GPT</h2>", unsafe_allow_html=True)
with col_signout:
    st.markdown(
        """
        <button style="
            background-color:rgba(255,255,255,0.1);
            color:white;
            border:none;
            padding:8px 14px;
            border-radius:8px;
            cursor:pointer;
            font-size:13px;
            transition:0.2s;
            width:100%;
        "
        onmouseover="this.style.backgroundColor='rgba(255,255,255,0.2)'"
        onmouseout="this.style.backgroundColor='rgba(255,255,255,0.1)'">
            🚪 Sign Out
        </button>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# Chat Messages
current_chat = get_current_chat()
if current_chat:
    for msg in current_chat["messages"]:
        if msg["sender"] == "user":
            st.markdown(
                f"""
                <div style="
                    text-align:right; 
                    background:rgba(59,130,246,0.2); 
                    padding:10px 14px; 
                    border-radius:12px; 
                    margin:6px 0; 
                    color:white;
                    max-width:70%;
                    margin-left:auto;">
                    {msg["content"]}
                    <div style="font-size:10px; color:gray; margin-top:4px;">
                        {msg["timestamp"].strftime('%H:%M')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="
                    text-align:left; 
                    background:rgba(255,255,255,0.08); 
                    padding:10px 14px; 
                    border-radius:12px; 
                    margin:6px 0; 
                    color:white;
                    max-width:70%;">
                    {msg["content"]}
                    <div style="font-size:10px; color:gray; margin-top:4px;">
                        {msg["timestamp"].strftime('%H:%M')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.markdown(
        "<div style='text-align:center; padding:40px; color:rgba(255,255,255,0.6);'>"
        "Welcome back! Start a new conversation or select one from the sidebar."
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)


# ================= Bottom Chatbox =================
st.markdown("### ")  # spacer

# File previews
if st.session_state.attached_files:
    st.markdown("**📎 Attached Files:**")
    for f in st.session_state.attached_files:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:8px; margin:4px 0; 
                        padding:6px; border:1px solid rgba(255,255,255,0.2); border-radius:8px;">
                📄 <span>{f.name}</span>
                <span style="font-size:10px; color:gray;">({round(f.size/1024,1)} KB)</span>
                <button style="margin-left:auto; background:red; color:white; border:none;
                               border-radius:4px; padding:2px 6px; font-size:10px; cursor:pointer;">
                    ❌
                </button>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Proper flexbox row (no overlap)
st.markdown(
    """
    <div style="display:flex; align-items:center; gap:10px; margin-top:10px;">
        <!-- Plus Button -->
        <button style="
            background-color:rgba(255,255,255,0.1);
            color:white;
            border:none;
            padding:12px;
            border-radius:8px;
            cursor:pointer;
            font-size:18px;
            flex:0 0 50px;
        "
        onmouseover="this.style.backgroundColor='rgba(255,255,255,0.2)'"
        onmouseout="this.style.backgroundColor='rgba(255,255,255,0.1)'">
            ➕
        </button>

        <!-- Chatbox -->
        <textarea placeholder="✍️ Message Judiciary GPT..." 
            style="
                flex:1;
                height:70px;
                padding:10px;
                border-radius:8px;
                border:1px solid rgba(255,255,255,0.2);
                background:rgba(255,255,255,0.05);
                color:white;
                resize:none;
                font-size:14px;
            "></textarea>

        <!-- Send Button -->
        <button style="
            background-color:rgba(59,130,246,0.9);
            color:white;
            border:none;
            padding:12px 20px;
            border-radius:8px;
            cursor:pointer;
            font-size:15px;
            font-weight:bold;
            flex:0 0 90px;
            transition:0.2s;
        "
        onmouseover="this.style.backgroundColor='rgba(59,130,246,1)'"
        onmouseout="this.style.backgroundColor='rgba(59,130,246,0.9)'">
            📨 Send
        </button>
    </div>
    """,
    unsafe_allow_html=True,
)

# Dropdown options
if st.session_state.show_add_options:
    st.markdown("---")
    uploaded = st.file_uploader("📄 Attach File", type=["pdf", "docx", "txt", "png", "jpg"])
    if uploaded:
        st.session_state.attached_files.append(uploaded)

    st.checkbox("🌐 Enable Web Search", key="is_web_search")
