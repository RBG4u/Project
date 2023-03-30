from model import Group, Comment, db, app


def query_groups():
    group_ids = db.session.query(Group.id_group).all()
    group_ids = [op.id_group for op in group_ids]
    return group_ids
    

if __name__ == '__main__':
    with app.app_context():
        query_groups()

