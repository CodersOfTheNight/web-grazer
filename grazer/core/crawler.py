import requests
import re
import logging

from collections import deque
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_session():
    return requests.Session()


def read_page(session, url):
    raw = session.get(url).text
    return BeautifulSoup(raw, "html.parser")


def extract_links(page):
    return [a.get("href") for a in page.find_all("a")]


def trim_link(link, root):
    result = re.sub(root, "", link)
    if result.startswith("http"):
        # External link to another domain
        return None

    return result


def create(config):
    root = config.root
    start = config.start_page
    pages = config.pages
    session = get_session()

    queue = deque(["{0}/{1}".format(root, start)])
    visited = []

    while len(queue) > 0:
        link = queue.popleft()
        logger.info("Scrapping: {0}".format(link))
        try:
            data = read_page(session, link)
        except Exception as ex:
            logger.error(ex)
            visited.append(link)
            continue

        visited.append(link)

        for page in pages:
            if page.matches_link_pattern(link):
                for mapping in page.mappings:
                    for result in mapping.parse(data):
                        yield result, link

        links = map(lambda x: root + x,
                    filter(lambda x: x is not None,
                           [trim_link(l, root)
                            for l in extract_links(data)]))

        for link in links:
            if link not in visited:
                queue.append(link)
