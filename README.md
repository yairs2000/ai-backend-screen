# AI Backend Developer Screen

A small take-home / pairing exercise for backend AI engineer candidates.

## Layout

```
screen.py         # skeleton the candidate completes
docs/             # documents to ingest (add or swap in your own)
requirements.txt  # candidate adds dependencies here
```

## The task

Open `screen.py` and implement the `TODO(candidate)` functions:

1. `load_documents` - read files from `docs/`
2. `chunk_text` - split documents into appropriate chunks with useful metadata
3. `embed_texts` - produce an embedding per chunk
4. `ingest` - tie it together and populate the in-memory `STORE` (idempotent)

Then run `python screen.py`. The provided `display_store` prints every
in-memory chunk with its embedding summary and metadata.
