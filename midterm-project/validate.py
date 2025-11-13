import requests


url = 'http://10.1.1.16:9696/predict'


client = {
    "engine_rpm": 200,
    "fuel_pressure": 2.1,
    "lub_oil_pressure": 1.8,
    "coolant_pressure": 0.9,
}

response = requests.post(url, json=client)
predictions = response.json()


print(predictions)
if predictions['condition']:
    print('Engine condition is GOOD')
else:
    print('Engine condition is BAD')