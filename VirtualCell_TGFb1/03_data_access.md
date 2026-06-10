# M1 · 데이터 획득 플레이북 (막힘 우회 + 정직한 경로)

> 목적: probe(`scripts/probe_signatures.py`)에 넣을 **실제 h5ad 확보.**
> 정직성: 접근번호는 데이터셋마다 다르고, 일부는 **통제접근(신청 필요)**. 가장 빠른 길부터 시도.
> ⚠️ 이 레포 작업환경은 외부망(NCBI/EBI/Cell) 차단됨 — 아래는 **당신 로컬(3070)에서** 실행.

## 경로 우선순위 (저항 적은 순)

### Route A — CZI CELLxGENE Discover ❌ TED 없음 (2026-06 확인)
- 전체 2126개 데이터셋 확인 결과 **TED/안와(orbital)/Graves orbitopathy 0건.**
- 눈 데이터는 전부 다른 조직: 망막·각막·시신경·섬유주·RPE/맥락막·안표면 등. **안와 지방/섬유아세포 없음.**
- API로 재확인: `scripts/search_cellxgene.py` (`pip install cellxgene-census`).
- → **TED엔 막다른 길.** Route C(GEO)로 직행. (CELLxGENE는 섬유화 *참조군*(폐/피부 fibroblast) 확보용으로만 보조 활용 가능)

### Route B — GEO 개방 processed matrix
- 대상 예: **GSE308553** (안와조직 transcriptome 2025, Sci Rep) 등 GEO 기탁분.
- 방법: GEO 페이지 → Supplementary file (matrix/barcodes/features 또는 .h5/.h5ad) 다운로드
  → `scripts/fetch_geo_supp.py` 또는 수동 → scanpy 로드.
- 장점: 대개 **즉시 개방**(신청 불필요).

### Route C — Li 2022 (Cell Rep Med) 원본
- ⚠️ 중국 그룹 → raw human scRNA-seq는 **GSA(NGDC, China) 통제접근**(HRA…)일 공산.
  raw는 데이터접근 신청+기관승인 필요(시간 소요). **processed matrix는 개방**일 수 있음.
- 정확 접근번호 확인(당신이 1분):
  1. PMC 전문 <https://pmc.ncbi.nlm.nih.gov/articles/PMC9418739/> → **"Data and code availability"** 절.
  2. 거기 적힌 GSE… / HRA… / CRA… / Zenodo DOI 를 그대로 사용.
  3. GSA면 개방(processed)/통제(raw) 구분 확인 후, 개방분 우선.

## 권장 실행 순서
1. **Route A 먼저 1분 검색** — 있으면 끝(가장 깨끗).
2. 없으면 **Route B(GSE308553 등 GEO 개방분)**.
3. Li 2022 원본이 꼭 필요하면 Route C로 접근번호 확인 + (필요시) 통제접근 신청 병행.

## 데이터 확보 후 (probe 연결)
```bash
cd VirtualCell_TGFb1/scripts
python probe_signatures.py --h5ad <받은파일>.h5ad --list-obs      # 컬럼/값 확인
python probe_signatures.py --h5ad <받은파일>.h5ad \
    --condition-col <질환컬럼> --case <질환값> --control <대조값> \
    --celltype-col <세포타입컬럼> --celltype-val Fibroblast \
    --outdir ../runs/probe_first
```
> `--list-obs` 는 바로 이 "컬럼명 모름" 문제를 풀라고 만든 것.

## 정직한 메모
- 접근번호를 본 세션에서 확정 못 함(작업환경 외부망 차단). 위 PMC 절에서 **당신이 직접 확인**이 가장 확실.
- 데이터 라이선스/동의범위 확인 후 사용(특히 통제접근 raw).
