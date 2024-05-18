from functools import lru_cache
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from googlesearch import search
import requests
from langchain.tools import tool

@lru_cache(maxsize=128)
def fetch_content_cached(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
    return None

@lru_cache(maxsize=128)
def GoogleSearch(q):
    results = list(search(q, num=5, stop=5, pause=2))
    summaries = []
    for url in results:
        content = fetch_content_cached(url)
        if content:
            parser = HtmlParser.from_string(content, url, Tokenizer("english"))
            summarizer = LexRankSummarizer()
            summary = summarizer(parser.document, 3)  # Summarize with 3 sentences
            summaries.append("\n".join(str(sentence) for sentence in summary))
    return summaries

class SearchTools():
    @tool("Searches the internet and summarizes the results")
    def search_internet(paragraph: str, num_sentences: int = 3) -> str:
        """
        Summarizes the search results for the given query using LexRank algorithm.

        Args:
        - paragraph (str): The query to search for.
        - num_sentences (int): The number of sentences in each summary. Defaults to 3.

        Returns:
        - str: The summarized text.
        """
        summaries = GoogleSearch(paragraph)
        summarized_text = "\n\n".join(summaries)
        return summarized_text
