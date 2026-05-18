from config import client, KNOWLEDGE_BASE_ID, MODEL_ARN

def ask(question, session_id=None):
    kwargs = {
        "input":{
            "text": question
        },
        "retrieveAndGenerateConfiguration":{
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN
            }
        }
    }
    if session_id:
        kwargs["sessionId"] = session_id

    response = client.retrieve_and_generate(**kwargs)        
    

    return {
        "answer": response["output"]["text"],
        "citations": response.get("citations", []),
        "session_id": response.get("sessionId")
    }
