import requests
from bs4 import BeautifulSoup

def fetch(url: str) -> str:
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    paragraphs = soup.find_all('p')
    second_paragraph = paragraphs[1].text
    return second_paragraph


if __name__ == "__main__":
    print(fetch("https://dev.qweather.com/en/help"))