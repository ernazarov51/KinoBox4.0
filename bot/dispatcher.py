from aiogram import Dispatcher,Bot
from db.config import TG
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
redis=Redis(host='localhost', port=6379)
redis_storage=RedisStorage(redis)


dp=Dispatcher(storage=redis_storage)
bot=Bot(TG.token)