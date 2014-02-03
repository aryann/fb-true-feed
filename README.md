fb-true-feed
============

This is a collection of scripts for viewing the status updates of
one's Facebook friends in reverse chronological order without any
filtering.

Before running this, ensure that requests is installed:

    $ pip install requests

Once requests is installed, run:

    $ python fetch_status_updates.py ACCESS_TOKEN DESTINATION_DIR
    $ python print_top_posts.py $(ls DESTINATION_DIR | sort | tail -n 1) 100

The first command fetches the latest data from your friends'
walls. The second command sorts the data by date and prints the 100
latest items.

The easiest way to get an ACCESS_TOKEN is to use Facebook's Graph
Explorer (https://developers.facebook.com/tools/explorer/).
