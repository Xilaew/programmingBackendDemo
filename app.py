from flask import Flask, Response
from flask import request
import os
import redis
import fakeredis
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
    <h1>An input form</h1>
    <form action='/submit' method='post'>
      <label>key</label><input type='text' name='key'></input>
      <label>value</label><input type='text' name='value'></input>
      <input type='submit'></input>
    </form>
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

    value = request.form['value']
    previous = get(key)
    store(key,value)
    result = {"previous": previous, "key": key, "value": value}
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
