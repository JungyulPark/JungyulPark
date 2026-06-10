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
- 실행:
  ```
  git clone https://github.com/ArcInstitute/state.git ; uv tool install -e .
  state emb  ...   # 세포 임베딩
  state tx   ...   # perturbation 예측
  ```
  공개 perturbation 데이터로 **baseline(PDS) 재현** 먼저(원래 M0 잔여) → 그다음 TGFβ.
- ⚠️ **정직한 리스크**: STATE 사전학습은 주로 *유전자/약물* perturbation. **TGFβ 리간드 자극은 분포 밖(OOD)** 일 수 있음 → 예측이 빗나갈 수 있다.
  - 완화: M2.1의 TGFβ 데이터로 **fine-tune(클라우드 GPU)** 또는 최소한 **검증**. 안 되면 STATE는 임베딩/맥락용으로만 쓰고 perturbation은 다른 방식(GEARS/scGen 비교) 검토.
- 검증: STATE 예측 처리군 vs 실제 처리군의 시그니처 점수 일치도.

### M2.3 · TED 질환특화 조건화 (데이터 도착 후)
- 안와/fibrocyte 맥락(TED scRNA-seq)으로 조건화 → "안와 fibroblast가 TGFβ에 어떻게 반응" = 질환특화 레이어 완성.
- 이게 거인이 못 가는 vertical. TED 데이터(저자 회신/wet lab) 대기.

## 하드웨어/라이선스 (변함없음)
- 3070(8GB): M2.1 전부 + STATE 추론 가능. STATE **학습/파인튜닝은 클라우드**(L4/A100, 현금트랙이 비용).
- STATE noncommercial: 내부 R&D 자유, 상업화 시 라이선스 협의 or 자체모델 대체.

## 이번 주 실행 순서 (Antigravity 위임 가능)
1. **M2.1 데이터 1개 확보** (TGFβ 처리 fibroblast scRNA-seq, GSE 확정) → probe
2. 결과: tgfb_signaling 급성 상승 확인 → `04_results.md`에 추가
3. 병행: STATE 클론 + 공개데이터 baseline 재현 (M2.2 준비)

> 원칙: **M2.1(실데이터, 즉시 승리)부터.** STATE OOD 리스크가 큰 M2.2는 그다음. TED(M2.3)는 데이터 대기.
