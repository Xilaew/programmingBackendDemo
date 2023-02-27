import requests
payload = {'key':'BB', 'value':'Gewinner'}
r = requests.post('https://codingschooldemo.herokuapp.com/submit', data=payload)
print(r.text)