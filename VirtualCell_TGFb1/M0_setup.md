# M0 · 인프라 셋업 + baseline 재현

> 목적: STATE를 인프라로 깔고, 공개 perturbation 데이터로 **baseline(PDS) 재현** → 이후 질환특화(M1–M3)의 출발선.
> 출처: [ArcInstitute/state](https://github.com/ArcInstitute/state), [cell-eval](https://github.com/ArcInstitute/cell-eval), [SE-600M](https://huggingface.co/arcinstitute/SE-600M).

## ⚠️ 전략 플래그 — 라이선스 (반드시 인지)
- **STATE는 noncommercial use.** 연구·벤치마크·내부 R&D 필터로는 자유. 그러나 **상업 제품에 STATE 가중치를 직접 탑재 불가.**
- 함의(헌장 1순위 = 회사·라이선스아웃):
  - 2026–2027: STATE를 **내부 in silico 스크리닝/검증 엔진**으로 사용 (합법, 문제없음).
  - 상업화 단계: ① Arc와 상업 라이선스 협의, 또는 ② **자체 데이터로 학습한 모델**(2027 wet lab scRNA-seq)로 대체.
  - → 해자는 STATE가 아니라 **우리 데이터·라벨·IP**라는 전제와 정확히 일치.

## 환경 요구
- GPU(권장, A100/L4급), Python 3.10+, CUDA. CPU로도 임베딩/소규모 추론 가능(학습은 느림).
- 디스크: 데이터 + 체크포인트 수십 GB.

## 설치 (uv 권장)
```bash
# 1) uv 설치 (없으면)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2) STATE
git clone https://github.com/ArcInstitute/state.git
cd state
uv tool install -e .         # 또는: uv run state --help

# 3) 평가 패키지 (PDS 등 지표)
git clone https://github.com/ArcInstitute/cell-eval.git

# 4) 분석 스택
uv pip install scanpy anndata scvi-tools
```
- 핵심 명령: `state emb`(세포 임베딩 사전학습/임베딩), `state tx`(perturbation 예측 학습/추론).
- 사전학습 임베딩: HuggingFace `arcinstitute/SE-600M`.

## Baseline 재현 절차 (M0 완료 기준)
1. **Virtual Cell Challenge 데이터** 또는 STATE repo 예시 perturbation 데이터 확보(공개 h5ad).
2. 전처리: normalize → log1p → HVG 선택 (`.obsm["X_hvg"]` 생성).
3. `state tx` 로 baseline 학습/추론 (repo의 Colab/예시 설정 따름).
4. **`cell-eval`로 PDS(Perturbation Discrimination Score) 측정** → 논문/리더보드 수치와 대조.
5. 수치·환경을 `runs/M0_baseline/`에 기록 → **재현성 확보 = M0 종료.**

## 완료 체크리스트
- [ ] STATE 설치 + `state --help` 동작
- [ ] cell-eval 설치
- [ ] 공개 perturbation 데이터로 baseline 1회 추론
- [ ] PDS 측정값 기록 (기대치와 ±오차 확인)
- [ ] 환경·시드·커맨드 `runs/M0_baseline/README` 로 고정

## 정직한 메모
- M0는 **"엔진이 도는지"** 검증일 뿐 — 질환특화 신호는 아직 없음(그건 M1–M2).
- GPU 미보유 시: 우선 SE 임베딩/소규모로 파이프라인만 검증하고, 학습은 클라우드 GPU(필요 시점에) 결정.
