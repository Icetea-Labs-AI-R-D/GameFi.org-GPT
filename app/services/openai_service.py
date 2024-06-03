class OpenAIService:
    """
    OpenAIService
    """
    def __init__(self) ->  None:
        pass
    
    async def extract_keyword(self, message: str = "", conversation : list = None, global_topic: dict = None):
        if global_topic is None:
            global_topic = {"api": "", "source": "", "topic": "", "type": ""}
        if conversation is None:
            conversation = []
            
        