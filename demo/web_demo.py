import streamlit as st
from src.main import create_app

st.set_page_config(page_title="Financial News Intelligence", layout="wide")
app = create_app()

st.title("Financial News Intelligence - Demo")

col1, col2 = st.columns(2)
with col1:
    if st.button("Ingest Mock Dataset"):
        res = app.state.news_graph.invoke({"mode": "ingest_mock"})
        st.success(f"Ingested {len(res.get('parsed_articles', []))} articles; Unique {len(res.get('unique_articles', []))}")
with col2:
    if st.button("Ingest RSS Feeds"):
        res = app.state.news_graph.invoke({"mode": "ingest_rss"})
        st.success(f"Ingested {len(res.get('parsed_articles', []))} RSS items; Unique {len(res.get('unique_articles', []))}")

q = st.text_input("Query", "HDFC Bank news")
top_k = st.slider("Top K", 1, 20, 10)
if st.button("Search"):
    res = app.state.query_graph.invoke({"query": q, "top_k": top_k})
    for r in res.get("search_results", []):
        art = r["article"]
        with st.expander(f"{art['title']} [{art.get('category')}] - score={r.get('score'):.3f}"):
            st.write(art["content"]) 
            st.caption(f"{art['source']} | {art['published_at']} | {art['url']}")
            st.info(r.get("explanation"))

st.subheader("Stats")
st.json(app.state.db.stats())
