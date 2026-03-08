from bs4 import BeautifulSoup
from urllib.parse import urljoin

def _get_text(el):
	if not el:
		return None
	return " ".join(el.get_text(separator=" ").split()).strip()

def _extract_phon(ph_div):
	if not ph_div:
		return None
	audio = None
	phon = None
	audio_btn = ph_div.find(class_="sound")
	if audio_btn:
		audio = audio_btn.get("data-src-mp3") or audio_btn.get("data-src-ogg")
	phon_span = ph_div.find(class_="phon")
	if phon_span:
		phon = phon_span.get_text().strip()
	return {"text": phon, "audio": audio}

def parse_html(html, base_url="https://www.oxfordlearnersdictionaries.com"):
	soup = BeautifulSoup(html, "lxml")
	results = []
	for entry in soup.select("div.entry"):
		entry_id = entry.get("id")
		head = entry.find("h1", class_="headword")
		pos = entry.find("span", class_="pos")
		phon_br = entry.find(class_="phons_br")
		phon_us = entry.find(class_="phons_n_am")
		verb_forms = []
		vf_table = entry.select_one("table.verb_forms_table")
		if vf_table:
			for tr in vf_table.select("tr.verb_form"):
				cells = tr.find_all("td")
				if not cells:
					continue
				form = " ".join(cells[0].get_text(strip=True).split())
				phon = cells[1].get_text(strip=True) if len(cells) > 1 else None
				verb_forms.append({"form": form, "phon": phon})
		senses = []
		for sh in entry.select("span.shcut-g"):
			h2 = sh.find("h2", class_="shcut")
			group = _get_text(h2) or None
			for li in sh.select("li.sense"):
				cefr = li.get("cefr")
				grammar = _get_text(li.find(class_="grammar"))
				def_el = li.find(class_="def")
				def_text = _get_text(def_el)
				examples = [ _get_text(x) for x in li.select(".examples .x") ]
				extra = []
				collapse = li.find(class_="collapse")
				if collapse:
					for ex in collapse.select(".examples .unx"):
						extra.append(_get_text(ex))
				senses.append({
					"group": group,
					"cefr": cefr,
					"grammar": grammar,
					"definition": def_text,
					"examples": [e for e in examples if e],
					"extra_examples": [e for e in extra if e]
				})
		idioms = []
		for a in entry.select("a.Ref"):
			href = a.get("href") or ""
			txt = _get_text(a)
			if "idiom" in href or "idm" in href or "idiom" in txt.lower():
				idioms.append({"text": txt, "href": urljoin(base_url, href)})
		phrasals = []
		for a in entry.select("a"):
			href = a.get("href") or ""
			txt = _get_text(a)
			if "/definition/english/" in href and "pv" in href:
				phrasals.append({"text": txt, "href": urljoin(base_url, href)})
		related = []
		for a in soup.select("a.Ref"):
			href = a.get("href") or ""
			txt = _get_text(a)
			if "/definition/english/" in href:
				related.append({"text": txt, "href": urljoin(base_url, href)})
		origin = None
		for h in soup.find_all(["h2", "h3", "h4"]):
			if "origin" in h.get_text().lower():
				ns = h.find_next_sibling()
				origin = _get_text(ns)
				break
		res = {
			"entry_id": entry_id,
			"headword": _get_text(head),
			"part_of_speech": _get_text(pos),
			"phonetics": {
				"uk": _extract_phon(phon_br),
				"us": _extract_phon(phon_us)
			},
			"verb_forms": verb_forms,
			"senses": senses,
			"idioms": idioms,
			"phrasal_verbs": phrasals,
			"related_entries": related,
			"origin": origin
		}
		results.append(res)
	return {"word": results[0].get("headword") if results else None,
			"results": results}