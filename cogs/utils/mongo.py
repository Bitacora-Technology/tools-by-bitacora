import os

import motor.motor_asyncio as motor

client = motor.AsyncIOMotorClient(os.getenv('client_uri'))
db = client['tools-by-bitacora']
