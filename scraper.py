"""
Web scraper gratuit pour récupérer des données d'entraînement depuis internet.
Utilise BeautifulSoup et requests sans service payant.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from urllib.parse import urljoin, quote
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """Scraper web gratuit pour récupérer des données d'entraînement."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def search_google(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Recherche sur Google et retourne les résultats.
        Note: Utilise une approche simple sans API payante.
        """
        results = []
        try:
            # Utiliser DuckDuckGo comme alternative gratuite
            url = f"https://duckduckgo.com/html/?q={quote(query)}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a", class_="result__url")

            for link in links[:num_results]:
                href = link.get("href")
                if href and href.startswith("http"):
                    results.append({"url": href, "title": link.text})

            logger.info(f"Trouvé {len(results)} résultats pour '{query}'")
            return results

        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {e}")
            return []

    def scrape_url(self, url: str) -> Dict:
        """
        Scrape le contenu d'une URL.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.content, "html.parser")

            # Extraire le titre
            title = ""
            if soup.title:
                title = soup.title.string

            # Extraire le texte principal
            # Supprimer les scripts et styles
            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)

            return {
                "url": url,
                "title": title,
                "content": text[:5000],  # Limiter à 5000 caractères
                "success": True,
            }

        except Exception as e:
            logger.error(f"Erreur lors du scraping de {url}: {e}")
            return {
                "url": url,
                "title": "",
                "content": "",
                "success": False,
                "error": str(e),
            }

    def scrape_topic(self, topic: str, num_pages: int = 5, code_only: bool = False) -> List[Dict]:
        """
        Scrape plusieurs pages sur un sujet donné.
        Si code_only=True, scrape uniquement du code (GitHub, etc.)
        """
        logger.info(f"Scraping du sujet: {topic} (code_only={code_only})")
        all_data = []

        if code_only:
            # Scraper GitHub pour du code
            search_results = self.scrape_github(topic, num_results=num_pages)
        else:
            # Rechercher les URLs normales
            search_results = self.search_google(topic, num_results=num_pages)

        # Scraper chaque URL (sans délai pour aller au plus rapide)
        for idx, result in enumerate(search_results):
            logger.info(f"Scraping {idx + 1}/{len(search_results)}: {result['url']}")
            content = self.scrape_url(result["url"])
            if content["success"]:
                all_data.append(content)

        logger.info(f"Scraping terminé: {len(all_data)} pages récupérées")
        return all_data

    def extract_code_examples(self, content: str) -> List[str]:
        """
        Extrait les exemples de code du contenu.
        """
        soup = BeautifulSoup(content, "html.parser")
        code_blocks = soup.find_all(["code", "pre"])
        examples = [block.get_text() for block in code_blocks]
        return examples

    def scrape_github(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Scrape les résultats GitHub pour un sujet.
        """
        results = []
        try:
            url = f"https://github.com/search?q={quote(query)}&type=repositories"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            repos = soup.find_all("a", class_="v-align-middle")

            for repo in repos[:num_results]:
                href = repo.get("href")
                if href:
                    results.append({
                        "url": urljoin("https://github.com", href),
                        "name": repo.text.strip(),
                    })

            logger.info(f"Trouvé {len(results)} repositories GitHub")
            return results

        except Exception as e:
            logger.error(f"Erreur lors du scraping GitHub: {e}")
            return []

    def scrape_stackoverflow(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Scrape les questions/réponses Stack Overflow.
        """
        results = []
        try:
            url = f"https://stackoverflow.com/search?q={quote(query)}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            questions = soup.find_all("a", class_="s-link")

            for question in questions[:num_results]:
                href = question.get("href")
                if href and href.startswith("/questions/"):
                    results.append({
                        "url": urljoin("https://stackoverflow.com", href),
                        "title": question.text.strip(),
                    })

            logger.info(f"Trouvé {len(results)} questions Stack Overflow")
            return results

        except Exception as e:
            logger.error(f"Erreur lors du scraping Stack Overflow: {e}")
            return []


def main():
    """Test du scraper."""
    scraper = WebScraper()

    # Exemple: scraper sur "Unity game development"
    topic = "Unity game development best practices"
    data = scraper.scrape_topic(topic, num_pages=3)

    for item in data:
        print(f"\n{'='*60}")
        print(f"URL: {item['url']}")
        print(f"Titre: {item['title']}")
        print(f"Contenu (premiers 200 chars): {item['content'][:200]}...")


if __name__ == "__main__":
    main()
