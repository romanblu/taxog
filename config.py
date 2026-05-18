from dotenv import load_dotenv
import os
import boto3

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
MODEL_ARN = os.getenv("MODEL_ARN")

if not KNOWLEDGE_BASE_ID or not MODEL_ARN:
    raise RuntimeError("Set KNOWLEDGE_BASE_ID and MODEL_ARN in .env")


client = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

