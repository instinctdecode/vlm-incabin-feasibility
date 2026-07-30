# Run summary (frozen eval set, n=250, Apple M4 Max)

Latency measured on Apple M4 Max — relative comparison only, NOT automotive-SoC performance.

## All runs

| run_id | model | mode | prompt | accuracy | parse_fail_rate | parse_fallback_rate | latency_p50_s | latency_p95_s | peak_memory_gb | model_disk_gb | n |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cnn_mobilenet_v3_small | mobilenet_v3_small | cnn_baseline | - | 0.784 | 0.000 | 0.000 | 0.007 | 0.008 | 2.232 | 0.006 | 250 |
| cnn_resnet18 | resnet18 | cnn_baseline | - | 0.880 | 0.000 | 0.000 | 0.005 | 0.008 | 3.333 | 0.045 | 250 |
| qwen32b-4bit_fs1 | mlx-community/Qwen2.5-VL-32B-Instruct-4bit | fewshot | p1 | 0.496 | 0.000 | 0.000 | 9.398 | 10.112 | 21.031 | 19.825 | 250 |
| qwen32b-4bit_zs_p1 | mlx-community/Qwen2.5-VL-32B-Instruct-4bit | zeroshot | p1 | 0.460 | 0.000 | 0.000 | 5.338 | 5.611 | 20.682 | 19.825 | 250 |
| qwen3b-4bit-base_desc | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | describe | p1 | 0.020 | 0.980 | 0.020 | 0.580 | 0.672 | 3.881 | 3.090 | 250 |
| qwen3b-4bit-ftfull_desc | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | describe | p1 | 0.188 | 0.812 | 0.188 | 0.615 | 1.009 | 4.473 | 3.090 | 250 |
| qwen3b-4bit-ftfull_zs_p1 | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | zeroshot | p1 | 0.844 | 0.000 | 0.000 | 0.784 | 0.815 | 4.434 | 3.090 | 250 |
| qwen3b-4bit-ftfull_zs_p2 | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | zeroshot | p2 | 0.844 | 0.000 | 0.000 | 0.796 | 0.816 | 4.438 | 3.090 | 250 |
| qwen3b-4bit-ftfull_zs_p3 | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | zeroshot | p3 | 0.852 | 0.000 | 0.000 | 0.733 | 0.747 | 4.451 | 3.090 | 250 |
| qwen3b-4bit-ftholdout_desc | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | describe | p1 | 0.096 | 0.872 | 0.000 | 2.876 | 5.143 | 4.473 | 3.090 | 250 |
| qwen3b-4bit-ftholdout_zs_p1 | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | zeroshot | p1 | 0.752 | 0.000 | 0.000 | 0.796 | 0.819 | 4.434 | 3.090 | 250 |
| qwen3b-4bit_fs1 | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | fewshot | p1 | 0.240 | 0.000 | 0.000 | 2.216 | 4.830 | 4.310 | 3.090 | 250 |
| qwen3b-4bit_mf4 | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | multiframe | p1 | 0.432 | 0.000 | 0.000 | 1.156 | 1.211 | 4.269 | 3.090 | 250 |
| qwen3b-4bit_zs_p1 | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | zeroshot | p1 | 0.388 | 0.000 | 0.000 | 0.584 | 0.604 | 4.000 | 3.090 | 250 |
| qwen3b-4bit_zs_p2 | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | zeroshot | p2 | 0.376 | 0.000 | 0.000 | 0.580 | 0.614 | 4.004 | 3.090 | 250 |
| qwen3b-4bit_zs_p3 | mlx-community/Qwen2.5-VL-3B-Instruct-4bit | zeroshot | p3 | 0.264 | 0.064 | 0.000 | 0.640 | 0.701 | 3.928 | 3.090 | 250 |
| qwen3b-bf16_zs_p1 | mlx-community/Qwen2.5-VL-3B-Instruct-bf16 | zeroshot | p1 | 0.388 | 0.000 | 0.000 | 1.201 | 1.349 | 8.260 | 7.525 | 250 |
| qwen72b-4bit_zs_p1 | mlx-community/Qwen2.5-VL-72B-Instruct-4bit | zeroshot | p1 | 0.484 | 0.000 | 0.000 | 10.912 | 11.551 | 43.198 | 42.326 | 250 |
| qwen7b-4bit_fs1 | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | fewshot | p1 | 0.452 | 0.000 | 0.000 | 4.100 | 5.493 | 6.701 | 5.653 | 250 |
| qwen7b-4bit_fusion_high | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | fusion | p1 | 0.412 | 0.000 | 0.000 | 1.512 | 1.611 | 6.459 | 5.653 | 250 |
| qwen7b-4bit_fusion_low | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | fusion | p1 | 0.412 | 0.000 | 0.000 | 1.502 | 1.592 | 6.458 | 5.653 | 250 |
| qwen7b-4bit_fusion_normal | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | fusion | p1 | 0.412 | 0.000 | 0.000 | 1.535 | 1.612 | 6.458 | 5.653 | 250 |
| qwen7b-4bit_mf2 | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | multiframe | p1 | 0.440 | 0.000 | 0.000 | 1.240 | 1.271 | 6.411 | 5.653 | 250 |
| qwen7b-4bit_mf4 | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | multiframe | p1 | 0.460 | 0.000 | 0.000 | 2.047 | 2.102 | 6.741 | 5.653 | 250 |
| qwen7b-4bit_mf8 | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | multiframe | p1 | 0.460 | 0.000 | 0.000 | 3.710 | 3.811 | 7.018 | 5.653 | 250 |
| qwen7b-4bit_zs_p1 | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | zeroshot | p1 | 0.428 | 0.000 | 0.000 | 1.225 | 2.380 | 6.392 | 5.653 | 250 |
| qwen7b-4bit_zs_p2 | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | zeroshot | p2 | 0.428 | 0.000 | 0.000 | 1.258 | 3.521 | 6.392 | 5.653 | 250 |
| qwen7b-4bit_zs_p3 | mlx-community/Qwen2.5-VL-7B-Instruct-4bit | zeroshot | p3 | 0.260 | 0.000 | 0.000 | 1.898 | 2.558 | 6.392 | 5.653 | 250 |
| qwen7b-bf16_zs_p1 | mlx-community/Qwen2.5-VL-7B-Instruct-bf16 | zeroshot | p1 | 0.412 | 0.000 | 0.000 | 2.308 | 2.618 | 17.336 | 16.600 | 250 |
| smolvlm2-4bit_zs_p1 | models/smolvlm2-2.2b-4bit | zeroshot | p1 | 0.108 | 0.000 | 0.000 | 0.975 | 1.221 | 2.911 | 1.862 | 250 |
| smolvlm2-bf16_fs1 | mlx-community/SmolVLM2-2.2B-Instruct-mlx | fewshot | p1 | 0.100 | 0.000 | 0.000 | 19.226 | 27.095 | 11.304 | 4.499 | 250 |
| smolvlm2-bf16_zs_p1 | mlx-community/SmolVLM2-2.2B-Instruct-mlx | zeroshot | p1 | 0.100 | 0.000 | 0.000 | 2.156 | 3.318 | 5.466 | 4.499 | 250 |
| smolvlm2-bf16_zs_p2 | mlx-community/SmolVLM2-2.2B-Instruct-mlx | zeroshot | p2 | 0.100 | 0.000 | 0.000 | 2.069 | 3.301 | 5.466 | 4.499 | 250 |
| smolvlm2-bf16_zs_p3 | mlx-community/SmolVLM2-2.2B-Instruct-mlx | zeroshot | p3 | 0.100 | 0.004 | 0.948 | 4.045 | 5.150 | 5.553 | 4.499 | 250 |

