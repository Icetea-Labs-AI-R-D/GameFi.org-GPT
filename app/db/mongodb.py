from motor.motor_asyncio import AsyncIOMotorClient
from app.core.conf import settings
from motor.core import (
    AgnosticClient,
    AgnosticDatabase,
    AgnosticCollection
)
from beanie import init_beanie

async_mongodb_client = None

def get_async_mongodb_client() -> AgnosticClient:
    
    """ 
    Use this function when beanie is not available
    """
    
    global async_mongodb_client
    if async_mongodb_client is None:
        async_mongodb_client = AsyncIOMotorClient(
            f"mongodb://localhost:27017/{settings.MONGODB_DATABASE}",
            maxPoolSize=100,
            minPoolSize=10,
        )
    return async_mongodb_client

def get_async_mongodb_database(db_name: str | None) -> AgnosticDatabase:
    if db_name is None:
        db_name = settings.MONGODB_DATABASE
    client = get_async_mongodb_client()
    return client[db_name]

def get_async_mongodb_collection(col_name: str) -> AgnosticCollection:
    db = get_async_mongodb_database()
    return db[col_name]

async def start_async_mongodb() -> None:
    try:
        async_mongodb_database = get_async_mongodb_database()
        await init_beanie(
            database=async_mongodb_database,
            document_models=[
                
            ],
        )
        print("Successfully initialized Beanie")
    except Exception as e:
        print(e)