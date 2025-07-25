# 🔄 MySQL to Redis Caching via Flask API (Docker Compose POC)

This Docker Compose project demonstrates a **proof of concept (POC)** for caching **MySQL database results in Redis**, served via a **Flask API**.

---

## 📦 What This Does

- A Flask API fetches data from a **MySQL database**.
- The response is **cached in Redis** to avoid hitting MySQL on repeated requests.
- Redis serves cached responses if available.
- The MySQL container is **not part of this Compose file** — instead, it's running in **another Docker Compose project**.
- We use **Docker external networking** to connect across projects.

---
# Database Operation
Connect Docker Mysql using `Dbeaver` or any other sql client and User database `company` 
```
CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255),
  email VARCHAR(255)
);

INSERT INTO users (name, email) VALUES ('kk1', 'kk1@example.com')
INSERT INTO users (name, email) VALUES ('kk2', 'kk2@example.com')

Select * from users;
```
## 📁 Project Structure

```
project-root/
├── app/
│ ├── app.py
│ └── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 🧠 Why Cross-Compose Networking?

This POC assumes:
- You already have another Docker application running a MySQL container named `mysqltomongoflinkcdc`.
- That application is using a Docker network called `mysqltomongoflinkcdc_default`.

This Compose file connects to that MySQL container via **network sharing**, allowing the Flask app to talk to the remote MySQL service as if it were local.

---

## ⚙️ Docker Compose Setup

### 🐳 `docker-compose.yml`

```yaml
version: '3.8'

services:
  redis:
    image: redis:alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
    networks:
      - mysqltomongoflinkcdc_default

  flask-api:
    build: .
    container_name: flask-app-cache
    ports:
      - "5001:5001"
    depends_on:
      - redis
    environment:
      DB_HOST: mysql        # Hostname of the external MySQL container
      DB_PORT: 3306
      DB_USER: user
      DB_PASSWORD: password
      DB_NAME: company
      REDIS_HOST: redis
    networks:
      - mysqltomongoflinkcdc_default

volumes:
  mysql_data_cache:

networks:
  mysqltomongoflinkcdc_default:
    external: true  # Connect to external Docker network from another Compose
```

# 🧱  Dockerfile
```
FROM python:3.11-slim
WORKDIR /app
COPY app/ .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
```
# 📜  requirements.txt
```
flask
redis
mysql-connector-python
```
# 🐍 Flask App Logic
Inside app/app.py, the app checks Redis first. If data isn’t cached, it queries MySQL, caches it in Redis, and returns the result.
```
from flask import Flask, jsonify
import mysql.connector
import redis
import os
import json

app = Flask(__name__)

# Connect to Redis
redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0)

# MySQL connection function
def get_mysql_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "user"),
        password=os.environ.get("DB_PASSWORD", "password"),
        database=os.environ.get("DB_NAME", "company")
    )

@app.route("/user/<int:user_id>")
def get_user(user_id):
    # Check Redis cache
    cached = redis_client.get(f"user:{user_id}")
    if cached:
        return jsonify({"source": "redis", "data": json.loads(cached)})

    # Query MySQL
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Cache in Redis
    redis_client.setex(f"user:{user_id}", 60, json.dumps(user))
    return jsonify({"source": "mysql", "data": user})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

```
# 🧪 Testing
```
docker-compose up --build
```
# Test via browser or curl:
```
curl http://localhost:5001/user/1
```
- First request: fetches from MySQL
- Second request: serves from Redis cache


