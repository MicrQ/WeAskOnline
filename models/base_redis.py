#!/usr/bin/env python3
"""Redis connector which connects to the redis server and handles connection"""

from datetime import timedelta
import os
from dotenv import load_dotenv
import redis


load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
PASSWORD = os.getenv('PASSWORD')
USERNAME = os.getenv('USERNAME')


class RedisServer():
    def __init__(self):
        try:
            # self.redis_client = redis.Redis(HOST, PORT, password=PASSWORD, username=USERNAME)
            self.redis_client = redis.Redis()
        except Exception as e:
            print({"error": e})
    
    def get(self, key: str):
        try:
            return self.redis_client.get(key)
        except Exception as e:
            print("Key not found or expired")
    
    def set(self, key: str, value: str):
        if not key or not value:
            print("key or value is missing")
            return False
        self.redis_client.set(key, value, timedelta(hours=5.0))
        return True
    
    def set_token(self, key: str, value: str):
        if not key or not value:
            print("key or value is missing")
            return False
        self.redis_client.set(key, value, timedelta(days=2.0))
        return True
    
    def hset(self, user_email, token, user_data):
        if not user_data or not user_email:
            return False
        self.redis_client.hset(user_email, mapping=user_data)
        self.redis_client.hset(user_email, "token", token)
        self.redis_client.expire(user_email, 5 * 60)
        return True

    def hgetall(self, email: str):
        return self.redis_client.hgetall(email)
