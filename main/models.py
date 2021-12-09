import requests

from database import db


class Link(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(128), unique=False, nullable=False)
    description = db.Column(db.String(128), unique=False, nullable=False)
    status_code = db.Column(db.Integer, unique=False, nullable=True)

    def __init__(self, link, description, status_code):
        self.link = link
        self.description = description
        self.status_code = status_code

    def __init__(self, link, description):
        self.link = link
        self.description = description
        self.status_code = None




class LinkStatusCodeIn:
    status_code = 200

    def __init__(self, link: str):
        try:
            self.status_code = requests.get(link).status_code
        except requests.ConnectionError:
            self.status_code = 404
