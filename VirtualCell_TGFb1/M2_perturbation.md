# M2 · 질환특화 perturbation 레이어 (빌드 계획)

> **목표:** "TGFβ를 *가했을 때*" fibroblast 상태가 어떻게 이동하는지 예측/검증.
> M1이 던진 질문에 답한다 — 만성 스냅샷에선 TGFβ 신호가 평탄했다(`04_results.md`).
> perturbation으로 **급성 TGFβ 활성 readout**을 살려야 binder(M4) 효과를 읽을 수 있다.
> 전략: 오픈 FM(Arc STATE)을 인프라로, TGFβ perturbation을 그 위 레이어로.

## M2의 두 기둥
| 기둥 | 내용 | 비고 |
|---|---|---|
| **A. STATE 엔진** | perturbation 반응 예측 FM (인프라) | noncommercial 라이선스(R&D OK), 3070=추론만 |
| **B. TGFβ 정답 데이터** | TGFβ 처리 vs 비처리 fibroblast scRNA-seq | STATE 예측을 검증할 ground truth |

## 단계 (쉬운 실데이터 승리 → 어려운 예측 순)

### M2.1 · TGFβ 처리 데이터로 "급성 신호" 검증 ★먼저 (STATE 불필요)
- 목적: **만성(ILD)에선 평탄했던 tgfb_signaling이, 급성 TGFβ 처리에선 오르는가?** → M1 가설 직접 검증.
- 데이터 후보(저자 확보 또는 GEO 개방분, **NCBI 되는 로컬에서 GSE 확정**):
  - 진피 fibroblast + TGFβ1 (5일 처리) scRNA-seq — Frontiers 2023
  - TGFβ 시간/용량 코스 단일세포 (EMT) — bioRxiv 2022.05.06.490972
  - 폐/심장 fibroblast + TGFβ 처리 코스 (GEO 검색)
- 실행: 다운로드 → `convert_gsa.py` → `probe_signatures.py --case TGFb_treated --control untreated`
- **기대: tgfb_signaling + myofibroblast 둘 다 급성 상승** → 엔진이 "활성 신호"를 잡는다 입증.
- (보너스) tgfb_signaling v1: 미매칭/음성피드백(SMAD7/SKIL) 점검은 **이 데이터에서** 경험적으로 — p-hacking 아님.

### M2.2 · STATE perturbation 예측 (핵심, 난이도↑)
- 목적: 비처리 fibroblast + "TGFβ 자극" perturbation → STATE가 처리군 상태로의 이동을 예측하는가?
- **✅ 인프라 완료 (2026-06-10):**
  ```bash
  # 설치
  pip install uv && uv tool install arc-state
  # → state --help, state tx {train,predict,infer}, state emb {fit,transform,...} 동작 확인

  # baseline train (50 steps, CPU, 예시 데이터)
  state tx train \
    data.kwargs.toml_config_path=... data.kwargs.embed_key=X_hvg \
    data.kwargs.control_pert=TARGET1 training.max_steps=50 use_wandb=false ...
  # → 101M 파라미터 LlamaBidirectional 모델 학습 완료, final.ckpt 저장

  # inference
  state tx infer --model-dir runs/state_baseline/baseline_test \
    --adata .../random.h5ad --control-pert TARGET1 --output baseline_inferred.h5ad
  # → 10,000세포 예측 완료 (controls 2077, treated 7923)
  ```
- **⚠️ 핵심 설정 이슈(해결됨):**
  - `wandb/default.yaml` 없음 → configs에 직접 생성 (`mode: disabled, local_wandb_dir: /tmp/wandb`)
  - `control_pert` Hydra override 방식: `"data.kwargs.control_pert=<LABEL>"` (따옴표 필수)
- **다음 단계 (게이트 질문 먼저):** ⚠️ 위 train은 **장난감 데이터 50-step = 배관 점검**일 뿐, 학습된 모델 아님.
  진짜 다음은 **"STATE가 TGFβ perturbation을 표현할 수 있는가"** 를 먼저 확인:
  1. 사전학습 STATE 체크포인트 확보(HuggingFace `arcinstitute/SE-600M` 등) — 장난감 모델 폐기.
  2. 그 모델의 **perturbation 어휘에 TGFβ/사이토카인이 있는지** 확인.
  3. 없으면(OOD) → STATE-tx는 TGFβ 레이어에 부적합 → STATE-**emb**(임베딩)만 FM으로 쓰고
     TGFβ 반응은 실 ±TGFβ 데이터의 supervised delta로 학습(데이터 필요) 또는 GEARS/scGen 비교.
- ⚠️ **정직한 리스크**: STATE 사전학습은 주로 *유전자/약물* perturbation. **TGFβ 리간드 자극은 OOD** 일 수 있음.
  - 완화: fine-tune(클라우드 GPU L4/A100) 또는 STATE를 임베딩/맥락용으로만 쓰고 perturbation은 GEARS/scGen 비교.
- 검증: STATE 예측 처리군 vs 실제 처리군의 시그니처 점수 일치도.

### M2.3 · TED 질환특화 조건화 (데이터 도착 후)
- 안와/fibrocyte 맥락(TED scRNA-seq)으로 조건화 → "안와 fibroblast가 TGFβ에 어떻게 반응" = 질환특화 레이어 완성.
- 이게 거인이 못 가는 vertical. TED 데이터(저자 회신/wet lab) 대기.

## 하드웨어/라이선스 (변함없음)
- 3070(8GB): M2.1 전부 + STATE 추론 가능. STATE **학습/파인튜닝은 클라우드**(L4/A100, 현금트랙이 비용).
- STATE noncommercial: 내부 R&D 자유, 상업화 시 라이선스 협의 or 자체모델 대체.

## 실행 현황 (2026-06-10 기준)
| 단계 | 상태 | 비고 |
|---|---|---|
| M2.1 TGFβ 실데이터 검증 | **종료** | 데이터 3회 시도 모두 설계 함정 또는 껍데기. 공개 ±TGFβ primary fibroblast scRNA 희소. |
| M2.2 STATE 인프라 | **배관 ✅ / 실모델 ❌** | 설치+train+infer가 장난감 데이터로 동작(=smoke test). 진짜 baseline·사전학습 모델·TGFβ 표현 가능성은 미확인. |
| M2.3 TED 조건화 | 대기 | 저자 회신/wet lab 데이터 필요. |

> 원칙: **M2.2 다음 단계 — M1 fibroblast 데이터로 STATE perturbation 적용**. TED(M2.3)는 데이터 대기.


