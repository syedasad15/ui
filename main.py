# import streamlit as st
# import datetime
# import uuid

# st.set_page_config(page_title="Judiciary GPT", layout="wide")

# # ================= Session State =================
# if "chats" not in st.session_state:
#     st.session_state.chats = [
#         {
#             "id": "1",
#             "title": "Sample Chat",
#             "messages": [
#                 {"id": "m1", "sender": "user", "content": "Hello JudgeGPT", "timestamp": datetime.datetime.now()},
#                 {"id": "m2", "sender": "assistant", "content": "Hi 👋 I am Judiciary GPT.", "timestamp": datetime.datetime.now()},
#             ],
#             "lastUpdated": datetime.datetime.now(),
#         }
#     ]
# if "current_chat" not in st.session_state:
#     st.session_state.current_chat = "1"
# if "attached_files" not in st.session_state:
#     st.session_state.attached_files = []
# if "is_web_search" not in st.session_state:
#     st.session_state.is_web_search = False
# if "show_add_options" not in st.session_state:
#     st.session_state.show_add_options = False
# if "chat_search" not in st.session_state:
#     st.session_state.chat_search = ""


# # ================= Helper =================
# def get_current_chat():
#     return next((c for c in st.session_state.chats if c["id"] == st.session_state.current_chat), None)


# # ================= Sidebar =================
# with st.sidebar:
#     st.markdown("### 👤 User Name")

#     if st.button("➕ New Chat", use_container_width=True):
#         cid = str(uuid.uuid4())
#         st.session_state.chats.insert(0, {
#             "id": cid,
#             "title": "New conversation",
#             "messages": [],
#             "lastUpdated": datetime.datetime.now(),
#         })
#         st.session_state.current_chat = cid

#     st.text_input("🔍 Search chats", key="chat_search", placeholder="Search chats...")

#     filtered = [c for c in st.session_state.chats if st.session_state.chat_search.lower() in c["title"].lower()]
#     for chat in filtered:
#         if st.button(f"💬 {chat['title']}", key=chat["id"], use_container_width=True):
#             st.session_state.current_chat = chat["id"]


# # ================= Main =================
# col_header, col_signout = st.columns([8, 1])
# with col_header:
#     st.markdown("## ⚖️ Judiciary GPT")
# with col_signout:
#     st.button("🚪 Sign Out", use_container_width=True)

# st.divider()

# current_chat = get_current_chat()
# if current_chat:
#     for msg in current_chat["messages"]:
#         if msg["sender"] == "user":
#             st.markdown(
#                 f"""
#                 <div style="text-align:right; background:rgba(59,130,246,0.2);
#                             padding:10px 14px; border-radius:12px; margin:6px 0;
#                             color:white; max-width:70%; margin-left:auto;">
#                     {msg["content"]}
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
#         else:
#             st.markdown(
#                 f"""
#                 <div style="text-align:left; background:rgba(255,255,255,0.08);
#                             padding:10px 14px; border-radius:12px; margin:6px 0;
#                             color:white; max-width:70%;">
#                     {msg["content"]}
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
# else:
#     st.info("Welcome back! Start a new conversation or select one from the sidebar.")

# st.divider()


# # ================= Bottom Chatbox =================
# if st.session_state.attached_files:
#     st.markdown("**📎 Attached Files:**")
#     for f in st.session_state.attached_files:
#         st.markdown(f"- 📄 {f.name} ({round(f.size/1024,1)} KB)")

# chat_col1, chat_col2, chat_col3 = st.columns([0.12, 5, 0.6], vertical_alignment="center")

# with chat_col1:
#     if st.button("➕", help="Add options"):
#         st.session_state.show_add_options = not st.session_state.show_add_options

# with chat_col2:
#     st.text_area(
#         "Message box",
#         key="input_message",
#         placeholder="✍️ Message Judiciary GPT...",
#         height=70,
#         label_visibility="collapsed",
#     )

# with chat_col3:
#     st.button("📨 Send", use_container_width=True, help="Send message")


# # Dropdown options
# if st.session_state.show_add_options:
#     st.divider()
#     uploaded = st.file_uploader("📄 Attach File", type=["pdf", "docx", "txt", "png", "jpg"])
#     if uploaded:
#         st.session_state.attached_files.append(uploaded)

#     st.checkbox("🌐 Enable Web Search", key="is_web_search")
import streamlit as st
import datetime
import uuid

st.set_page_config(page_title="Judiciary GPT", layout="wide")

# ================= Custom CSS =================
st.markdown(
    """
    <style>
    /* Remove top padding so page starts right below navbar */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    body {
        background-color: #0e1117;
        color: white;
    }
    /* Chat bubbles */
    .user-msg {
        text-align: right;
        background: rgba(59,130,246,0.2);
        padding: 10px 14px;
        border-radius: 12px;
        margin: 6px 0;
        color: white;
        max-width: 70%;
        margin-left: auto;
    }
    .assistant-msg {
        text-align: left;
        background: rgba(255,255,255,0.08);
        padding: 10px 14px;
        border-radius: 12px;
        margin: 6px 0;
        color: white;
        max-width: 70%;
    }
    /* Buttons */
    .btn-signout {
        background: rgba(255,255,255,0.1);
        color: white;
        padding: 8px 14px;
        font-size: 13px;
        width: 100%;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.2s;
    }
    .btn-signout:hover {
        background: rgba(255,255,255,0.2);
    }
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
if "chat_search" not in st.session_state:
    st.session_state.chat_search = ""


# ================= Sidebar =================
with st.sidebar:
    st.markdown("### 👤 User Name")

    if st.button("➕ New Chat", use_container_width=True):
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
col_header, col_signout = st.columns([8, 1])
with col_header:
    st.markdown("## ⚖️ Judiciary GPT")
with col_signout:
    st.markdown('<button class="btn-signout">🚪 Sign Out</button>', unsafe_allow_html=True)

st.divider()

current_chat = next((c for c in st.session_state.chats if c["id"] == st.session_state.current_chat), None)
if current_chat:
    for msg in current_chat["messages"]:
        if msg["sender"] == "user":
            st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-msg'>{msg['content']}</div>", unsafe_allow_html=True)
else:
    st.info("Welcome back! Start a new conversation or select one from the sidebar.")
