import logging
from logging_setup import setup
from formatters import format_sources
from botocore.exceptions import ClientError, BotoCoreError
from bedrock.factory import get_rag_client
from settings import settings

log = logging.getLogger(__name__)
setup(level=settings.log_level)

def main():
    
    rag_client = get_rag_client()
    session_id = None
    print("Tax assistant. /new /quit. Not professional tax advice.")

    while True:
        question = input("> ").strip()
        if not question:
            continue

        if question == "/new":
            session_id = None
            print("New conversation started.")
            continue

        if question in ("/quit", "/q", "quit"):
            break
        try:
            result = rag_client.ask(question, session_id=session_id)
            print(result)
        except ClientError as e:
            code = e.response.get("Error, {}").get("Code", "Unknown")
            if code in {"ThrottlingException", "TooManyRequestsException"}:
                print("Service is throttling, please retry shortly.")
            elif code in {"AccessDeniedException", "UnauthorizedException"}:
                print("AWS denied the request. Check IAM permissions and model access.")
            elif code == "ResourceNotFoundException":
                print("Knowledge Base or model not found. Check KB_ID and MODEL_ARN.")
            else:
                log.exception("Bedrock client error")
                print(f"AWS error ({code}). See logs.")
            continue

        except (EndpointConnectionError, BotoCoreError):
            log.exception("Network/SDK error")
            print("Network problem reaching Bedrock. Retry.")
            continue
        
        print(result.answer)

        print("SOURCES: \n",format_sources(result.citations))
        
        session_id = result.session_id
