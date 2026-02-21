from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import Agent, MCPStreamableHTTPTool
from app.tools.document_intelligence_scanner import DocumentIntelligenceInvoiceScanHelper
from app.common.user_profile_provider import UserProfileProvider

import logging


logger = logging.getLogger(__name__)

class PaymentAgent :
    instructions = """
    you are a personal financial advisor who help the user with their recurrent bill payments. The user may want to pay the bill uploading a photo of the bill, or it may start the payment checking transactions history for a specific payee.
        
       {user_mail}
        Current timestamp:
       {current_date_time}
        
        """
    name = "PaymentAgent"
    description = "This agent manages user payments related information such as submitting payment requests and bill payments."

    def __init__(self, azure_chat_client: AzureOpenAIChatClient,
                  account_mcp_server_url: str,
                  transaction_mcp_server_url: str,
                  payment_mcp_server_url: str,
                  document_scanner_helper : DocumentIntelligenceInvoiceScanHelper):
        self.azure_chat_client = azure_chat_client
        self.account_mcp_server_url = account_mcp_server_url
        self.transaction_mcp_server_url = transaction_mcp_server_url
        self.payment_mcp_server_url = payment_mcp_server_url
        self.document_scanner_helper = document_scanner_helper
        

    async def build_af_agent(self) -> Agent:
    
      logger.info("Building request scoped Payment agent run ")
      
      logger.info("Initializing Account MCP, Transaction MCP, Payment MCP server tools for PaymentAgent") 
      
      account_mcp_server = MCPStreamableHTTPTool(
        name="Account MCP server client",
        url=self.account_mcp_server_url
      )
      transaction_mcp_server = MCPStreamableHTTPTool(
        name="Transaction MCP server client",
        url=self.transaction_mcp_server_url
      )
      payment_mcp_server = MCPStreamableHTTPTool(
        name="Payment MCP server client",
        url=self.payment_mcp_server_url,
        approval_mode = { "always_require_approval": ["processPayment"] }
      )

      await account_mcp_server.connect()
      await transaction_mcp_server.connect()
      await payment_mcp_server.connect()
      full_instruction = PaymentAgent.instructions.format(user_mail=UserProfileProvider._get_logged_user_email(), 
                                                          current_date_time=UserProfileProvider._get_current_timestamp())
      return Agent(
      client=self.azure_chat_client,
      instructions=full_instruction.strip(),
      name=PaymentAgent.name,
      tools=[account_mcp_server,
              transaction_mcp_server, 
              payment_mcp_server,
            self.document_scanner_helper.scan_invoice])
            
        