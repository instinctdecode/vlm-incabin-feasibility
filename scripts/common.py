"""Shared definitions: class taxonomy, prompts, JSON parsing.

Dataset: State Farm Distracted Driver Detection (10-class driver state).
NOTE: This project uses only public data. No proprietary/company data.
"""
import json
import re

CLASSES = {
    "c0": "safe driving (both hands on wheel, eyes on road)",
    "c1": "texting with right hand (looking at phone held in right hand)",
    "c2": "talking on the phone with right hand (phone held to right ear)",
    "c3": "texting with left hand (looking at phone held in left hand)",
    "c4": "talking on the phone with left hand (phone held to left ear)",
    "c5": "operating the radio / center console (hand reaching to dashboard controls)",
    "c6": "drinking (holding a cup or bottle to mouth)",
    "c7": "reaching behind (arm reaching to back seat)",
    "c8": "hair and makeup (touching hair or face grooming)",
    "c9": "talking to passenger (head turned toward passenger seat)",
}
CLASS_IDS = list(CLASSES.keys())

# Short names for confusion-matrix axes / reports
SHORT = {
    "c0": "safe", "c1": "text_R", "c2": "phone_R", "c3": "text_L",
    "c4": "phone_L", "c5": "radio", "c6": "drink", "c7": "reach_back",
    "c8": "hair_makeup", "c9": "talk_pass",
}

_CLASS_BLOCK = "\n".join(f"- {cid}: {desc}" for cid, desc in CLASSES.items())
_CLASS_BLOCK_TERSE = "\n".join(
    f"- {cid}: {desc.split('(')[0].strip()}" for cid, desc in CLASSES.items()
)

# ---------------------------------------------------------------- prompts
# P1: primary prompt (used for the main size-vs-accuracy curve)
PROMPT_P1 = f"""You are a driver monitoring system analyzing an in-cabin camera image of a driver.

Classify the driver's current state into exactly one of these classes:
{_CLASS_BLOCK}

Answer with ONLY a JSON object, no other text:
{{"class_id": "<one of c0..c9>"}}"""

# P2: paraphrase — different framing/wording, same task (prompt sensitivity)
PROMPT_P2 = f"""Look at this photo taken inside a car showing the driver.

What is the driver doing? Pick the single best matching category:
{_CLASS_BLOCK}

Respond with valid JSON only in this exact format:
{{"class_id": "c0"}}
Replace c0 with your chosen class id. Output nothing except the JSON."""

# P3: terse — minimal instruction (prompt sensitivity)
PROMPT_P3 = f"""Classify the driver state:
{_CLASS_BLOCK_TERSE}

JSON only: {{"class_id": "cX"}}"""

PROMPTS = {"p1": PROMPT_P1, "p2": PROMPT_P2, "p3": PROMPT_P3}

# Multi-frame variant (stage 5)
def prompt_multiframe(n_frames: int) -> str:
    return f"""You are a driver monitoring system. You are given {n_frames} consecutive frames (in temporal order) from an in-cabin camera watching the driver.

Considering the whole sequence, classify the driver's sustained state into exactly one of:
{_CLASS_BLOCK}

Answer with ONLY a JSON object, no other text:
{{"class_id": "<one of c0..c9>"}}"""

# Fusion variant (stage 7).
# WARNING: heart-rate values injected with this prompt are SYNTHETIC test
# context, NOT real measurements. See report section 7.
def prompt_fusion(hr_bpm: int) -> str:
    return f"""You are a driver monitoring system analyzing an in-cabin camera image of a driver.

Additional sensor context: the driver's current heart rate is {hr_bpm} bpm.

Task 1 — classify the driver's visible activity into exactly one of:
{_CLASS_BLOCK}

Task 2 — combining the image and the heart-rate context, rate the driver's arousal state as one of: "low" (drowsy-risk range), "normal", "elevated" (stress/agitation range).

Answer with ONLY a JSON object, no other text:
{{"class_id": "<c0..c9>", "arousal": "<low|normal|elevated>"}}"""

# ---------------------------------------------------------------- parsing
_JSON_RE = re.compile(r"\{[^{}]*\}")
_CID_RE = re.compile(r"\bc[0-9]\b")

def parse_prediction(text: str):
    """Parse model output. Returns (class_id|None, parse_mode, extra_dict).

    parse_mode: 'strict'   — valid JSON with a valid class_id field
                'fallback' — class id recovered from free text
                'fail'     — no class id recoverable
    """
    text = text.strip()
    # strip common markdown fences
    fenced = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    for candidate in (fenced, text):
        m = _JSON_RE.search(candidate)
        if not m:
            continue
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        cid = obj.get("class_id") or obj.get("class") or obj.get("classId")
        if isinstance(cid, str):
            cid = cid.strip().lower()
            if cid in CLASSES:
                return cid, "strict", obj
            m2 = _CID_RE.search(cid)
            if m2:
                return m2.group(0), "strict", obj
    # fallback: any bare cX token in the raw text
    m3 = _CID_RE.search(text.lower())
    if m3:
        return m3.group(0), "fallback", {}
    # fallback: class-name keyword match (very loose, last resort)
    tl = text.lower()
    for cid, desc in CLASSES.items():
        key = desc.split("(")[0].strip()
        if key in tl:
            return cid, "fallback", {}
    return None, "fail", {}
