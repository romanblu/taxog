from bedrock import ask
from formatters import format_sources


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
        except Exception as e:
            print(f"Error: {e}")
            continue

        print(result["answer"])

        print("SOURCES: \n",format_sources(result["citations"]))
        
        session_id = result["session_id"]
