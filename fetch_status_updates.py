import json
import logging
import os
import requests
import sys
import time

_TIME_BETWEEN_RUNS_SEC = 120


def get_friends(access_token, logger):
    url = 'https://graph.facebook.com/me/friends'
    while True:
        response = requests.get(
            url,
            params={'access_token': access_token})
        if response.status_code != requests.codes.ok:
            logger.error('Received status code %s when listing friends: %s',
                         response.status_code, response.text)
            return

        data = response.json()
        for friend in data.get('data', []):
            yield friend['id']


        next_url = data.get('paging', {}).get('next')
        if next_url:
            url = next_url
        else:
            break


if __name__ == '__main__':
    logger = logging.getLogger(__file__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    access_token = sys.argv[1]
    base_dir = sys.argv[2]

    while True:
        epoch_ms = int(time.time() * 1000)
        dir = os.path.join(base_dir, str(epoch_ms))

        logger.info('Starting new run; data will be written to %s.', dir)
        os.mkdir(dir)
        
        friends = list(get_friends(access_token, logger))
        logger.info('%s friends found.', len(friends))

        for friend_id in friends:
            data_file = os.path.join(dir, friend_id)
            logger.info(
                'Fetching feed for friend %s; data will be written to %s.',
                friend_id, data_file)
            response = requests.get(
                'https://graph.facebook.com/{0}/statuses'.format(friend_id),
                params={'access_token': access_token})
            if response.status_code == requests.codes.ok:
                with open(data_file, 'w') as f:
                    f.write(response.text)
            else:
                logger.error('Received status code %s for friend %s: %s',
                             response.status_code, friend_id, response.text)

        logger.info('Done with run.')
        time.sleep(_TIME_BETWEEN_RUNS_SEC)

