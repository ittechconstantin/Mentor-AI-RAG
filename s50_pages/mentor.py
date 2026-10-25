import streamlit as st
from comun import api


st.title("🧭 Mentorul tau de cariera IT")
if "messages" not in st.session_state:
    st.session_state.messages = []


def arata_apeluri(apeluri):
    if apeluri:
        with st.expander("📚 Surse - ghidurile gasite"):
            for a in apeluri:
                st.caption(a["rezultat"])


for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        arata_apeluri(m.get("apeluri"))


mesaj = st.chat_input("Intreaba-ma despre cariera in IT...")

if mesaj:
    with st.chat_message("user"):
        st.markdown(mesaj)

    istoric = []
    for m in st.session_state.messages:
        istoric.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Ma gandesc ..."):
            ok, rezultat = api("POST", "/chat", json={"mesaj": mesaj, "istoric":istoric}, timeout = 400)
        if not ok:
            st.error(rezultat)
            st.stop()
        st.markdown(rezultat["raspuns"])
        arata_apeluri(rezultat["apeluri"])
    st.session_state.messages.append({"role": "user", "content": mesaj})
    st.session_state.messages.append({"role":"assistant", "content": rezultat["raspuns"], "apeluri": rezultat["apeluri"]})

if st.session_state.messages and st.sidebar.button("Conversatie noua"):
    st.session_state.messages = []
    st.rerun()
