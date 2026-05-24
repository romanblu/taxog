from dotenv import load_dotenv
import os
import boto3
from botocore.config import Config
import re

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
MODEL_ARN = os.getenv("MODEL_ARN")

if not AWS_REGION:
    raise RuntimeError("AWS_REGION is required")
if not re.fullmatch(r"[A-Z0-9]{10}", KNOWLEDGE_BASE_ID or ""):
    raise RuntimeError("KNOWLEDGE_BASE_ID looks invalid (expected 10 uppercase alphanumerics)")
if not (MODEL_ARN or "").startswith("arn:aws:bedrock:"):
    raise RuntimeError("MODEL_ARN must be a Bedrock ARN")

config = Config(
    region_name=AWS_REGION,
    retries={"max_attempts": 5, "mode": "adaptive"},
    read_timeout=120,
    connect_timeout=10,
    user_agent_extra="taxog/0.1",
    
    )
client = boto3.client("bedrock-agent-runtime", config=config)

