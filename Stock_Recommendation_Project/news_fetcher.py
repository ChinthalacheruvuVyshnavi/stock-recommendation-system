import requests
import urllib.parse
import xml.etree.ElementTree as ET


def get_news(company_name, limit=8):
    try:
        query = urllib.parse.quote(company_name + " stock market")
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        headlines = []
        seen = set()

        for item in items:
            title_element = item.find("title")
            if title_element is not None and title_element.text:
                title = title_element.text.strip()

                # remove trailing source after " - "
                cleaned = title.split(" - ")[0].strip()

                if cleaned and cleaned.lower() not in seen:
                    headlines.append(cleaned)
                    seen.add(cleaned.lower())

            if len(headlines) >= limit:
                break

        return headlines

    except Exception:
        return []