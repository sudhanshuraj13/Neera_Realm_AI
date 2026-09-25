"""
Tier 1: Dense Semantic Vector Alignment Engine.

Calculates high-speed (~20ms) vector cosine similarity between distilled candidate
and job representations using sentence-transformers (all-MiniLM-L6-v2).
Includes lightweight fallback for environments without PyTorch installed.
"""

from __future__ import annotations

import logging
import time
from functools import lru_cache
from typing import Optional, Tuple

import numpy as np
from .schemas import VectorSimilarityResult

logger = logging.getLogger("nextgen_ats.tier1_vector")


@lru_cache(maxsize=1)
def _load_sentence_transformer():
    """Lazy load the sentence transformer model singleton."""
    try:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading sentence-transformers model 'all-MiniLM-L6-v2'...")
        return SentenceTransformer("all-MiniLM-L6-v2")
    except ImportError:
        logger.warning(
            "sentence-transformers not installed. Running in heuristic vector fallback mode."
        )
        return None
    except Exception as e:
        logger.warning("Could not load sentence-transformers: %s. Using fallback.", e)
        return None


def _heuristic_similarity(text1: str, text2: str) -> float:
    """Fast Jaccard-based lexical-semantic overlap fallback."""
    tokens1 = set(w.lower() for w in text1.split() if len(w) > 2)
    tokens2 = set(w.lower() for w in text2.split() if len(w) > 2)
    if not tokens1 or not tokens2:
        return 0.30
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    jaccard = len(intersection) / len(union)
    # Scale Jaccard (typically 0.05-0.4) to resemble embedding cosine (0.3 - 0.8)
    return min(0.95, max(0.20, 0.35 + (jaccard * 1.5)))


def compute_vector_alignment(
    resume_distilled: str,
    jd_distilled: str,
) -> VectorSimilarityResult:
    """
    Compute dense vector similarity and calibrated ATS alignment score.

    Args:
        resume_distilled: Distilled candidate text.
        jd_distilled: Distilled job text.

    Returns:
        VectorSimilarityResult with raw cosine, calibrated score (0-100), and latency.
    """
    start_time = time.perf_counter()
    model = _load_sentence_transformer()

    if model is not None:
        try:
            embeddings = model.encode(
                [resume_distilled[:2000], jd_distilled[:2000]],
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            raw_cosine = float(np.dot(embeddings[0], embeddings[1]))
        except Exception as e:
            logger.warning("Embedding inference error: %s, falling back", e)
            raw_cosine = _heuristic_similarity(resume_distilled, jd_distilled)
    else:
        raw_cosine = _heuristic_similarity(resume_distilled, jd_distilled)

    # Calibrate raw cosine:
    # In technical document embeddings, unrelated documents sit around 0.25-0.35,
    # strong alignment is 0.70 - 0.85+.
    # Formula maps [0.25, 0.85] -> [15, 99]
    scaled = (raw_cosine - 0.25) / (0.85 - 0.25) * 100.0
    calibrated_score = int(np.clip(scaled, 10, 99))
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return VectorSimilarityResult(
        raw_cosine=round(raw_cosine, 4),
        calibrated_score=calibrated_score,
        latency_ms=round(elapsed_ms, 2),
    )