## Per-class accuracy

| run_id | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass |
|---|---|---|---|---|---|---|---|---|---|---|
| cnn_mobilenet_v3_small | 0.64 | 0.68 | 1.00 | 0.64 | 1.00 | 0.88 | 0.80 | 0.96 | 0.76 | 0.48 |
| cnn_resnet18 | 0.96 | 0.88 | 1.00 | 0.80 | 1.00 | 0.92 | 0.96 | 1.00 | 0.80 | 0.48 |
| qwen32b-4bit_fs1 | 0.80 | 0.96 | 1.00 | 0.04 | 0.00 | 0.00 | 0.80 | 0.08 | 0.92 | 0.36 |
| qwen32b-4bit_zs_p1 | 0.80 | 0.64 | 1.00 | 0.24 | 0.00 | 0.04 | 0.80 | 0.00 | 0.92 | 0.16 |
| qwen3b-4bit-base_desc | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.20 | 0.00 | 0.00 | 0.00 |
| qwen3b-4bit-ftfull_desc | 0.00 | 0.16 | 0.24 | 0.16 | 0.68 | 0.00 | 0.60 | 0.00 | 0.00 | 0.04 |
| qwen3b-4bit-ftfull_zs_p1 | 0.36 | 0.88 | 0.84 | 1.00 | 1.00 | 0.96 | 0.84 | 1.00 | 0.88 | 0.68 |
| qwen3b-4bit-ftfull_zs_p2 | 0.40 | 0.88 | 0.84 | 1.00 | 1.00 | 0.96 | 0.80 | 1.00 | 0.88 | 0.68 |
| qwen3b-4bit-ftfull_zs_p3 | 0.44 | 0.88 | 0.84 | 1.00 | 1.00 | 0.96 | 0.84 | 1.00 | 0.88 | 0.68 |
| qwen3b-4bit-ftholdout_desc | 0.00 | 0.20 | 0.00 | 0.64 | 0.04 | 0.00 | 0.04 | 0.00 | 0.04 | 0.00 |
| qwen3b-4bit-ftholdout_zs_p1 | 0.72 | 0.84 | 0.88 | 0.96 | 1.00 | 0.44 | 0.92 | 0.88 | 0.88 | 0.00 |
| qwen3b-4bit_fs1 | 0.12 | 1.00 | 0.96 | 0.00 | 0.00 | 0.00 | 0.20 | 0.00 | 0.12 | 0.00 |
| qwen3b-4bit_mf4 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.48 | 0.00 |
| qwen3b-4bit_zs_p1 | 0.68 | 1.00 | 0.96 | 0.00 | 0.00 | 0.00 | 0.68 | 0.00 | 0.56 | 0.00 |
| qwen3b-4bit_zs_p2 | 0.88 | 1.00 | 0.96 | 0.00 | 0.00 | 0.00 | 0.52 | 0.00 | 0.40 | 0.00 |
| qwen3b-4bit_zs_p3 | 0.00 | 1.00 | 0.64 | 0.00 | 0.00 | 0.00 | 0.68 | 0.00 | 0.32 | 0.00 |
| qwen3b-bf16_zs_p1 | 0.64 | 1.00 | 0.96 | 0.00 | 0.00 | 0.00 | 0.68 | 0.00 | 0.60 | 0.00 |
| qwen72b-4bit_zs_p1 | 0.72 | 0.00 | 0.00 | 0.92 | 0.96 | 0.04 | 0.88 | 0.04 | 0.88 | 0.40 |
| qwen7b-4bit_fs1 | 0.84 | 0.84 | 1.00 | 0.08 | 0.00 | 0.00 | 0.80 | 0.36 | 0.56 | 0.04 |
| qwen7b-4bit_fusion_high | 0.76 | 1.00 | 0.76 | 0.00 | 0.00 | 0.00 | 0.80 | 0.08 | 0.72 | 0.00 |
| qwen7b-4bit_fusion_low | 0.80 | 1.00 | 0.80 | 0.00 | 0.00 | 0.00 | 0.76 | 0.08 | 0.68 | 0.00 |
| qwen7b-4bit_fusion_normal | 0.80 | 1.00 | 0.80 | 0.00 | 0.00 | 0.00 | 0.76 | 0.08 | 0.68 | 0.00 |
| qwen7b-4bit_mf2 | 0.96 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.84 | 0.00 | 0.60 | 0.00 |
| qwen7b-4bit_mf4 | 0.96 | 0.96 | 1.00 | 0.00 | 0.00 | 0.00 | 0.88 | 0.00 | 0.80 | 0.00 |
| qwen7b-4bit_mf8 | 1.00 | 0.92 | 1.00 | 0.00 | 0.00 | 0.00 | 0.88 | 0.00 | 0.80 | 0.00 |
| qwen7b-4bit_zs_p1 | 0.84 | 0.96 | 1.00 | 0.00 | 0.00 | 0.00 | 0.76 | 0.04 | 0.68 | 0.00 |
| qwen7b-4bit_zs_p2 | 0.92 | 1.00 | 0.92 | 0.00 | 0.00 | 0.00 | 0.76 | 0.08 | 0.60 | 0.00 |
| qwen7b-4bit_zs_p3 | 0.08 | 1.00 | 0.76 | 0.00 | 0.04 | 0.00 | 0.68 | 0.00 | 0.04 | 0.00 |
| qwen7b-bf16_zs_p1 | 0.92 | 0.96 | 1.00 | 0.00 | 0.00 | 0.00 | 0.64 | 0.04 | 0.56 | 0.00 |
| smolvlm2-4bit_zs_p1 | 0.08 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| smolvlm2-bf16_fs1 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| smolvlm2-bf16_zs_p1 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| smolvlm2-bf16_zs_p2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| smolvlm2-bf16_zs_p3 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Confusion matrices

