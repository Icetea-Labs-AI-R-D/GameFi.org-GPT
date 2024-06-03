from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from typing import Any
from chromadb import HttpClient
import asyncio

class ChromaService:
    """
    ChromaService
    """
    embedding_function: OpenAIEmbeddingFunction
    vectordb_topic: Any
    vectordb_content: Any
    vectordb_docs: Any
    client: HttpClient
    def __init__(self) -> None:
        self.client = HttpClient()

        # Initialize the embedding function
        self.embedding_function = OpenAIEmbeddingFunction(
            api_key="",
        )        
        # Initialize vectordb collections
        self.vectordb_docs = self.client.get_or_create_collection(
            name="vector_docs",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        
        self.vectordb_content = self.client.get_or_create_collection(
            name="vector_content",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        
        self.vectordb_topic = self.client.get_or_create_collection(
            name="vector_topic",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        
    async def similarity_search(self, query: str = "", filter: dict = {}) -> dict:
        """
        Similarity search
        """
        result = self.vectordb_content.query(
            query_text=[query.lower()],
            n_results=3,
            where=filter
        )
        result = [{
            "page_content": result["documents"][0][i],
            "metadata": result["metadata"][0][i]
        } for i in range(len(result["ids"][0]))]
        return result
    
    async def similarity_search_with_score(self, query: str = "", index: int = 0):
        """_summary_

        Args:
            query (str, optional): _description_. Defaults to "".
            index (int, optional): _description_. Defaults to 0.
        """
        result = self.vectordb_content.query(
            query_text=[query.lower()],
            n_results=1
        )
        result = [{
            "page_content": result["documents"][0][i],
            "metadata": result["metadata"][0][i]
        } for i in range(len(result["ids"][0]))]
        return (result[0], index)
    
    async def retrieve_keywords(self, keyword: dict = {}, global_topic: dict = {}) -> dict:
        """_summary_

        Args:
            keyword (dict, optional): _description_. Defaults to {}.
            global_topic (dict, optional): _description_. Defaults to {}.
        """
        topics = []
        contents = []
        retrieved_topics = []
        tasks = []
        keyword = keyword.get("keywords", []) 
        
        try:
            keywords = [(key, index) for index, key in enumerate(keyword)]
            tasks = [
                self.similarity_search_with_score(key, index) for key, index in keywords
            ]
            retrieved_topics = await asyncio.gather(*tasks)
            topics = list(filter(lambda x: x[0]["metadata"]["type"] == "topic", retrieved_topics))
            if len(topics) > 0:
                topic = topics[0]
                keywords = list(filter(lambda x: x[1] != topic[1], keywords))
                global_topic = topic[0]["metadata"]
            filter = {
                "topic": global_topic.get("topic", "")
            }    
            keywords = list(map(lambda x: x[0], keywords))
            tasks = [
                self.similarity_search(key, filter) for key in keywords
            ]
            group_contents = await asyncio.gather(*tasks)
            for content in group_contents:
                contents.extend(content)
            contents = list(map(lambda x: x["metadata"], contents))
            return {
                "topic": global_topic,
                "content": contents,
                "global_topic": global_topic
            }
        except Exception as e:
            print(e)
            return {
                "topic": global_topic,
                "content": [],
                "global_topic": global_topic
            }