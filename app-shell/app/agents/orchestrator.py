from typing import Any, AsyncGenerator
from collections.abc import AsyncIterable
from agent_framework.azure import AzureOpenAIChatClient
from app.agents.sample_agent import SampleAgent
from agent_framework import WorkflowEvent


from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

class Orchestrator:
    

    def __init__(self, 
                 client: AzureOpenAIChatClient,
                 sample_agent: SampleAgent
                                ):
      self.client = client
      self.sample_agent = sample_agent
      self.workflow = None  # Will be initialized in async method

            
    
    async def processMessageStream(self, user_message: str , thread_id : str ) -> AsyncGenerator[WorkflowEvent,None]:
        # TODO: implement actual orchestration logic here, for demo purposes we are directly invoking the sample agent with the user message and streaming the response back.
        pass