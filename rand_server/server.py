from klein import run, route
from datetime import datetime
import json
from threading import Lock
import sys

lock = Lock()
messages = []

@route('/Feed', methods=['POST'])
def feed(request):
    global messages
    with lock:
        content = json.loads(request.content.read())
        new_messages = filter(lambda x: x["time"] > content["from"], messages)
    return json.dumps({'messages' : list(new_messages)})

@route('/Send', methods=['POST'])
def send(request):
    content = json.loads(request.content.read())
    global messages
    with lock:
        if len(messages) > 1000:
            messages = messages[-1000:]
        messages.append({'text' : content['text'], 'author' : content['author'], 'time' : str(datetime.utcnow())})
    return True

run("localhost", int(sys.argv[1]))
