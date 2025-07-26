import requests
import json

url = "https://lsm93412.live.dynatrace.com/api/v2/logs/ingest"
headers = {
    "Authorization": "Api-Token ",
    "Content-Type": "application/json; charset=utf-8"
}

payload = [
    {
        "timestamp": "2029-12-26T14:30:00Z",
        "level": "ERROR",
        "message": "Application failed to connect to database. from python i sent again and again",
        "host": "app-server-1",
        "service": "user-service-kk",
        "source": "application",
        "log.source": "user-service-kk-python",
        "log.trace_id": "123456abcdef",
        "log.span_id": "654321fedcba",
        "env": "production",
        "region": "us-east-1",
        "dt.system": "Linux",
        "dt.custom.key": "custom value"
    }
]

response = requests.post(url, headers=headers, data=json.dumps(payload))

print("Status code:", response.status_code)
print("Response body:", response.text)
