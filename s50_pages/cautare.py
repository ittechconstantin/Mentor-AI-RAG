import streamlit as st
from comun import api

st.title("🔎 Cautare in ghiduri")
intrebare = st.text_input("Intrebare")
n = st.slider("Cate ghiduri", min_value=1, max_value=5, value=2)

if intrebare:
    ok, rezultate = api("GET", "/cauta", params={"intrebare": intrebare, "n": n}, timeout=30)
    if not ok:
        st.error(rezultate)
        st.stop()

    for r in rezultate:
        with st.container(border=True):
            st.subheader(r["titlu"])
            st.caption(f"Distanta: {r['distanta']:.4f}")
            st.write(r["text"])
