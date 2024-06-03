import asyncio
from app.core.conf import settings
from openai import AsyncOpenAI
from langsmith.wrappers import wrap_openai
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class OpenAIQueue(metaclass=SingletonMeta):
    queue: asyncio.Queue
    
    def __init__(self):
        self.queue = asyncio.Queue()
        
    async def put(self, item):
        await self.queue.put(item)
    
    async def empty(self):
        return self.queue.empty()
    
    async def get(self):
        if self.empty():
            item = await self.queue.get()
            self.queue.task_done()
        return item
    
    async def init_queue(self):
        if self.queue is None:
            self.queue = asyncio.Queue()
            
        if self.empty():
            apis = [
                wrap_openai(AsyncOpenAI(api_key=settings.OPENAI_API_KEY1))
                for _ in range(2)
            ] + [
                wrap_openai(AsyncOpenAI(api_key=settings.OPENAI_API_KEY2))
                for _ in range(2)
            ]
            for api in apis:
                await self.put(api)
        print("Init openai key queue")
                
    async def close_queue(self):
        while not self.empty():
            self.queue.get_nowait()
            self.queue.task_done()
        self.queue = None
        print("Close openai key queue")

openai_queue = OpenAIQueue()

async def get_openai_queue():
    return openai_queue