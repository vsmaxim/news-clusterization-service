from datetime import datetime, timedelta
from typing import List

import vk_api

from news_parser.parser.config import config


vk_session = vk_api.VkApi(config['vk_api']['username'], config['vk_api']['password'])
vk_session.auth()

vk = vk_session.get_api()

def get_latest_posts_links(group_id: int, days_count: int) -> List[str]:
    current_offset = 0
    max_wall_count = 100
    current_date = datetime.now()
    end_date = current_date - timedelta(days=days_count)

    result_links = []

    while current_date > end_date:
        result = vk.wall.get(owner_id=-group_id, count=100, offset=current_offset)
        
        result_links.extend([
            attachment['link']['url'] 
            for item in result['items']
            for attachment in item.get('attachments', []) 
            if attachment['type'] == 'link'
        ])

        last_item = result['items'][-1]
        current_date = datetime.fromtimestamp(last_item['date'])
        current_offset += max_wall_count

    return result_links
