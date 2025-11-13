import requests


url = 'http://localhost:9696/predict'


client = {
    "engine_rpm": 950,
    "fuel_pressure": 13.1,
    "lub_oil_temp": 66.7
}

response = requests.post(url, json=client)
predictions = response.json()


print(predictions)
if predictions['condition']:
    print('Engine condition is GOOD')
else:
    print('Engine condition is BAD')