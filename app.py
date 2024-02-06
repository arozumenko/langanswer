# Save this as app.py
import uvicorn
import logging
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response
from analysta_index.interfaces.llm_processor import generateResponse

from config import guidance_message, context_message

logging.basicConfig(level=logging.DEBUG)

# ChatCompletion is an abstract class for applications and model adapters
class TestAssistantApplication(ChatCompletion):
    async def chat_completion(
        self, request: Request, response: Response
    ) -> None:
        # Get last message (the newest) from the history
        last_user_message = request.messages[-1]
        
        # Generate response with a single choice
        with response.create_single_choice() as choice:
            response = generateResponse(last_user_message.content, guidance_message, context_message, collection='test_collection', top_k=10)
            message = response['response'] + '\n\n' + 'References: ' + '\n\n' 
            
            for ref in response['references']:
                message += f'[{ref}]\n\n'
            choice.append_content(message or "")


# DIALApp extends FastAPI to provide an user-friendly interface for routing requests to your applications
app = DIALApp()
app.add_chat_completion("echo", TestAssistantApplication())

# Run built app
if __name__ == "__main__":
    uvicorn.run(app, port=5003)