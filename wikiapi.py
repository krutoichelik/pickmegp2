from common import *
import logging
logger = logging.getLogger(__name__)

df = pd.read_csv("matches_dataset.csv")


def get_wiki_html(query):
    try:
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": 1,
            "format": "json",
            "formatversion": 2
        }

        headers = {"User-Agent": "begemotik228"}

        r = requests.get(
            url="https://en.wikipedia.org/w/api.php",
            params=search_params,
            headers=headers,
            timeout=10
        )

        data = r.json()

        title = data["query"]["search"][0]["title"]

        title_encoded = title.replace(" ", "_")

        url_html = f"https://en.wikipedia.org/api/rest_v1/page/html/{title_encoded}"

        html = requests.get(url_html, headers=headers, timeout=10).text
        match = re.search(r'established_in_(\d{4})', html)
        year = match.group(1)
        return 2023 - int(year)

    except:
        logger.exception("ошибка при получении года основания для '%s' из Wikipedia", query)
        return pd.NA

