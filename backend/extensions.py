from flask_sqlalchemy import SQLAlchemy
import redis

db = SQLAlchemy()

redis_client = redis.Redis(
    host="localhost",  # or "redis" if inside docker network
    port=6379,
    db=0,
    decode_responses=True,
)