**cnn_mobilenet_v3_small** (acc=0.784)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 16 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 4 | 0 |
| text_R | 0 | 17 | 1 | 2 | 0 | 0 | 4 | 0 | 1 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 4 | 0 | 0 | 16 | 0 | 3 | 0 | 0 | 2 | 0 | 0 |
| phone_L | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 0 | 0 | 1 | 0 | 0 | 22 | 0 | 0 | 0 | 2 | 0 |
| drink | 0 | 0 | 0 | 0 | 0 | 0 | 20 | 0 | 4 | 1 | 0 |
| reach_back | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 24 | 1 | 0 | 0 |
| hair_makeup | 0 | 0 | 0 | 0 | 0 | 3 | 1 | 1 | 19 | 1 | 0 |
| talk_pass | 5 | 0 | 1 | 0 | 0 | 6 | 0 | 0 | 1 | 12 | 0 |

**cnn_resnet18** (acc=0.88)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| text_R | 0 | 22 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 3 | 0 | 0 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 2 | 0 | 0 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 0 |
| drink | 1 | 0 | 0 | 0 | 0 | 0 | 24 | 0 | 0 | 0 | 0 |
| reach_back | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 |
| hair_makeup | 1 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 20 | 1 | 0 |
| talk_pass | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 12 | 0 |

