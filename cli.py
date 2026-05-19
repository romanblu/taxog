from bedrock import ask
from formatters import format_sources
from botocore.exceptions import ClientError, BotoCoreError

def main():
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
            result = ask(question, session_id=session_id)
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
        
        print(result["answer"])

        print("SOURCES: \n",format_sources(result["citations"]))
        
        session_id = result["session_id"]
