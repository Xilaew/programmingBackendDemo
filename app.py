from flask import Flask, Response
from flask import request, redirect, url_for
import os
import json

app = Flask(__name__)

if 'REDISCLOUD_URL' in os.environ:
    import redis    
    r = redis.from_url(os.environ['REDISCLOUD_URL'])
    print("Found redis at: " + os.environ['REDISCLOUD_URL'])
else:
    import fakeredis
    r = fakeredis.FakeStrictRedis()
    print("using Fakeredis")

def store(key, value):
    r.set(key, value)


def get(key):
    result = r.get(key)
    if type(result) == bytes:
        return result.decode("utf-8")
    else:
        return result


@app.route('/', methods=['GET'])
def homepage():
    return """
    <html>
    <head>
    <title>sink ships</title>
    </head>
    <body style="background-color: white;">
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


@app.route('/submit', methods=['POST'])
def submit():
    key = request.form['key']
    value = request.form['value']
    previous = get(key)
    store(key, value)
    result = {"previous": previous, "key": key, "value": value}
    return json.dumps(result)


def decode(redisvalue):
    if type(redisvalue) == bytes:
        return redisvalue.decode("utf-8")
    if redisvalue == None:
        return ""
    else:
        return redisvalue


def header(l):
    return "<th></th>" + "".join(["<th>{}</th>".format(i) for i in l])


def row(l, v):
    keys = ["{}{}".format(v, i) for i in l]
    values = r.mget(*keys)
    return "<tr><th>{v}</th>{content}</tr>".format(v=v, content="".join(["<td>{}</td>".format(decode(value)) for value in values]))


@app.route('/judge', methods=['GET'])
def judge():
    l = [str(chr(x)) for x in range(ord('A'), ord('Z') + 1)]
    table1 = "<table><tr>{head}</tr>{body}</table>".format(head=header(l), body="".join([row(l, v) for v in l]))
    result = ""
    cursor = '0'
    while cursor != 0:
        cursor, keys = r.scan(cursor=cursor)
        if len(keys) <= 0:
            break
        values = r.mget(*keys)
        for (key, value) in (zip(keys, values)):
            result += "<tr><td>{key}</td><td>{value}</td></tr>".format(key=key.decode("utf-8"), value=value.decode("utf-8"))
    result = "{table1}<hr><table>{result}</table>".format(table1=table1, result=result)
    return result


@app.route('/clear', methods=['POST'])
def post_clear():
    r.flushdb()
    return redirect(url_for('judge'))


@app.route('/clear', methods=['GET'])
def get_clear():
    return app.send_static_file("clear.html")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
