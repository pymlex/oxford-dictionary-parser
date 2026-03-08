from fake_useragent import UserAgent
import requests

ua = UserAgent()

def _user_agent():
	return ua.random

def fetch_page(word, page_index):
	headers = {"User-Agent": _user_agent()}
	url1 = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}_{page_index}"
	r = requests.get(url1, headers=headers, timeout=10)
	if r.status_code == 200 and len(r.text) > 200:
		return r.status_code, r.text
	url2 = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
	r2 = requests.get(url2, headers=headers, timeout=10)
	return r2.status_code, r2.text