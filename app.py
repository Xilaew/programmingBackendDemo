from flask import Flask, Response
from flask import request, redirect, url_for
import os
import redis
#import fakeredis
import json

app = Flask(__name__)

r = redis.from_url(os.environ.get("REDIS_URL"))
#r = fakeredis.FakeStrictRedis()


def store(key, value):
    r.set(key,value)


def get(key):
    result = r.get(key)
    if type(result) == bytes:
        return result.decode("utf-8")
    else:
        return result


@app.route('/', methods = ['GET'])
def homepage():
    return """
    <html>
    <head>
    <title>sink ships</title>
    </head>
    <body>
    <h1>An input form</h1>
    <form action='/submit' method='post'>
      <label>key</label><input type='text' name='key'></input>
      <label>value</label><input type='text' name='value'></input>
      <input type='submit'></input>
    </form>
    <img src="https://api.thecatapi.com/v1/images/search?format=src">
    </body>
    </html>
    """


@app.route('/submit', methods = ['POST'])
def submit():
    key = request.form['key']
    value = request.form['value']
    previous = get(key)
    store(key,value)
    result = {"previous": previous, "key": key, "value": value}
    return json.dumps(result)


@app.route('/judge', methods = ['GET'])
def judge():
    result = ""
    cursor = '0'
    while cursor != 0:
        cursor, keys = r.scan(cursor=cursor)
        values = r.mget(*keys)
        for (key, value) in (zip(keys, values)):
            result += "<tr><td>{key}</td><td>{value}</td></tr>".format(key=key.decode("utf-8"), value=value.decode("utf-8"))
    result = "<table>{result}</table>".format(result=result)
    return result


app.route('/clear', methods = ['POST'])
def post_clear():
    r.flushdb()
    return redirect(url_for(judge))


app.route('/clear', methods = ['GET'])
def get_clear():
    return app.send_static_file()



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
