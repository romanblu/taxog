from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class RagAnswer:
    answer: str
    citations: list[dict[str, Any]]
    session_id: str | None
    request_id: str | None
class TaxRagClient:
    def __init__(self, client, kb_id: str, model_arn: str, system_prompt: str,
                 guardrail_id: str | None = None, guardrail_version: str | None = None,
                 num_results: int = 5):
        self._client = client
        self._kb_id = kb_id
        self._model_arn = model_arn
        self._system_prompt = system_prompt
        self._guardrail_id = guardrail_id
        self._guardrail_version = guardrail_version
        self._num_results = num_results
    def ask(self, question: str, *, session_id: str | None = None,
            metadata_filter: dict | None = None) -> RagAnswer:
        kb_cfg: dict[str, Any] = {
            "knowledgeBaseId": self._kb_id,
            "modelArn": self._model_arn,
            "retrievalConfiguration": {
                "vectorSearchConfiguration": {
                    "numberOfResults": self._num_results,
                    **({"filter": metadata_filter} if metadata_filter else {}),
                }
            },
            "generationConfiguration": {
                "promptTemplate": {"textPromptTemplate": self._system_prompt},
                "inferenceConfig": {
                    "textInferenceConfig": {"temperature": 0.2, "maxTokens": 1024}
                },
            },
        }
        if self._guardrail_id:
            kb_cfg["generationConfiguration"]["guardrailConfiguration"] = {
                "guardrailId": self._guardrail_id,
                "guardrailVersion": self._guardrail_version or "DRAFT",
            }
        kwargs: dict[str, Any] = {
            "input": {"text": question},
            "retrieveAndGenerateConfiguration": {
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": kb_cfg,
            },
        }
        if session_id:
            kwargs["sessionId"] = session_id
        resp = self._client.retrieve_and_generate(**kwargs)
        return RagAnswer(
            answer=resp["output"]["text"],
            citations=resp.get("citations", []),
            session_id=resp.get("sessionId"),
            request_id=resp.get("ResponseMetadata", {}).get("RequestId"),
        )