**qwen32b-4bit_fs1** (acc=0.496)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 20 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| text_R | 0 | 24 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 23 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| phone_L | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| radio | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 |
| drink | 0 | 1 | 0 | 1 | 0 | 0 | 20 | 0 | 0 | 3 | 0 |
| reach_back | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 4 | 0 |
| hair_makeup | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 23 | 1 | 0 |
| talk_pass | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 |

**qwen32b-4bit_zs_p1** (acc=0.46)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 20 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| text_R | 0 | 16 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 19 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 22 | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 0 |
| radio | 19 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 4 | 0 |
| drink | 0 | 1 | 1 | 0 | 0 | 0 | 20 | 0 | 0 | 3 | 0 |
| reach_back | 21 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |
| hair_makeup | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 23 | 0 | 0 |
| talk_pass | 20 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |

**qwen3b-4bit-base_desc** (acc=0.02)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| text_R | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| phone_R | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| text_L | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| phone_L | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| radio | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| drink | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 20 |
| reach_back | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| hair_makeup | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| talk_pass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |

**qwen3b-4bit-ftfull_desc** (acc=0.188)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| text_R | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 21 |
| phone_R | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 19 |
| text_L | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 21 |
| phone_L | 0 | 0 | 0 | 0 | 17 | 0 | 0 | 0 | 0 | 0 | 8 |
| radio | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| drink | 0 | 0 | 0 | 0 | 0 | 0 | 15 | 0 | 0 | 0 | 10 |
| reach_back | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| hair_makeup | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| talk_pass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 24 |

**qwen3b-4bit-ftfull_zs_p1** (acc=0.844)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 9 | 0 | 0 | 2 | 0 | 5 | 0 | 0 | 0 | 9 | 0 |
| text_R | 0 | 22 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 21 | 0 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| text_L | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 0 | 0 | 0 | 0 | 0 | 24 | 0 | 0 | 0 | 1 | 0 |
| drink | 0 | 2 | 0 | 0 | 0 | 0 | 21 | 0 | 2 | 0 | 0 |
| reach_back | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 |
| hair_makeup | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 22 | 1 | 0 |
| talk_pass | 2 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 17 | 0 |

**qwen3b-4bit-ftfull_zs_p2** (acc=0.844)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 10 | 0 | 0 | 2 | 0 | 3 | 0 | 0 | 0 | 10 | 0 |
| text_R | 0 | 22 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 21 | 0 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| text_L | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 0 | 0 | 0 | 0 | 0 | 24 | 0 | 0 | 0 | 1 | 0 |
| drink | 0 | 2 | 0 | 0 | 0 | 0 | 20 | 0 | 3 | 0 | 0 |
| reach_back | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 |
| hair_makeup | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 22 | 1 | 0 |
| talk_pass | 2 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 17 | 0 |

