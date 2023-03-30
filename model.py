from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_group = db.Column(db.Integer, unique=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f"Group {self.id}, {self.name}"
    

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_post = db.Column(db.Integer)
    text = db.Column(db.String)

    id_group_from = db.Column(db.Integer, db.ForeignKey('group.id_group'),
        nullable=False)
    group = db.relationship('Group',
        backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f"Comment {self.id}, {self.id_group_from}, {self.text}"
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
