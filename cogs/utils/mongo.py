import os
from typing import Optional
import motor.motor_asyncio as motor

client = motor.AsyncIOMotorClient(os.getenv('client_uri'))
db = client['tools-by-bitacora']


class Guild:
    def __init__(self, guild: int) -> None:
        self.guilds = db['guilds']
        self.query = {'_id': guild}

    async def new(self) -> None:
        await self.guilds.insert_one(self.query)

    async def find(self) -> Optional[dict]:
        return await self.guilds.find_one(self.query)

    async def check(self) -> dict:
        guild_settings = await self.find()
        if not guild_settings:
            await self.new()
            guild_settings = await self.find()
        return guild_settings

    async def update(self, query: dict) -> None:
        await self.guilds.update_one(self.query, query, upsert=True)
