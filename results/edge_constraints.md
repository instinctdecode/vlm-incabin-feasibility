# 차량용 엣지 제약 조사 종합 (단계 6 기초 자료)

전 항목 공개 자료 기반, 조회일 2026-07-25. 원시 주장·인용문·검증 판정은
`results/edge_research.json` (63개 주장 중 59개 교차 확인, 1개 정정, 3개 미검증 표기).

## 1. 차량 SoC 메모리·연산 예산

| 플랫폼 | AI 성능 | 메모리(레퍼런스/양산) | 출처 |
|---|---|---|---|
| Qualcomm SA8155P (콕핏, 양산 다수) | >10 TOPS | 개발보드 8GB LPDDR4X; Li Auto L9 양산차는 SA8155P×2에 24GB | [qualcomm.com PDF](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qul7413_sa8155_productbrief_r4.pdf), [thundercomm.com](https://www.thundercomm.com/product/sa8155p-automotive-development-platform/), [arenaev.com](https://m.arenaev.com/li_li_l9_interior_teased_to_debut_during_this_years_beijing_auto_show-news-76.php) |
| Qualcomm SA8295P (콕핏, 현행 상위) | 30 TOPS NPU | 개발보드 16GB LPDDR4X | [cnevpost.com](https://cnevpost.com/2021/11/29/jidus-first-model-to-feature-qualcomm-snapdragon-8295-chip-based-on-5nm-process/), [lantronix.com PDF](https://cdn.lantronix.com/wp-content/uploads/pdf/MPB-00130-RevB-SA8295P-A4.pdf) |
| TI TDA4VM (DMS/전방 ADAS 대표) | 8 TOPS (8bit) | 레퍼런스 킷 4GB LPDDR4 | [ti.com](https://www.ti.com/product/TDA4VM), [ti.com/tool](https://www.ti.com/tool/SK-TDA4VM) |
| TI TDA4VH | 32 TOPS | LPDDR4 4채널 | [ti.com](https://www.ti.com/product/TDA4VH-Q1) |
| NVIDIA DRIVE Orin (고급 ADAS 도메인) | 254 TOPS | 32/64GB LPDDR5 | [nvidia.com](https://www.nvidia.com/en-us/self-driving-cars/in-vehicle-computing/), [nvidia.com/jetson](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) |
| NVIDIA DRIVE Thor (차세대) | 1,000+ INT8 TOPS | 64GB LPDDR5X | [edge-ai-vision.com](https://www.edge-ai-vision.com/2025/09/accelerate-autonomous-vehicle-development-with-the-nvidia-drive-agx-thor-developer-kit/) |

**DMS가 실제로 쓰는 몫**: DMS는 SoC를 IVI/클러스터와 공유한다. 정량 공개 사례 —
Cipia Driver Sense(Euro NCAP 대응 기본형)는 Ambarella CV28에서 **AI 엔진의 10%,
Arm 코어의 50%만 사용**(고급형: AI 35%/Arm 60%)
([prnewswire](https://www.prnewswire.com/il/news-releases/cipias-driver-sense-dms-now-available-on-ambarellas-cv28-automotive-soc-301533978.html)).
→ 현행 DMS의 실효 예산은 "전용 SoC 전부"가 아니라 **수 TOPS·기가바이트 미만~수 GB 수준**으로 보는 것이 합리적.

## 2. NPU 트랜스포머/VLM 지원 현황 (2026-07 기준)

| 벤더/툴체인 | 상태 | 근거 |
|---|---|---|
| TI TIDL (TDA4x) | ViT/DeiT 지원은 SDK 9.1(2024-01)부터, 현 11.x에서 Attention MatMul/Softmax 제한 'None'이지만 LayerNorm은 W축만, Erf는 GELU 패턴 안에서만 — **연산자 제약 잔존, LLM/VLM급 배치 사례 없음** | [github TIDL 9.1](https://github.com/TexasInstruments/edgeai-tidl-tools/blob/09_01_00_05/docs/tidl_fsg_vtfr.md), [github master](https://github.com/TexasInstruments/edgeai-tidl-tools/blob/master/docs/vision_transformers.md) |
| Qualcomm AI Hub (SA8255P/8295P/8650P/8775P) | **Llama-3.2-1B/3B 4bit이 자동차 칩셋 공식 카탈로그에 등재** — 콕핏 NPU에서 LLM 실행이 공식 지원 영역에 진입 | [aihub.qualcomm.com](https://aihub.qualcomm.com/automotive/models), [Llama 1B 페이지](https://aihub.qualcomm.com/automotive/models/llama_v3_2_1b_instruct) |
| Qualcomm Ride Elite / Cockpit Elite | 백서에서 "large VLM + end-to-end transformer 호스팅" 명시(차세대) | [qualcomm.com PDF](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-Ride-GLOBAL-whitepaper.pdf) |
| Ambarella CV3-AD/N1 | CES 2025에서 CV3-AD 위 LLM 장면 서술 데모; N1은 1~34B 멀티모달 LLM(Llama2-13B 25tok/s, <50W), N1-655은 LLaVA-OneVision 등 지원 | [ambarella.com](https://www.ambarella.com/news/ambarella-brings-generative-ai-capabilities-to-edge-devices-introduces-n1-system-on-chip-series-for-on-premise-applications/), [blog](https://www.ambarella.com/blog/advancing-genai-at-the-edge-during-ces-2025/) |
| Cerence CaLLM Edge | 3.8B(Phi-3 기반) 4bit **차량 임베디드 SLM 양산 지향 발표**(2024-11) — 텍스트 전용이지만 "3~4B 4bit"이 차량 임베디드의 현실적 상한 시사 | [globenewswire](https://www.globenewswire.com/news-release/2024/11/13/2980461/0/en/Cerence-Introduces-Pioneering-Embedded-Small-Language-Model-Purpose-Built-for-Automotive.html) |
| NXP i.MX95 eIQ | GenAI Flow로 LLM 빌딩블록 제공(2024-11) | [github NXP](https://github.com/nxp-appcodehub/dm-eiq-genai-flow-demonstrator/blob/main/eiq_genai_flow/README.md) |
| Renesas R-Car V4H | CNN 가속기 중심, 트랜스포머 지원 공개 언급 없음(조회일 기준). 차세대 X5H(400 TOPS, 3nm)부터 생성형 AI 명시 | [renesas.com](https://www.renesas.com/en/products/r-car-v4h), [Gen5 발표](https://www.renesas.com/en/about/newsroom/renesas-fast-tracks-sdv-innovation-r-car-gen-5-soc-based-end-end-multi-domain-solution-platform) |

## 3. 실시간 요구사항 (규제·평가 프로토콜)

- **Euro NCAP Safe Driving/Driver Engagement v1.1** (2025-10, 시행 2026-01):
  Long Distraction = 전방 이탈 시선 3~4초, Short Distraction(VATS) = 30초 창에서
  누적 10초, 마이크로슬립 = 눈감김 1~2초, 수면 = ≥3초, 무반응 = 경고 후 3초 내
  시선 미복귀 또는 눈감김 ≥6초. 조명 1~100,000 lux, 연령 16~80, 피부톤 전 범위
  강건성 요구. ([euroncap.com PDF](https://cdn.euroncap.com/cars/assets/euro_ncap_protocol_safe_driving_driver_engagement_v11_a30e874152.pdf))
- **EU GSR 2019/2144 하위규정**: DDAW(2021/1341) — KSS≥8 경고, 70km/h 이상 자동
  활성, 민감도>40% 검증, PERCLOS 대체 지표 인정. ADDW(2023/2590) — 주의분산
  영역 응시 50km/h 이상에서 최대 3.5초(20~50km/h는 6초) 내 경고, 시선 이벤트
  50ms 분해능 허용, 경고 4초 내 미발령 시 false negative. 2024-07부터 신규
  차량형식 의무. ([EUR-Lex 2021/1341](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32021R1341), [EUR-Lex 2023/2590](https://eur-lex.europa.eu/legal-content/en/TXT/PDF/?uri=OJ%3AL_202302590))
- **PERCLOS**: 1분 창에서 눈이 80% 이상 감긴 시간 비율(Wierwille 1994; FHWA TB 98-006).
  ([ntlrepository PDF](https://ntlrepository.blob.core.windows.net/lib/51000/51300/51369/tb98-006.pdf))
- **DMS 카메라**: OV2311급 2MP 글로벌셔터, 최대 60fps, 940nm NIR 조명이 표준.
  ([ovt.com](https://www.ovt.com/products/ov2311/), [ams-osram.com](https://ams-osram.com/applications/automotive-mobility/in-cabin-sensing))
- 시사점: **시선/눈감김 계열 판정은 50ms 분해능 + 초 단위 누적 창**을 요구 →
  프레임 파이프라인은 실질 30~60fps(프레임당 수십 ms) 수준. 행동 분류(본 검토
  과제)는 이보다 완화된 1~수 Hz로도 규정 창(3.5초) 안에 들어올 수 있음.

## 4. 엣지 하드웨어에서의 소형 VLM 실측 공개 벤치마크

- Jetson Orin Nano 8GB (NVIDIA 공식, JetPack 6.2): Qwen2-VL-2B 2.8→4.4 tok/s,
  SmolVLM-2B 8.1→12.9 tok/s, **LLaVA-1.6-7B INT4 0.41→0.57 tok/s** —
  7B급은 8GB 엣지 모듈에서 대화형조차 곤란.
  ([developer.nvidia.com](https://developer.nvidia.com/blog/nvidia-jetson-orin-nano-developer-kit-gets-a-super-boost/))
- Qwen2-VL-7B: BF16 16.07GB / INT8 10.11GB / INT4 7.20GB (A100 측정, 공식 모델카드).
  ([huggingface.co](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct-AWQ))
- 스마트폰급: Qualcomm이 MWC 2024에서 7B+ LLaVA 온디바이스 데모(정량 미공개).
  ([edge-ai-vision.com](https://www.edge-ai-vision.com/2024/02/qualcomm-continues-to-bring-the-generative-ai-revolution-to-devices-and-empowers-developers-with-qualcomm-ai-hub/))
- LiteVLM(DRIVE Thor, arXiv:2506.07416): 파이프라인 최적화로 E2E 지연 2.5×↓(FP8 3.2×).
- 참고 학술 결과: 미세조정 CLIP(단일 프레임)이 StateFarm 83.15%
  (arXiv:2306.10159); 2026년 연구는 "대형 VLM은 상시 모니터로 부적합 → 11.39M
  경량 학생 모델로 증류 + 희소 VLM 호출" 구조 제안(arXiv:2606.26922) — 본 검토의
  하이브리드 경로와 일치.

## 5. 예산선 도출 (보고서 §6에서 사용)

- **현행 콕핏/DMS 현실 예산**: DMS 몫으로 볼 수 있는 메모리는 대략 **1~4GB**
  (TDA4VM 킷 전체가 4GB, SA8155P 보드 8GB에서 IVI/클러스터와 공유, Cipia 사례처럼
  DMS는 SoC 일부만 배정). AI 연산은 수 TOPS 수준.
- **차세대(발표 기준) 상위 플랫폼**: Cockpit Elite/Ride Elite, Thor, X5H —
  VLM 호스팅을 명시하나 양산차 DMS 배치 사례는 조회일 기준 미확인.
- 임베디드 언어모델의 공개 선례 상한: **3.8B/4bit(Cerence CaLLM Edge)**,
  자동차 공식 카탈로그 LLM: **1B/3B 4bit(Qualcomm AI Hub)**.
