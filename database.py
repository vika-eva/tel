import asyncpg
import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Database connected ✅")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            print("Database disconnected ❌")

    async def add_user(self, user_id: int, full_name: str, username: str):
        query = """INSERT INTO users (user_id, full_name, username)
                   VALUES ($1, $2, $3) 
                   ON CONFLICT (user_id) DO NOTHING"""
        await self.pool.execute(query, user_id, full_name, username)

    async def get_user(self, user_id: int):
        query = "SELECT * FROM users WHERE user_id = $1"
        return await self.pool.fetchrow(query, user_id)

db = Database()