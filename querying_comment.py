from model import Group, Comment, db, app


def query_comment(id_group):
    text_comments = []
    comments = Comment.query.filter_by(id_group_from=id_group).order_by(Comment.text).all()
    for comment in comments:
        text_comments.append({'group_id':comment.id_group_from,
                              'text':comment.text})
    return text_comments


if __name__ == '__main__':
    with app.app_context():
        id = '26464472'
        commen = query_comment(id)
        print(commen)



