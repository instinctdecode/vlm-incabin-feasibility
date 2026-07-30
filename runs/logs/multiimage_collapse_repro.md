# Multi-image generation collapse on MLX stack (mlx-vlm 0.6.7, mlx 0.32.0)

Measured 2026-07-25, Apple M4 Max 128GB, temperature=0.0.
Symptom: with total prompt tokens ≳2.5k from many images, Qwen2.5-VL 3B/7B
4bit generate degenerate output (immediate EOS, or repeated `<|im_start|>` /
`addCriterion` tokens). Same prompts with fewer/smaller images work.

| model | images | prompt_tokens | result |
|---|---|---|---|
| 3B-4bit | 10 ex@448 + query@640x480 (11) | 2691 | empty (EOS at token 1) |
| 3B-4bit | 10 ex@448 + query (11, interleaved) | ~2.6k | `<|im_start|>` loop |
| 7B-4bit | 10 ex@448 + query (11, interleaved) | 2621 | ` addCriterion` garbage |
| 3B-4bit | 10 ex@224 + query (11, interleaved) | 1181 | OK `{"class_id": "c1"}` |
| 7B-4bit | 2 frames @640x480 | 1034 | OK |
| 7B-4bit | 4 frames @640x480 | 1820 | OK |
| 7B-4bit | 8 frames @640x480 | 3392 | `<|im_start|>` + garbage |

Consequence for experiments:
- few-shot: example images downsized to max-side 224 (interleaved image-label
  format) — recorded in run configs.
- multiframe: ALL frames downsized to max-side 448 uniformly for mf2/mf4/mf8.
- The collapse itself is reported as a deployment-stack risk finding
  (stage 5 / parsing-reliability sections).
