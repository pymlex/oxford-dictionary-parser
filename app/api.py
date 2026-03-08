from fastapi import APIRouter, Query
from app.fetcher import fetch_page
from app.parser import parse_html
from app.config import MAX_PAGES

router = APIRouter()

@router.get("/parse")
def parse(word: str = Query(...)):
	pages = []
	status, html = fetch_page(word, 1)
	if status != 200:
		return {"status": "error", "message": "not found", "results": []}
	parsed = parse_html(html)
	pages.extend(parsed.get("results", []))
	related = []
	for r in parsed.get("results", []):
		for rel in r.get("related_entries", []):
			href = rel.get("href", "")
			if "/definition/english/" in href:
				tail = href.rstrip("/").split("/")[-1]
				if "_" in tail:
					parts = tail.rsplit("_", 1)
					w = parts[0]
					idx = parts[1]
				else:
					w = tail
					idx = "1"
				related.append({"word": w, "page_index": idx, "href": href})
	seen = set()
	for rel in related:
		key = (rel["word"], rel["page_index"])
		if key in seen:
			continue
		seen.add(key)
		if len(pages) >= MAX_PAGES:
			break
		status, html = fetch_page(rel["word"], rel["page_index"])
		if status != 200:
			continue
		parsed2 = parse_html(html)
		for e in parsed2.get("results", []):
			e["page_index"] = int(rel["page_index"])
			pages.append(e)
	return {
		"status": "ok",
		"word": word,
		"pages_found": len(pages),
		"results": pages
	}