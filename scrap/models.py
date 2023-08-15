class Summary:
    def __init__(self, votes: int, answers: int, views: int):
        self.votes = votes
        self.answers = answers
        self.views = views


class Post:
    def __init__(self, title, summary: Summary):
        self.title = title
        self.summary = summary