**qwen3b-4bit-ftfull_zs_p3** (acc=0.852)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 11 | 0 | 0 | 2 | 0 | 4 | 0 | 0 | 0 | 8 | 0 |
| text_R | 0 | 22 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 21 | 0 | 3 | 0 | 0 | 0 | 1 | 0 | 0 |
| text_L | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 0 | 0 | 0 | 0 | 0 | 24 | 0 | 0 | 0 | 1 | 0 |
| drink | 0 | 3 | 0 | 0 | 0 | 0 | 21 | 0 | 1 | 0 | 0 |
| reach_back | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 |
| hair_makeup | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 22 | 1 | 0 |
| talk_pass | 2 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 17 | 0 |

**qwen3b-4bit-ftholdout_desc** (acc=0.096)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| text_R | 0 | 5 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 14 |
| phone_R | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 24 |
| text_L | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| phone_L | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 24 |
| radio | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| drink | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 23 |
| reach_back | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |
| hair_makeup | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 24 |
| talk_pass | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 |

**qwen3b-4bit-ftholdout_zs_p1** (acc=0.752)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 18 | 4 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 21 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 22 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 1 | 0 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 10 | 0 | 0 | 0 | 0 | 11 | 1 | 3 | 0 | 0 | 0 |
| drink | 0 | 1 | 0 | 0 | 0 | 0 | 23 | 0 | 1 | 0 | 0 |
| reach_back | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0 | 0 |
| hair_makeup | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 22 | 0 | 0 |
| talk_pass | 23 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |

**qwen3b-4bit_fs1** (acc=0.24)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 3 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 1 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 4 | 21 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 7 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 7 | 0 | 13 | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| reach_back | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 1 | 11 | 5 | 3 | 0 | 0 | 0 | 0 | 3 | 2 | 0 |
| talk_pass | 5 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**qwen3b-4bit_mf4** (acc=0.432)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 1 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 1 | 3 | 0 | 0 | 0 | 21 | 0 | 0 | 0 | 0 |
| reach_back | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 8 | 0 | 2 | 2 | 0 | 0 | 1 | 0 | 12 | 0 | 0 |
| talk_pass | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**qwen3b-4bit_zs_p1** (acc=0.388)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 17 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 1 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 2 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 19 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 7 | 1 | 0 | 0 | 0 | 17 | 0 | 0 | 0 | 0 |
| reach_back | 11 | 13 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 3 | 6 | 2 | 0 | 0 | 0 | 0 | 0 | 14 | 0 | 0 |
| talk_pass | 20 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**qwen3b-4bit_zs_p2** (acc=0.376)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 22 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 1 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 2 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 22 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 5 | 6 | 1 | 0 | 0 | 0 | 13 | 0 | 0 | 0 | 0 |
| reach_back | 20 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 9 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 |
| talk_pass | 21 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**qwen3b-4bit_zs_p3** (acc=0.264)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 0 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 3 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 4 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| radio | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 7 | 1 | 0 | 0 | 0 | 17 | 0 | 0 | 0 | 0 |
| reach_back | 0 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| hair_makeup | 0 | 10 | 2 | 0 | 0 | 0 | 0 | 4 | 8 | 0 | 1 |
| talk_pass | 0 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |

**qwen3b-bf16_zs_p1** (acc=0.388)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 16 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 1 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 1 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 18 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 7 | 1 | 0 | 0 | 0 | 17 | 0 | 0 | 0 | 0 |
| reach_back | 10 | 14 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 1 | 5 | 3 | 0 | 0 | 0 | 1 | 0 | 15 | 0 | 0 |
| talk_pass | 14 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**qwen72b-4bit_zs_p1** (acc=0.484)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 0 |
| text_R | 0 | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 0 | 0 | 24 | 0 | 0 | 0 | 1 | 0 | 0 |
| text_L | 0 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| phone_L | 0 | 0 | 0 | 0 | 24 | 0 | 0 | 0 | 1 | 0 | 0 |
| radio | 15 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 8 | 0 |
| drink | 0 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 2 | 1 | 0 |
| reach_back | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 8 | 11 | 0 |
| hair_makeup | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 22 | 1 | 0 |
| talk_pass | 11 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 3 | 10 | 0 |

