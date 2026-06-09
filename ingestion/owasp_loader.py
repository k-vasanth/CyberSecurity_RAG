import requests
import json
from bs4 import BeautifulSoup
from config import OWASP_DATA_PATH


class OWASPLoader:
    def __init__(self):
        self.sources = [
    "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html",
    "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html",
    "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html",
    "https://owasp.org/www-community/attacks/xss/",
    "https://owasp.org/www-community/attacks/sql_injection",
    "https://owasp.org/www-community/attacks/authentication_bypass"
    ]
        

    def fetch_page(self, url):
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )
            if response.status_code == 200:
                return response.text
            return None
        except Exception as error:
            print(f"Error fetching {url}: {error}")
            return None

    def parse_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        lines = []
        bad_words = [
            "translation",
            "translated by",
            "contributors",
            "project sponsors",
            "twitter",
            "pdf",
            "pptx",
            "copyright",
            "cookie",
            "privacy policy",
            "email protected"
        ]
        for line in text.split("\n"):
            line = line.strip()
            if len(line) < 40:
                continue
            if any(word in line.lower() for word in bad_words):
                continue
            lines.append(line)
        return "\n".join(lines)

    def load(self):
        OWASP_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = json.dumps(self.sources, indent=2)
        with open(OWASP_DATA_PATH, "w", encoding="utf-8") as file:
            file.write(data)

        documents = []
        for source in self.sources:
            print(type(source))
            print(f"Fetching: {source}")
            html = self.fetch_page(source)
            if not html:
                continue
            text = self.parse_html(html)
            documents.append({
                "source": source,
                "title": source,
                "content": text,
                "url": source
            })
        return documents

