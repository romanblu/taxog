# Taxog

CLI tax Q&A assistant powered by [Amazon Bedrock Knowledge Base](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Answers are grounded in your uploaded tax documents using retrieval-augmented generation (RAG), with source citations and multi-turn conversation support.

> **Disclaimer:** This tool provides general information from documents in the knowledge base. It is **not** professional tax, legal, or financial advice. Always verify with a qualified tax professional for your specific situation.

## Features

- Interactive terminal chat
- Grounded answers via `retrieve_and_generate`
- Source citations (S3 URIs and snippets)
- Multi-turn conversations using Bedrock `sessionId`
- Config via environment variables (`.env`)

## Prerequisites

- Python 3.10+ (recommended)
- An AWS account with access to:
  - Amazon Bedrock (model enabled in your region)
  - A Bedrock **Knowledge Base** already created and synced with your tax documents
- AWS credentials configured (see [Setup](#setup))

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/taxog.git
cd taxog
```

### 2. Create virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

| Variable | Description |
|:----------|:-------|
| AWS_REGION | AWS region for Bedrock (e.g. us-east-1) |
| KNOWLEDGE_BASE_ID | Your Bedrock Knowledge Base ID |
| MODEL_ARN | Inference profile or foundation model ARN for generation |
| AWS_ACCESS_KEY_ID | Optional if using `aws configure` instead |
| AWS_SECRET_ACCESS_KEY | Optional if using aws configure instead |


## AWS Configuration:

1. Create IAM user, for example `tax-agent-dev`
2. Specify IAM permissions:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:ListFoundationModels",
                "bedrock:Retrieve",
                "bedrock:RetrieveAndGenerate",
                "bedrock:GetInferenceProfile",
                "bedrock:ListInferenceProfiles"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::tax-agent-docs"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::tax-agent-docs/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:CreateKnowledgeBase",
                "bedrock:GetKnowledgeBase",
                "bedrock:StartIngestionJob",
                "bedrock:ListKnowledgeBases"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

- Go to security credentials tab and create access key, choose CLI or local code and save Access Key and Secret
- `aws configure` and enter access key, secret, us-east-1, json format 
- Enter the variables in .env
- test using `aws sts get-caller-identity`
- Configure S3 bucket:
  - Create `tax-agent-docs` bucket with folders: `/tax/ /vat/ /income-tax/`
  - Upload government PDFs, tax rules, VAT guides
  - From IRS website `[https://www.irs.gov/publications](https://www.irs.gov/publications)`  download documents and structure as follows:

```
s3://tax-agent-docs/
  ├── income-tax/
  │     ├── pub17.pdf
  │     ├── pub334.pdf
  │     ├── i1040sc.pdf
  │
  ├── expenses/
  │     ├── pub463.pdf
  │
  ├── home-office/
  │     ├── pub587.pdf
  │
  ├── depreciation/
  │     ├── pub946.pdf
```

- Bedrock knowledge bases:
  - Create new knowledge base
  - choose the s3 bucket as its source
  - Parsing strategy: bedrock default
  - Chunking strategy: Fixed size with 800-1200 max tokens and 100-200 overlap
  - Embedding model: titan text embedding v2
  - Choose OpenSearch vector store
  - Sync the knowledge base data source
- Add model inference profile and knowledge base ID to .env 
- Test knowledge base inside AWS CLI:
  - inside the KB select `Test knowldge base`
  - select the model
  - enter in the chat the following questions: `“What is deductible under Schedule C?”` `“Can I deduct home office expenses?”` `“How does depreciation work?”` `“What counts as business travel?”`
- Test in python CLI run `python main.py`

