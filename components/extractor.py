import os
import json

DATA_DIR = "/Users/macos/PycharmProjects/tiktok_influencers_scraper/data"

list_of_json = os.listdir(DATA_DIR)


for l in list_of_json:
    with open(DATA_DIR + "/" + l, 'r') as json_file:
        data = json.load(json_file)
        i = 0