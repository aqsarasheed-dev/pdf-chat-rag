# Design Decisions

- Why ChromaDB: local, free, persistent, simple.
- Why FastEmbed: free local embeddings; avoids paid embedding APIs.
- Why MAX_DISTANCE gate: reduces hallucinations when retrieval is weak.
- Why lexical fallback: embeddings are weak for short queries; hybrid retrieval improves recall.
- Why citations + evidence quotes: forces grounded answers.