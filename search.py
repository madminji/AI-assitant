import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def search(content: str):
    
    params = {
    "engine": "bing",
    "q": content,
    "api_key": "61bdf2145620795a264bce9b27cfda77db70cd7f59a35ae105391f436264acf7"   #API Key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" in results:
        # 获取第一条搜索结果的 snippet 字段
        search_result = results["organic_results"][0]
        snippet = search_result.get("snippet", "")
        return f"Please answer {content} based on the search result:\n\n{snippet}"

    return f"No search results found for: {content}"

# if __name__ == "__main__":
#     search("Sun Wukong")