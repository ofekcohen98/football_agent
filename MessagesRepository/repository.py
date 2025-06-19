import redis
from dotenv import load_dotenv
import os


class RedisRepository:
    def __init__(self):
        """Initialize the Redis repository."""
        load_dotenv()
        self.redis_server = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            db=int(os.getenv("REDIS_DB"))
        )

    def set(self, key, value):
        """        Set a key-value pair in Redis.

        Args:
            key (str): The key to set.
            value (str): The value to associate with the key.
        """
        self.redis_server.set(key, value)

    def get(self, key):
        """
        Get the value associated with a key in Redis.

        Args:
            key (str): The key to retrieve.

        Returns:
            str: The value associated with the key, or None if the key does not exist.
        """
        value = self.redis_server.get(key)
        return value.decode('utf-8') if value else None
    
    def delete(self, key):
        """
        Delete a key from Redis.

        Args:
            key (str): The key to delete.
        """
        self.redis_server.delete(key)