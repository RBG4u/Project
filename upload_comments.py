from model import Comment, db, app
import csv


def save_comments(comments):
    db.session.bulk_insert_mappings(Comment, comments)
    db.session.commit()


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['id_post', 'text', 'id_group_from']
        reader = csv.DictReader (f, fields, delimiter=';')
        comments_data = []
        for row in reader:
            comments_data.append(row)
        return comments_data


if __name__ == '__main__':
    with app.app_context():
        comments = read_csv('list_comments.csv')
        save_comments(comments)
