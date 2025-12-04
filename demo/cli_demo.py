import argparse
from pprint import pprint
from src.main import create_app


def cmd_ingest(app, mode: str):
    graph = app.state.news_graph
    result = graph.invoke({"mode": mode})
    print(f"Ingested: {len(result.get('parsed_articles', []))}, Unique: {len(result.get('unique_articles', []))}")


def cmd_query(app, query: str, top_k: int):
    graph = app.state.query_graph
    result = graph.invoke({"query": query, "top_k": top_k})
    for i, r in enumerate(result.get("search_results", []), 1):
        art = r["article"]
        print(f"{i}. {art['title']} [{art.get('category')}] - score={r.get('score'):.3f}")
        print(f"   {art['source']} | {art['published_at']} | {art['url']}")
        print(f"   {r.get('explanation')}")


def cmd_stats(app):
    pprint(app.state.db.stats())


def cmd_article(app, article_id: str):
    pprint(app.state.db.get_article(article_id))


def cmd_entities(app):
    pprint(app.state.db.list_entities())


def main():
    parser = argparse.ArgumentParser(description="Financial News Intelligence CLI Demo")
    sub = parser.add_subparsers(dest="cmd")

    p_ingest = sub.add_parser("ingest-mock")
    p_ingest = sub.add_parser("ingest-rss")

    p_query = sub.add_parser("query")
    p_query.add_argument("text")
    p_query.add_argument("--top_k", type=int, default=10)

    sub.add_parser("stats")

    p_article = sub.add_parser("article")
    p_article.add_argument("id")

    sub.add_parser("entities")

    args = parser.parse_args()
    app = create_app()

    if args.cmd == "ingest-mock":
        cmd_ingest(app, "ingest_mock")
    elif args.cmd == "ingest-rss":
        cmd_ingest(app, "ingest_rss")
    elif args.cmd == "query":
        cmd_query(app, args.text, args.top_k)
    elif args.cmd == "stats":
        cmd_stats(app)
    elif args.cmd == "article":
        cmd_article(app, args.id)
    elif args.cmd == "entities":
        cmd_entities(app)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