**qwen7b-4bit_fs1** (acc=0.452)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 21 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 |
| text_R | 0 | 21 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 23 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 23 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 3 | 0 | 2 | 0 | 0 | 20 | 0 | 0 | 0 | 0 |
| reach_back | 14 | 0 | 0 | 1 | 0 | 0 | 0 | 9 | 1 | 0 | 0 |
| hair_makeup | 1 | 0 | 9 | 0 | 0 | 1 | 0 | 0 | 14 | 0 | 0 |
| talk_pass | 17 | 1 | 0 | 4 | 0 | 0 | 0 | 2 | 0 | 1 | 0 |

**qwen7b-4bit_fusion_high** (acc=0.412)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 19 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 6 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 3 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 22 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 5 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 0 | 0 |
| reach_back | 20 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| hair_makeup | 0 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 18 | 0 | 0 |
| talk_pass | 17 | 7 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

**qwen7b-4bit_fusion_low** (acc=0.412)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 20 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 5 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 3 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 23 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 1 | 5 | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| reach_back | 21 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| hair_makeup | 1 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 17 | 0 | 0 |
| talk_pass | 18 | 6 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

**qwen7b-4bit_fusion_normal** (acc=0.412)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 20 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 5 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 3 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 23 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 1 | 5 | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| reach_back | 21 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| hair_makeup | 1 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 17 | 0 | 0 |
| talk_pass | 17 | 7 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

**qwen7b-4bit_mf2** (acc=0.44)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 24 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 20 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 2 | 2 | 0 | 0 | 0 | 21 | 0 | 0 | 0 | 0 |
| reach_back | 18 | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 1 | 3 | 3 | 2 | 1 | 0 | 0 | 0 | 15 | 0 | 0 |
| talk_pass | 23 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**qwen7b-4bit_mf4** (acc=0.46)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 24 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 24 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 1 | 2 | 0 | 0 | 0 | 22 | 0 | 0 | 0 | 0 |
| reach_back | 22 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 1 | 1 | 2 | 1 | 0 | 0 | 0 | 0 | 20 | 0 | 0 |
| talk_pass | 23 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**qwen7b-4bit_mf8** (acc=0.46)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 23 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 1 | 2 | 0 | 0 | 0 | 22 | 0 | 0 | 0 | 0 |
| reach_back | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 20 | 0 | 0 |
| talk_pass | 24 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**qwen7b-4bit_zs_p1** (acc=0.428)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 21 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 24 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 21 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 4 | 0 | 2 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| reach_back | 20 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| hair_makeup | 0 | 3 | 4 | 1 | 0 | 0 | 0 | 0 | 17 | 0 | 0 |
| talk_pass | 18 | 4 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

**qwen7b-4bit_zs_p2** (acc=0.428)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 23 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 1 | 23 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 1 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 24 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 1 | 5 | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| reach_back | 22 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| hair_makeup | 2 | 6 | 2 | 0 | 0 | 0 | 0 | 0 | 15 | 0 | 0 |
| talk_pass | 20 | 3 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

**qwen7b-4bit_zs_p3** (acc=0.26)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 2 | 6 | 0 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 3 | 19 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 14 | 10 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 4 | 4 | 0 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 7 | 0 | 1 | 0 | 0 | 17 | 0 | 0 | 0 | 0 |
| reach_back | 2 | 3 | 0 | 19 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 0 | 12 | 0 | 11 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| talk_pass | 4 | 5 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**qwen7b-bf16_zs_p1** (acc=0.412)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 23 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 24 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 23 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 1 | 3 | 2 | 3 | 0 | 0 | 16 | 0 | 0 | 0 | 0 |
| reach_back | 22 | 0 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| hair_makeup | 1 | 0 | 7 | 3 | 0 | 0 | 0 | 0 | 14 | 0 | 0 |
| talk_pass | 18 | 0 | 0 | 6 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

**smolvlm2-4bit_zs_p1** (acc=0.108)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 2 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 1 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| reach_back | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| talk_pass | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**smolvlm2-bf16_fs1** (acc=0.1)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| reach_back | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| talk_pass | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**smolvlm2-bf16_zs_p1** (acc=0.1)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| reach_back | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| talk_pass | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**smolvlm2-bf16_zs_p2** (acc=0.1)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| reach_back | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| talk_pass | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**smolvlm2-bf16_zs_p3** (acc=0.1)

| true\pred | safe | text_R | phone_R | text_L | phone_L | radio | drink | reach_back | hair_makeup | talk_pass | FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safe | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_R | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_R | 24 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| text_L | 24 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| phone_L | 24 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| radio | 23 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drink | 23 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| reach_back | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hair_makeup | 23 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| talk_pass | 23 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
