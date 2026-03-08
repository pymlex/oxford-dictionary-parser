from fake_useragent import UserAgent
import requests

ua = UserAgent()

def fetch_page(word, page_index):
	headers = {"User-Agent": ua.random}
	url = (
		"https://www.oxfordlearnersdictionaries.com/definition/english/"
		+ word
		+ "_"
		+ str(page_index)
	)
	r = requests.get(url, headers=headers, timeout=10)
	return r.status_code, r.text