from klein import run, route
from datetime import datetime
import json
from threading import Lock

lock = Lock()
messages = []

@route('/Feed', methods=['POST'])
def feed(request):
    global messages
    content = json.loads(request.content.read())
    new_messages = filter(lambda x: x["time"] > content["from"], messages)
    return json.dumps({'messages' : list(new_messages)})

@route('/Send', methods=['POST'])
def send(request):
    content = json.loads(request.content.read())
    global messages
    lock.acquire()
    try:
        if len(messages) > 1000:
            messages = messages[-1000:]
        messages.append({'text' : content['text'], 'author' : content['author'], 'time' : str(datetime.utcnow())})
    finally:
        lock.release()
    return True

run("localhost", 10000)
