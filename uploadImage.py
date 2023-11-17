import requests
from datetime import datetime

filename = 'image.png'
bucketName = 'agribot-guava'
datetime = datetime.now()

with open(filename, 'rb') as f:
    data = f.read()
res = requests.put(url='https://0je3rk9t12.execute-api.us-east-1.amazonaws.com/dev/agribot-guava/'+f'{datetime}'+'.jpg',
                    data=data,
                    headers={'Content-Type': 'application/octet-stream'})