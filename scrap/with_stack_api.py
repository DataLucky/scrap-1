import json

from stackapi import StackAPI

SITE = StackAPI('stackoverflow')
questions = SITE.fetch("questions")


def extract_questions():
    with open("stack.json", "w") as file:
        file.write(json.dumps(questions['items']))


def extract_users():
    with open("stack.json", "w") as file:
        file.write(json.dumps(questions['items']))
