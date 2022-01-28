from flask import Flask, Response
from flask import request
import os
import fakeredis
#import redis

app = Flask(__name__)

#r = redis.from_url(os.environ.get("REDIS_URL"))
r = fakeredis.FakeStrictRedis()

@app.route('/')
def homepage():
    play_id = request.args.get('app_id')
    play_id = 'tech.jonas.travelbudget' if play_id is None else play_id

    return """
    <h1>Whats this app about</h1>
    <form action='/' method='get'>
      <input type='text' name='app_id'></input>
      <input type='submit'></input>
    </form>
    <img src="/png/{play_id}">
    """.format(play_id=play_id)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
