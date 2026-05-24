from config import client, KNOWLEDGE_BASE_ID, MODEL_ARN
from bedrock.rag import TaxRagClient
from bedrock.prompts import TAX_SYSTEM_PROMPT
import os

def get_rag_client() -> TaxRagClient:
    return TaxRagClient(
        client=client,
        kb_id=KNOWLEDGE_BASE_ID,
        model_arn=MODEL_ARN,
        system_prompt=TAX_SYSTEM_PROMPT,
        guardrail_id=os.getenv("GUARDRAIL_ID"),          # optional
        guardrail_version=os.getenv("GUARDRAIL_VERSION"),
        num_results=int(os.getenv("KB_NUM_RESULTS", "5")),
    )