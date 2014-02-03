import heapq
import json
import os
import sys


def print_posts(posts):
    for time, data in heapq.nlargest(len(posts), posts):
        print '---'
        print 'time:', time
        print 'name:', data['from']['name'].encode('utf-8')
        print 'message:', data['message'].encode('utf-8')


def add_item(item, limit, heap):
    if len(heap) < limit:
        heap.append(item)
    else:
        heapq.heappushpop(heap, item)


if __name__ == '__main__':
    dir = sys.argv[1]
    limit = int(sys.argv[2])

    latest_statuses = []
    
    for friend_feed in os.listdir(dir):
        with open(os.path.join(dir, friend_feed)) as f:
            statuses = json.load(f)
            for status in statuses.get('data', []):
                add_item((status.get('updated_time'), status),
                         limit, latest_statuses)

    print_posts(latest_statuses)
