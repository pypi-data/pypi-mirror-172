from requests import get
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse

def Search(query : str, headers: dict = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"}):
    results: list = []

    page_source: str = get(f"https://www.google.com/search?q={quote(query)}&num=20&hl=en", headers=headers).text

    try:
        parser: list = BeautifulSoup(page_source, "html.parser").findAll("div", attrs={"class" : "yuRUbf"})
    except AttributeError:
        return dict(message = "No Result Found!")

    if parser:
        for i in parser:
            results.append(dict(url = i.find("a").get("href"), netloc = urlparse(i.find("a").get("href")).netloc, title = i.find("h3", attrs={"class" :"LC20lb MBeuO DKV0Md"}).text))

    if results:
        return results

    return dict(message = "No Result Found!")