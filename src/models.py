import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ.get(
    "DATABASE_URL") or "postgres://postgres:0000@localhost:5432/monk"

db = SQLAlchemy()


def create_all():
    db.create_all()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


imgtag = db.Table('imgtag',
    db.Column('image_id', db.Integer, db.ForeignKey('Image.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'))
)

class Image(db.Model):
    __tablename__ = 'Image'

    id = Column(Integer, primary_key=True)
    url = Column(String(120), nullable=False)
    name = Column(String(120), nullable=False)
    type = Column(String(120), nullable=False)
    tags = db.relationship('Tag', secondary=imgtag, backref='tag_images', lazy=True)

    def __init__(self, url, name, type):
        self.url = url
        self.name = name
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def addTag(self, tag):
        self.image_tags.append(tag)
        db.session.commit()

    def getTags(self):
        return [tag.format() for tag in self.image_tags]

    def format(self):
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name,
            'type': self.type
        }


class Tag(db.Model):
    __tablename__ = 'Tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    images = db.relationship('Image', secondary=imgtag, backref='image_tags', lazy=True)

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def addImage(self, image):
        self.tag_images.append(image)
        db.session.commit()

    def getImages(self):
        return self.tag_images

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }
