import streamlit as st
from history import get_history, clear_history

st.title("🕘 Search History")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first")

else:
    history = get_history(st.session_state.user)

    if not history:
        st.info("No history yet")

    for query, time in history:
        st.write(f"🔍 {query} — {time}")

    if st.button("🗑️ Clear History"):
        clear_history(st.session_state.user)
        st.success("History cleared")