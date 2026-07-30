# Upstream issue draft — mlx-vlm chunked-prefill degeneration

- **Target repo**: https://github.com/Blaizzy/mlx-vlm (bug localized to mlx-vlm:
  same prompt through mlx-lm works; mlx core unaffected)
- **Submit URL**: https://github.com/Blaizzy/mlx-vlm/issues/new
- **Related (reference in the body, not duplicates of this exact report)**:
  #1639 (closed as fixed, but the reporter's token-threshold follow-up — 1,352 tok
  OK / 2,434 tok garbage — was never addressed and matches this bug), PR #1332
  (fixed the analogous chunked-prefill bug for Qwen3-VL deepstack only),
  PR #1527 / #1486 / #1143 (history of Qwen M-RoPE position-state bugs).
- Alternative to a new issue: comment on #1639 asking to reopen, attaching the
  evidence below. A new issue with a precise title is likely clearer since #1639
  was framed as a checkpoint-corruption bug.

---

## TITLE

Qwen2.5-VL: any prompt longer than `prefill_step_size` (default 2048) degenerates — empty output or `<|im_start|>` repetition; text-only and multi-image, bf16 and 4-bit, 0.6.7 and current main

## BODY

### Describe the bug

With Qwen2.5-VL models, **any prompt whose length exceeds `prefill_step_size`
(default 2048) produces degenerate output at temperature 0**: either an
immediate EOS (empty string) or endless `<|im_start|>` / `addCriterion`
repetition. The trigger is chunked prefill itself, not the content
(full log: `repro_log.txt`, all runs below are in it):

- happens with **many images** (e.g. 11 images at 448×336 = 2,165 tokens) and
  with **text-only** prompts (4,338 tokens) alike;
- happens on **bf16 and 4-bit** checkpoints, 3B and 7B (log sections 2-3; the
  7B failure emits ` addCriterion` — the same signature reported in #1639) —
  so not quantization / not checkpoint corruption;
- flipping **only** `prefill_step_size` flips the bug both ways:
  - 2,165-token prompt + `prefill_step_size=8192` (chunking off) → **OK**
  - 1,195-token prompt (fine by default) + `prefill_step_size=512` → **DEGENERATE**
- the same text through **mlx-lm** 0.31.3 (`mlx-community/Qwen2.5-3B-Instruct-4bit`,
  4,348 tokens under its chat template, same default chunked prefill)
  → **OK** (log line 15), so this is mlx-vlm's model implementation, not
  mlx / mlx-lm.

### To Reproduce

Self-contained script (generates its own synthetic images):
[repro_multiimage_collapse.py] — attached / gist.

```
python repro_multiimage_collapse.py --model mlx-community/Qwen2.5-VL-3B-Instruct-4bit --with-mlx-lm-control
```

Output on mlx-vlm 0.6.7 (abridged — k=2,4,8,12 lines omitted; full log attached;
git main @ 2026-07-26 (0.6.8) reruns of control/k=10/k=11/all three toggles give
the same results, log section 4):

```
[control text-only ~4338 tok] -> DEGENERATE(repetition)   out='<|im_start|>\n<|im_start|>\n<|im_start|>\n'
[k= 1 images,   225 prompt tok] -> OK                       out='4'
[k= 6 images,  1195 prompt tok] -> OK                       out='5'
[k=10 images,  1971 prompt tok] -> OK                       out='10'
[k=11 images,  2165 prompt tok] -> DEGENERATE(repetition)   out='<|im_start|>\n<|im_start|>\n...'
[k=14 images,  2747 prompt tok] -> DEGENERATE(empty)        out=''
[k=11 images,  2165 tok, prefill=8192] -> OK                out='10' (long prompt, chunking OFF)
[k= 6 images,  1195 tok, prefill=512] -> DEGENERATE(repetition)     (short prompt, chunking FORCED)
[text-only ~4.3k tok, prefill=8192] -> OK                   out='4'  (text-only, chunking OFF)
[control mlx-lm 0.31.3 text-only 4348 tok, default chunking] -> OK  out='4'
```

Minimal inline version:

```python
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config

model, processor = load("mlx-community/Qwen2.5-VL-3B-Instruct-4bit")
config = load_config("mlx-community/Qwen2.5-VL-3B-Instruct-4bit")
long_text = ("The quick brown fox jumps over the lazy dog. " * 430
             + "\nAfter all that text: what is 2+2? Answer with just the number.")
prompt = apply_chat_template(processor, config, long_text, num_images=0)
r = generate(model, processor, prompt, image=[], max_tokens=24, temperature=0.0)
print(repr(r.text))   # '<|im_start|>\n<|im_start|>\n...'  (expected: '4')
r = generate(model, processor, prompt, image=[], max_tokens=24, temperature=0.0,
             prefill_step_size=8192)
print(repr(r.text))   # '4'
```

### Expected behavior

Chunked prefill should be output-invariant: the same prompt must generate the
same (correct) answer regardless of `prefill_step_size`.

### Analysis (as far as I could trace it)

The chunked-prefill loop in `mlx_vlm/generate/ar.py` slices `input_ids` /
`inputs_embeds` per chunk and calls `model.language_model(...)` per slice. In
`mlx_vlm/models/qwen2_5_vl/language.py::LanguageModel.__call__`, the M-RoPE
position state (`self._position_ids`, `self._rope_deltas`) is computed by
`get_rope_index(...)` **on the first chunk only** (the `cache_offset == 0`
branch sees only the first ≤2048 tokens). Later chunks take the
decode-style else-branch, which linearly extends positions
(`arange(seq_length) + cache_offset + rope_deltas`). Consequences:

- image tokens that fall in chunk 2+ get flat text-style positions instead of
  3D M-RoPE grid positions, and `rope_deltas` is computed from an incomplete
  sequence;
- empirically even text-only prompts degenerate once chunking engages, so the
  cross-chunk position/state bookkeeping appears wrong in general for this
  model family.

This looks like the same class of bug as PR #1332, which fixed
"visual embeds misaligned during chunked prefill" for **Qwen3-VL** — there
seems to be no analogous fix for `qwen2_5_vl`. It also likely explains the
unresolved tail of #1639: the reporter's follow-up shows 605/1,352-token
prompts OK and 2,434/2,720/3,755-token prompts producing `addCriterion`
garbage — exactly the `prefill_step_size=2048` boundary — but the issue was
closed after a short-prompt verification.

### Workaround

Pass `prefill_step_size` ≥ prompt length (e.g. `8192`), or keep prompts under
2,048 tokens (downscale/reduce images). Memory cost of unchunked prefill was
acceptable in my tests (3B/7B on 128GB).

### Environment

- mlx-vlm: 0.6.7 (PyPI) and git main @ 2026-07-26 (0.6.8)
- mlx: 0.32.0, mlx-lm: 0.31.3 (control; log line 15)
- macOS 26.5.2 (Darwin 25.5.0), Apple M4 Max, 128GB
- Python 3.12.13
- Models: mlx-community/Qwen2.5-VL-3B-Instruct-4bit, -bf16, 7B-Instruct-4bit
  (each reproduced — log sections 1–3)
- temperature 0.0, max_tokens 24
