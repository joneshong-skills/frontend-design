#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Core - Hybrid BM25 + embedding search for UI/UX style guides

Architecture (aligned with skill-proxy hybrid pattern):
  Phase 1: BM25 keyword scoring (standard TF-IDF)
  Phase 2: Embedding similarity (Qwen3-Embedding-0.6B via oMLX bridge)
  Phase 3: Score-weighted fusion with dynamic alpha
  Graceful degradation: oMLX down → BM25-only fallback
"""

import csv
import json
import math
import re
import subprocess
from collections import defaultdict
from math import log
from pathlib import Path

# ============ CONFIGURATION ============
DATA_DIR = Path(__file__).parent.parent / "data"
EMBED_CACHE_DIR = Path.home() / ".claude/data/frontend-design"
MAX_RESULTS = 3

# oMLX embedding bridge (Qwen3-Embedding-0.6B via persistent subprocess)
OMLX_PYTHON = Path.home() / ".venvs/omlx/bin/python3"
OMLX_WORKER = Path.home() / ".venvs/omlx/embed_worker.py"
EMBED_BATCH_SIZE = 10
EMBED_THRESHOLD = 0.40

# Score-weighted fusion (aligned with skill-proxy pattern)
FUSION_ALPHA_HIGH = 0.7  # alpha when max_bm25 >= 3.0 (strong keyword match)
FUSION_ALPHA_MED = 0.5  # alpha when max_bm25 >= 1.0
FUSION_ALPHA_LOW = 0.3  # alpha when max_bm25 < 1.0 (ambiguous, lean on embedding)

CSV_CONFIG = {
    "style": {
        "file": "styles.csv",
        "search_cols": [
            "Style Category",
            "Keywords",
            "Best For",
            "Type",
            "AI Prompt Keywords",
        ],
        "output_cols": [
            "Style Category",
            "Type",
            "Keywords",
            "Primary Colors",
            "Effects & Animation",
            "Best For",
            "Performance",
            "Accessibility",
            "Framework Compatibility",
            "Complexity",
            "AI Prompt Keywords",
            "CSS/Technical Keywords",
            "Implementation Checklist",
            "Design System Variables",
        ],
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["Product Type", "Notes"],
        "output_cols": [
            "Product Type",
            "Primary (Hex)",
            "Secondary (Hex)",
            "CTA (Hex)",
            "Background (Hex)",
            "Text (Hex)",
            "Notes",
        ],
    },
    "chart": {
        "file": "charts.csv",
        "search_cols": [
            "Data Type",
            "Keywords",
            "Best Chart Type",
            "Accessibility Notes",
        ],
        "output_cols": [
            "Data Type",
            "Keywords",
            "Best Chart Type",
            "Secondary Options",
            "Color Guidance",
            "Accessibility Notes",
            "Library Recommendation",
            "Interactive Level",
        ],
    },
    "landing": {
        "file": "landing.csv",
        "search_cols": [
            "Pattern Name",
            "Keywords",
            "Conversion Optimization",
            "Section Order",
        ],
        "output_cols": [
            "Pattern Name",
            "Keywords",
            "Section Order",
            "Primary CTA Placement",
            "Color Strategy",
            "Conversion Optimization",
        ],
    },
    "product": {
        "file": "products.csv",
        "search_cols": [
            "Product Type",
            "Keywords",
            "Primary Style Recommendation",
            "Key Considerations",
        ],
        "output_cols": [
            "Product Type",
            "Keywords",
            "Primary Style Recommendation",
            "Secondary Styles",
            "Landing Page Pattern",
            "Dashboard Style (if applicable)",
            "Color Palette Focus",
        ],
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["Category", "Issue", "Description", "Platform"],
        "output_cols": [
            "Category",
            "Issue",
            "Platform",
            "Description",
            "Do",
            "Don't",
            "Code Example Good",
            "Code Example Bad",
            "Severity",
        ],
    },
    "typography": {
        "file": "typography.csv",
        "search_cols": [
            "Font Pairing Name",
            "Category",
            "Mood/Style Keywords",
            "Best For",
            "Heading Font",
            "Body Font",
        ],
        "output_cols": [
            "Font Pairing Name",
            "Category",
            "Heading Font",
            "Body Font",
            "Mood/Style Keywords",
            "Best For",
            "Google Fonts URL",
            "CSS Import",
            "Tailwind Config",
            "Notes",
        ],
    },
    "icons": {
        "file": "icons.csv",
        "search_cols": ["Category", "Icon Name", "Keywords", "Best For"],
        "output_cols": [
            "Category",
            "Icon Name",
            "Keywords",
            "Library",
            "Import Code",
            "Usage",
            "Best For",
            "Style",
        ],
    },
    "react": {
        "file": "react-performance.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description"],
        "output_cols": [
            "Category",
            "Issue",
            "Platform",
            "Description",
            "Do",
            "Don't",
            "Code Example Good",
            "Code Example Bad",
            "Severity",
        ],
    },
    "web": {
        "file": "web-interface.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description"],
        "output_cols": [
            "Category",
            "Issue",
            "Platform",
            "Description",
            "Do",
            "Don't",
            "Code Example Good",
            "Code Example Bad",
            "Severity",
        ],
    },
}

STACK_CONFIG = {
    "html-tailwind": {"file": "stacks/html-tailwind.csv"},
    "react": {"file": "stacks/react.csv"},
    "nextjs": {"file": "stacks/nextjs.csv"},
    "astro": {"file": "stacks/astro.csv"},
    "vue": {"file": "stacks/vue.csv"},
    "nuxtjs": {"file": "stacks/nuxtjs.csv"},
    "nuxt-ui": {"file": "stacks/nuxt-ui.csv"},
    "svelte": {"file": "stacks/svelte.csv"},
    "swiftui": {"file": "stacks/swiftui.csv"},
    "react-native": {"file": "stacks/react-native.csv"},
    "flutter": {"file": "stacks/flutter.csv"},
    "shadcn": {"file": "stacks/shadcn.csv"},
    "jetpack-compose": {"file": "stacks/jetpack-compose.csv"},
}

# Common columns for all stacks
_STACK_COLS = {
    "search_cols": ["Category", "Guideline", "Description", "Do", "Don't"],
    "output_cols": [
        "Category",
        "Guideline",
        "Description",
        "Do",
        "Don't",
        "Code Good",
        "Code Bad",
        "Severity",
        "Docs URL",
    ],
}

AVAILABLE_STACKS = list(STACK_CONFIG.keys())


# ============ EMBEDDING HELPERS (oMLX subprocess bridge) ============

_omlx_proc: subprocess.Popen | None = None


def _ensure_omlx() -> bool:
    """Start oMLX worker subprocess if not running."""
    global _omlx_proc
    if _omlx_proc is not None and _omlx_proc.poll() is None:
        return True
    if not OMLX_PYTHON.exists() or not OMLX_WORKER.exists():
        return False
    try:
        _omlx_proc = subprocess.Popen(
            [str(OMLX_PYTHON), str(OMLX_WORKER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        line = _omlx_proc.stdout.readline()
        if not line:
            _omlx_proc.kill()
            _omlx_proc = None
            return False
        status = json.loads(line.strip())
        if status.get("status") == "ready":
            return True
        _omlx_proc.kill()
        _omlx_proc = None
        return False
    except Exception:
        if _omlx_proc:
            try:
                _omlx_proc.kill()
            except ProcessLookupError:
                pass
        _omlx_proc = None
        return False


def _embed_batch(texts):
    """Embed a batch of texts via oMLX bridge. Returns list of vectors or None on failure."""
    if not _ensure_omlx():
        return None
    try:
        req = {"texts": texts, "task_type": "search_document"}
        _omlx_proc.stdin.write(json.dumps(req) + "\n")
        _omlx_proc.stdin.flush()
        line = _omlx_proc.stdout.readline()
        if not line:
            return None
        resp = json.loads(line.strip())
        if "error" in resp:
            return None
        return resp.get("embeddings", [])
    except Exception:
        return None


def _embed_query(text):
    """Embed a single query via oMLX bridge. Returns vector or None."""
    if not _ensure_omlx():
        return None
    try:
        req = {"texts": [text], "task_type": "search_query"}
        _omlx_proc.stdin.write(json.dumps(req) + "\n")
        _omlx_proc.stdin.flush()
        line = _omlx_proc.stdout.readline()
        if not line:
            return None
        resp = json.loads(line.strip())
        if "error" in resp:
            return None
        embeddings = resp.get("embeddings", [])
        return embeddings[0] if embeddings else None
    except Exception:
        return None


def _cosine_sim(a, b):
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


def _cache_path_for(csv_path):
    """Get embedding cache file path for a given CSV."""
    EMBED_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    stem = csv_path.stem
    parent = csv_path.parent.name
    # stacks/react.csv → stacks-react.embeddings.json
    prefix = f"{parent}-" if parent != "data" else ""
    return EMBED_CACHE_DIR / f"{prefix}{stem}.embeddings.json"


def _load_or_build_embeddings(csv_path, documents):
    """Load embeddings from cache or build them. Returns list of vectors or None."""
    cache_file = _cache_path_for(csv_path)

    # Check cache freshness
    if cache_file.exists():
        csv_mtime = csv_path.stat().st_mtime
        cache_mtime = cache_file.stat().st_mtime
        if cache_mtime > csv_mtime:
            try:
                cached = json.loads(cache_file.read_text())
                if len(cached) == len(documents):
                    return cached
            except (json.JSONDecodeError, KeyError):
                pass  # Rebuild on corrupt cache

    # Build embeddings in batches
    all_embeddings = []
    for i in range(0, len(documents), EMBED_BATCH_SIZE):
        batch = documents[i : i + EMBED_BATCH_SIZE]
        result = _embed_batch(batch)
        if result is None:
            return None  # Ollama unavailable, graceful degradation
        all_embeddings.extend(result)

    # Save cache
    try:
        cache_file.write_text(json.dumps(all_embeddings))
    except OSError:
        pass  # Non-fatal

    return all_embeddings


def _compute_alpha(max_bm25):
    """Dynamic alpha based on BM25 confidence (same pattern as skill-proxy)."""
    if max_bm25 >= 3.0:
        return FUSION_ALPHA_HIGH
    elif max_bm25 >= 1.0:
        return FUSION_ALPHA_MED
    else:
        return FUSION_ALPHA_LOW


def _score_fuse(bm25_ranked, embed_sims, max_results):
    """Score-weighted fusion of BM25 and embedding similarities.

    bm25_ranked: [(idx, score), ...] sorted by score desc
    embed_sims: [(idx, similarity), ...] for all docs above threshold
    Returns: [(idx, fused_score), ...] top max_results
    """
    if not bm25_ranked and not embed_sims:
        return []

    max_bm25 = bm25_ranked[0][1] if bm25_ranked else 1.0
    alpha = _compute_alpha(max_bm25)

    bm25_map = {idx: score for idx, score in bm25_ranked}
    embed_map = {idx: sim for idx, sim in embed_sims}

    all_indices = set(bm25_map.keys()) | set(embed_map.keys())
    fused = []
    for idx in all_indices:
        bm25_norm = bm25_map.get(idx, 0) / max_bm25 if max_bm25 > 0 else 0
        embed_sim = embed_map.get(idx, 0)
        score = alpha * bm25_norm + (1 - alpha) * embed_sim
        fused.append((idx, score))

    fused.sort(key=lambda x: -x[1])
    return fused[:max_results]


# ============ BM25 IMPLEMENTATION ============
class BM25:
    """BM25 ranking algorithm for text search"""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0

    def tokenize(self, text):
        """Lowercase, split, remove punctuation, filter short words"""
        text = re.sub(r"[^\w\s]", " ", str(text).lower())
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents):
        """Build BM25 index from documents"""
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N

        for doc in self.corpus:
            seen = set()
            for word in doc:
                if word not in seen:
                    self.doc_freqs[word] += 1
                    seen.add(word)

        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        """Score all documents against query"""
        query_tokens = self.tokenize(query)
        scores = []

        for idx, doc in enumerate(self.corpus):
            score = 0
            doc_len = self.doc_lengths[idx]
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1

            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf = self.idf[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (
                        1 - self.b + self.b * doc_len / self.avgdl
                    )
                    score += idf * numerator / denominator

            scores.append((idx, score))

        return sorted(scores, key=lambda x: x[1], reverse=True)


# ============ SEARCH FUNCTIONS ============
def _load_csv(filepath):
    """Load CSV and return list of dicts"""
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _search_csv(filepath, search_cols, output_cols, query, max_results):
    """Core hybrid search: BM25 + embedding with score-weighted fusion."""
    if not filepath.exists():
        return []

    data = _load_csv(filepath)

    # Build documents from search columns
    documents = [" ".join(str(row.get(col, "")) for col in search_cols) for row in data]

    # Phase 1: BM25 search
    bm25 = BM25()
    bm25.fit(documents)
    bm25_ranked = bm25.score(query)

    # Phase 2: Embedding search (graceful degradation if oMLX unavailable)
    doc_embeddings = _load_or_build_embeddings(filepath, documents)
    if doc_embeddings:
        q_vec = _embed_query(query)
        if q_vec:
            embed_sims = []
            for idx, d_vec in enumerate(doc_embeddings):
                sim = _cosine_sim(q_vec, d_vec)
                if sim >= EMBED_THRESHOLD:
                    embed_sims.append((idx, sim))
            embed_sims.sort(key=lambda x: -x[1])

            # Phase 3: Score-weighted fusion
            fused = _score_fuse(bm25_ranked, embed_sims, max_results)
            results = []
            for idx, score in fused:
                if score > 0:
                    row = data[idx]
                    results.append(
                        {col: row.get(col, "") for col in output_cols if col in row}
                    )
            return results

    # Fallback: BM25-only (oMLX unavailable)
    results = []
    for idx, score in bm25_ranked[:max_results]:
        if score > 0:
            row = data[idx]
            results.append({col: row.get(col, "") for col in output_cols if col in row})

    return results


def detect_domain(query):
    """Auto-detect the most relevant domain from query"""
    query_lower = query.lower()

    domain_keywords = {
        "color": ["color", "palette", "hex", "#", "rgb"],
        "chart": [
            "chart",
            "graph",
            "visualization",
            "trend",
            "bar",
            "pie",
            "scatter",
            "heatmap",
            "funnel",
        ],
        "landing": [
            "landing",
            "page",
            "cta",
            "conversion",
            "hero",
            "testimonial",
            "pricing",
            "section",
        ],
        "product": [
            "saas",
            "ecommerce",
            "e-commerce",
            "fintech",
            "healthcare",
            "gaming",
            "portfolio",
            "crypto",
            "dashboard",
        ],
        "style": [
            "style",
            "design",
            "ui",
            "minimalism",
            "glassmorphism",
            "neumorphism",
            "brutalism",
            "dark mode",
            "flat",
            "aurora",
            "prompt",
            "css",
            "implementation",
            "variable",
            "checklist",
            "tailwind",
        ],
        "ux": [
            "ux",
            "usability",
            "accessibility",
            "wcag",
            "touch",
            "scroll",
            "animation",
            "keyboard",
            "navigation",
            "mobile",
        ],
        "typography": ["font", "typography", "heading", "serif", "sans"],
        "icons": [
            "icon",
            "icons",
            "lucide",
            "heroicons",
            "symbol",
            "glyph",
            "pictogram",
            "svg icon",
        ],
        "react": [
            "react",
            "next.js",
            "nextjs",
            "suspense",
            "memo",
            "usecallback",
            "useeffect",
            "rerender",
            "bundle",
            "waterfall",
            "barrel",
            "dynamic import",
            "rsc",
            "server component",
        ],
        "web": [
            "aria",
            "focus",
            "outline",
            "semantic",
            "virtualize",
            "autocomplete",
            "form",
            "input type",
            "preconnect",
        ],
    }

    scores = {
        domain: sum(1 for kw in keywords if kw in query_lower)
        for domain, keywords in domain_keywords.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "style"


def search(query, domain=None, max_results=MAX_RESULTS):
    """Main search function with auto-domain detection"""
    if domain is None:
        domain = detect_domain(query)

    config = CSV_CONFIG.get(domain, CSV_CONFIG["style"])
    filepath = DATA_DIR / config["file"]

    if not filepath.exists():
        return {"error": f"File not found: {filepath}", "domain": domain}

    results = _search_csv(
        filepath, config["search_cols"], config["output_cols"], query, max_results
    )

    return {
        "domain": domain,
        "query": query,
        "file": config["file"],
        "count": len(results),
        "results": results,
    }


def search_stack(query, stack, max_results=MAX_RESULTS):
    """Search stack-specific guidelines"""
    if stack not in STACK_CONFIG:
        return {
            "error": f"Unknown stack: {stack}. Available: {', '.join(AVAILABLE_STACKS)}"
        }

    filepath = DATA_DIR / STACK_CONFIG[stack]["file"]

    if not filepath.exists():
        return {"error": f"Stack file not found: {filepath}", "stack": stack}

    results = _search_csv(
        filepath,
        _STACK_COLS["search_cols"],
        _STACK_COLS["output_cols"],
        query,
        max_results,
    )

    return {
        "domain": "stack",
        "stack": stack,
        "query": query,
        "file": STACK_CONFIG[stack]["file"],
        "count": len(results),
        "results": results,
    }
