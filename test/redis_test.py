#!/usr/bin/env python3

from random import randint
from models.base_redis import RedisServer

data = {
    "name": "foo",
    "mail": "foo@mail.com",
    "authorization": "user"
    }

redis_ = RedisServer()
redis_.hset("foo@mail.com", 7583, data)
print(redis_.hgetall("foo@mail.com"))
