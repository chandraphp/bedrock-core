from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Document:
    """A retrieved piece of content with provenance.

    The citation engine in ops-brain uses source + metadata to build
    evidence-backed answers. bedrock-core defines the shape; applications
    populate the fields with domain-specific values (Splunk event ID,
    runbook URL, Confluence page, etc.).
    """
    content: str
    source: str
    score: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Document(source={self.source!r}, score={self.score:.3f}, content={self.content[:60]!r}...)"


class Retriever(ABC):
    """Abstract retrieval interface — resolves GAP-004.

    Retrieves relevant Documents given a query. Implementations decide
    the retrieval strategy (keyword, vector, hybrid, composite).
    callers only see retrieve().

    bedrock-core ships MockRetriever only. Applications provide
    domain-specific implementations backed by real vector stores.
    """

    @abstractmethod
    def retrieve(self, query: str, *, top_k: int = 5, **kwargs: Any) -> List[Document]:
        raise NotImplementedError

    def retrieve_and_format(self, query: str, *, top_k: int = 5, **kwargs: Any) -> str:
        """Retrieve and format as a numbered citation block for prompt injection."""
        docs = self.retrieve(query, top_k=top_k, **kwargs)
        if not docs:
            return "(no relevant documents found)"
        lines = []
        for i, doc in enumerate(docs, 1):
            lines.append(f"[{i}] {doc.source} (score={doc.score:.2f})\n{doc.content}")
        return "\n\n".join(lines)


class MockRetriever(Retriever):
    """Deterministic offline retriever for tests and CI.

    Stores documents in memory, uses simple keyword scoring.
    No embeddings, no vector store, no network.
    """

    def __init__(self, documents: Optional[List[Document]] = None):
        self._docs: List[Document] = list(documents or [])

    def add(self, document: Document) -> "MockRetriever":
        self._docs.append(document)
        return self

    def retrieve(self, query: str, *, top_k: int = 5, **kwargs: Any) -> List[Document]:
        query_lower = query.lower()
        scored = [
            Document(
                content=doc.content,
                source=doc.source,
                score=self._score(doc.content, query_lower),
                metadata=doc.metadata,
            )
            for doc in self._docs
        ]
        scored.sort(key=lambda d: d.score, reverse=True)
        return [d for d in scored if d.score > 0][:top_k]

    @staticmethod
    def _score(content: str, query: str) -> float:
        words = set(query.split())
        hits = sum(1 for w in words if w in content.lower())
        return hits / max(len(words), 1)
