from typing import Dict, List

from bs4 import Tag, ResultSet


def get_question(question: Tag) -> str:
    return question.select_one(".s-post-summary--content-title").text


def get_post_summary(question: Tag) -> dict[str, str]:
    def get_entry(summaries: ResultSet[Tag], index: int):
        return summaries[index].select_one(".s-post-summary--stats-item-number").text

    results = {}
    summaries = question.select_one(".s-post-summary--stats").select("div")
    results['votes'] = get_entry(summaries, 0)
    results['answers'] = get_entry(summaries, 1)
    results['has_accepted_answer'] = "has-accepted-answer" in summaries[1].get("class", "")
    results['views'] = get_entry(summaries, 2)
    return results


def get_post_summary_meta(question: Tag) -> list[str]:
    tags = question.select_one(".s-post-summary--content").select_one("ul").select("li")
    tags_result = [tag.text for tag in tags]
    return tags_result
