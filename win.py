import requests
headers = {'User-Agent': 'Mozilla/5.0'}
payload = {'key':'test', 'value':'123456'}
r = requests.post('https://codingschooldemo.herokuapp.com/submit', headers=headers, data=payload)
print(r)