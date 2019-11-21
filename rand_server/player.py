import requests
import json
from datetime import datetime
import time
import threading 
import random
import sys

class Player:
    def __init__(self, phrases, server_url, author):
        self.phrases = phrases
        self.server_url = server_url
        self.last_check = str(datetime.utcnow())
        self.author = author
    
    def say(self):
        text = random.choice(self.phrases)
        obj = {'author' : self.author, 'text' : text}
        result = requests.post(self.server_url + '/Send', json.dumps(obj))
        return result.ok

    def print_feed(self):
        while True:
            time.sleep(2)
            obj = {'from' : str(self.last_check)}
            self.last_check = str(datetime.utcnow())
            result = requests.post(self.server_url + '/Feed', json.dumps(obj))
            new_messages =  json.loads(result.text)["messages"]
            for msg in new_messages:
                print("{0}: {1}".format(msg["author"], msg["text"]))

with open(sys.argv[3]) as f:
    phrases = f.readlines()

player = Player(phrases, sys.argv[1], sys.argv[2])
thread = threading.Thread(target = player.print_feed)
thread.start()

while True:
    time.sleep(random.randint(5,10))
    player.say()
