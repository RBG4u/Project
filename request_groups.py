import requests
import config


def take_groups(token, version, group_ids):
    all_groups = []

    response = requests.get('https://api.vk.com/method/groups.getById', 
                            params={
                                'access_token':token,
                                'v':version,
                                'group_ids':group_ids
                            })

    groups = response.json()['response']

    for group in groups:
        data = {'id_group': group['id'], 
                'name': group['name']}
        all_groups.append(data)
    return all_groups

if __name__ == "__main__":
    take_groups(config.VK_TOKEN, config.VK_API_VERSION, config.GROUP_IDS)