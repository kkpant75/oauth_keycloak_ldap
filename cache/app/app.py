from flask import Flask, jsonify, request
import mysql.connector
import redis
import os
import json

app = Flask(__name__)

# Redis connection
redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0)

# MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)), 
        user=os.environ.get("DB_USER", "user"),
        password=os.environ.get("DB_PASSWORD", "password"),
        database=os.environ.get("DB_NAME", "testdb")
    )

@app.route("/user/<int:user_id>")
def get_user(user_id):
    # Check Redis first
    cached_user = redis_client.get(f"user:{user_id}")
    if cached_user:
        return jsonify({"source": "cache", "user": json.loads(cached_user)})

    # Fallback to MySQL
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Cache in Redis
    redis_client.setex(f"user:{user_id}", 10, json.dumps(user))  # Cache for 60 seconds

    return jsonify({"source": "mysql", "user": user})

if __name__ == "__main__":
    #get_user(1)
    app.run(host="0.0.0.0", port=5001)
