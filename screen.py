#!/usr/bin/env python3
"""AI backend developer screening exercise.

Goal
----
Ingest the documents in ``docs/`` into an in-memory vector store: split each
document into sensible chunks, embed each chunk, and keep the chunk text,
embedding and metadata together in memory.

What you need to do
-------------------
Fill in every function marked ``TODO(candidate)``:

  1. ``load_documents``  - read the files from the docs folder
  2. ``chunk_text``      - split a document into chunks (this is the part we
                           care about most; justify your strategy in comments)
  3. ``embed_texts``     - turn chunk texts into embedding vectors
  4. ``ingest``          - wire it all together and fill ``STORE``

``display_store`` is already provided and prints whatever you put in ``STORE``,
so you can check your work. Do not change the ``Chunk`` fields it relies on,
but you may add extra metadata keys.

Run
---
    python screen.py                  # ingest ./docs and display the store
    python screen.py --docs other/    # use another folder
    python screen.py --full           # show full chunk text and all vector values

You may use any libraries or embedding provider you like (add them to
``requirements.txt``). If you have no API access, a local model is fine, and a
clearly-labelled fake embedding is acceptable as a last resort - tell us why.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_DOCS_DIR = Path(__file__).parent / "docs"
SUPPORTED_SUFFIXES = {".md", ".txt"}


# --------------------------------------------------------------------------- #
# Data model (provided)
# --------------------------------------------------------------------------- #
@dataclass
class Document:
    """A source document loaded from disk."""

    path: Path
    text: str


@dataclass
class Chunk:
    """One embedded chunk held in memory."""

    id: str                          # unique, stable id, e.g. "<doc>::<index>"
    text: str                        # the chunk content
    embedding: list[float]           # the vector for ``text``
    metadata: dict[str, Any] = field(default_factory=dict)
    # Suggested metadata: source, chunk_index, char_start, char_end, section
    # heading, token_count ... add whatever you think is useful for retrieval.


# The in-memory store. ``ingest`` must populate this.
STORE: list[Chunk] = []


# --------------------------------------------------------------------------- #
# TODO(candidate): implement these
# --------------------------------------------------------------------------- #
def load_documents(docs_dir: Path) -> list[Document]:
    """Read every supported file under ``docs_dir`` and return Documents.

    Think about: recursion, encoding errors, empty files, deterministic order.
    """
    raise NotImplementedError("TODO(candidate): implement load_documents")


def chunk_text(text: str, source: str) -> list[dict[str, Any]]:
    """Split ``text`` into chunks.

    Return a list of dicts, each with at least ``{"text": str}`` plus any
    metadata you want to keep (e.g. char offsets, section heading).

    Think about: chunk size and overlap, respecting structure (headings,
    paragraphs, code blocks, lists) instead of cutting mid-sentence, and what
    happens to very short or very long sections.
    """
    raise NotImplementedError("TODO(candidate): implement chunk_text")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return one embedding vector per input text, in the same order.

    Think about: batching, rate limits / retries, API errors, and keeping the
    vector dimensionality consistent.
    """
    raise NotImplementedError("TODO(candidate): implement embed_texts")


def ingest(docs_dir: Path) -> None:
    """Load, chunk and embed all documents, appending Chunks to ``STORE``.

    Should be safe to call twice (no duplicate chunks).
    """
    raise NotImplementedError("TODO(candidate): implement ingest")


# --------------------------------------------------------------------------- #
# Display (provided)
# --------------------------------------------------------------------------- #
def display_store(store: list[Chunk] | None = None, full: bool = False,
                  preview_chars: int = 80, preview_dims: int = 6) -> None:
    """Pretty-print the in-memory embeddings and their metadata."""
    store = STORE if store is None else store
    if not store:
        print("The store is empty - nothing has been ingested yet.")
        return

    dims = {len(c.embedding) for c in store}
    sources = {c.metadata.get("source", "?") for c in store}
    lengths = [len(c.text) for c in store]
    print("=" * 72)
    print(f"Chunks: {len(store)}   Sources: {len(sources)}   "
          f"Embedding dims: {sorted(dims)}")
    print(f"Chunk length (chars): min={min(lengths)} "
          f"avg={sum(lengths) // len(lengths)} max={max(lengths)}")
    if len(dims) > 1:
        print("WARNING: inconsistent embedding dimensionality!")
    print("=" * 72)

    for i, c in enumerate(store):
        text = c.text.replace("\n", "\\n")
        if not full and len(text) > preview_chars:
            text = text[:preview_chars] + "..."
        vec = c.embedding if full else c.embedding[:preview_dims]
        vec_str = ", ".join(f"{v:.4f}" for v in vec)
        if not full and len(c.embedding) > preview_dims:
            vec_str += ", ..."
        norm = sum(v * v for v in c.embedding) ** 0.5
        print(f"[{i}] id={c.id}")
        print(f"    text     : {text}")
        print(f"    embedding: dim={len(c.embedding)} norm={norm:.4f} [{vec_str}]")
        for k, v in sorted(c.metadata.items()):
            print(f"    meta.{k}: {v}")
        print("-" * 72)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS_DIR,
                        help="folder containing documents to ingest")
    parser.add_argument("--full", action="store_true",
                        help="show full chunk text and complete vectors")
    args = parser.parse_args()

    ingest(args.docs)
    display_store(full=args.full)


if __name__ == "__main__":
    main()
