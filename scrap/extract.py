from bs4 import BeautifulSoup

import requests

from scrap.utils import get_question, get_post_summary_meta, get_post_summary

questions_url = "https://stackoverflow.com/questions/"
questions_resolved_url = "https://stackoverflow.com/questions?tab=newest&page=1590453"


def extract_questions(url):
    responses = requests.get(url)
    soup = BeautifulSoup(responses.text, "html.parser")
    questions = soup.select("#questions")[0].select(".s-post-summary")
    results = []
    for question in questions:
        question_entry = {
            "text": get_question(question),
            "meta_summary": get_post_summary_meta(question),
            "summary": get_post_summary(question)
        }
        results.append(question_entry)
    return results


results = extract_questions(questions_resolved_url)
results.append(*results)

print(results[0])
