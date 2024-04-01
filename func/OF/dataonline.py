from duckduckgo_search import DDGS
import json
from itertools import islice
import time
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def summarize_paragraph(paragraph: str, num_sentences: int = 3) -> str:
    """
    Summarizes the given paragraph using LexRank algorithm.

    Args:
    - paragraph (str): The paragraph of text to be summarized.
    - num_sentences (int): The number of sentences in the summary. Defaults to 3.

    Returns:
    - str: The summarized text.
    """
    parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)

    summarized_text = "\n".join(str(sentence) for sentence in summary)
    return summarized_text


def online_scraper(query: str, num_results: int = 2) -> list:
    """
    Scrapes online content using DuckDuckGo search and summarizes it.

    Args:
    - query (str): The search query.
    - num_results (int): The number of search results to consider. Defaults to 2.

    Returns:
    - list: A list of dictionaries containing 'url' and 'summary' for each result.
    """
    DUCKDUCKGO_MAX_ATTEMPTS = 3

    search_results = []
    attempts = 0

    while attempts < DUCKDUCKGO_MAX_ATTEMPTS:
        if not query:
            return search_results

        results = DDGS().text(query)
        search_results = list(islice(results, num_results))

        if search_results:
            break

        time.sleep(1)
        attempts += 1

    all_data = []
    for result in search_results:
        url = result.get("url", "")
        paragraph = result.get("body", "")
        summary = summarize_paragraph(paragraph)
        all_data.append({"url": url,"paragraph": paragraph, "summary": summary})

    return all_data

