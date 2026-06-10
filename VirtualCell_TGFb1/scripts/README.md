# scripts/ — 로컬 실행 (RTX 3070)

## fetch_geo_supp.py — GEO supplementary 다운로드 (로컬)
```bash
python fetch_geo_supp.py GSE308553                       # 파일 목록
python fetch_geo_supp.py GSE308553 --download -o ../data/GSE308553
```
데이터 획득 전체 전략은 [`../03_data_access.md`](../03_data_access.md) 참조 (Route A: CELLxGENE 권장).

## probe_signatures.py — go/no-go 검증 (파이프라인 아님)
시그니처 점수가 공개 안와 scRNA-seq에서 **TAO vs 대조를 분리하는지** 단 하나만 검정.

### ✅ 검증됨 (2026-06, 합성 데이터 smoke test)
실데이터 없이 파이프라인 정확성 확인 완료:
```bash
python make_synthetic.py --out /tmp/on.h5ad  --signal on    # 섬유화 신호 주입
python make_synthetic.py --out /tmp/off.h5ad --signal off   # 신호 없음
python probe_signatures.py --h5ad /tmp/on.h5ad  --condition-col disease --case TAO --control Control --celltype-col cell_type --celltype-val Fibroblast --outdir /tmp/on
python probe_signatures.py --h5ad /tmp/off.h5ad --condition-col disease --case TAO --control Control --celltype-col cell_type --celltype-val Fibroblast --outdir /tmp/off
```
- signal on → 핵심 섬유화 3프로그램 effect≈+1.0, p<1e-100 → **GO** (정상)
- signal off → 전부 비유의 → **NO-GO** (위양성 0, 정상)
- effect 부호: **양수 = 질환에서 상승**.

### 설치 (로컬, GPU 불필요)
```bash
pip install scanpy scipy pyyaml matplotlib
```

### 실행 (3단계)
```bash
# 1) 데이터의 obs 컬럼/값 먼저 확인 (condition 컬럼명을 모르므로 필수)
python probe_signatures.py --h5ad TAO_orbital.h5ad --list-obs

# 2) 확인한 컬럼/값으로 검정 (fibroblast subset 있으면 --celltype-* 추가)
python probe_signatures.py --h5ad TAO_orbital.h5ad \
    --condition-col disease --case TAO --control Control \
    --outdir ../runs/probe_li2022

# 3) 결과: 콘솔 표 + runs/probe_li2022/probe_results.csv + GO/NO-GO 판정
```

### 해석 (정직하게)
- **GO** = 핵심 섬유화 프로그램(tgfb_signaling/myofibroblast/ecm_fibrosis)이 질환에서 유의 상승
  (p<0.05 & |effect|>0.1). 엔진 방향의 **첫 증거**일 뿐, 증명 아님.
- **NO-GO** = 분리 안 됨 → 싸게 일찍 실패. 데이터 적합성·시그니처 v0·subset·배치효과 점검.
- ⚠️ 이건 "시그니처가 질환을 구분하나"이지 "binder가 효과 있나"가 아니다. perturbation 예측(STATE)은 그 다음.

### 다음 (GO일 때만)
- 다른 데이터셋(`01_datasets.md` D5 등)에서 재현 → 그때 비로소 **파이프라인**으로 승격.
- 시그니처 v0 → MSigDB 표준셋 보강 → v1 동결.
