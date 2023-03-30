from model import Group, db, app
from request_groups import take_groups
import config


def save_groups(dict_groups):
    for row in dict_groups:
        group_data = Group(id_group=row['id_group'], name=row['name'])
        db.session.add(group_data)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        groups = take_groups(config.VK_TOKEN, config.VK_API_VERSION, config.GROUP_IDS)
        save_groups(groups)
        