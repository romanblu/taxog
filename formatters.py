
def format_sources(citations):
    """Format the citations into a readable format"""
    if not citations:
        return []
    
    lines = []
    for citation in citations:
        for ref in citation.get("retrievedReferences", []):
            meta = ref.get("metadata", {})
            uri = (
                meta.get("x-amz-bedrock-kb-source-uri")
                or meta.get("source")
                or meta.get("uri")
            )

            if not uri:
                loc = ref.get("location") or {}
                s3 = loc.get("s3Location") or {}
                uri = s3.get("uri")

            snippet = (ref.get("content") or {}).get("text", "")
            snippet = (snippet[:200] + "…") if len(snippet) > 200 else snippet
            if uri:
                lines.append(f"{uri}" + (f" — \"{snippet}\"" if snippet else ""))
            elif snippet:
                lines.append(f"(no URI) — \"{snippet}\"")

    seen = set()
    unique = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique.append(line)
    return unique
