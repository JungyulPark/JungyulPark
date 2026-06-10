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

### Route C — GSA (China National Center for Bioinformation) 수동/요청 확보
- **Li et al. 2022 (Cell Rep Med) — [HRA000870](https://ngdc.cncb.ac.cn/gsa-human/browse/HRA000870)** (BioProject: PRJCA005234)
  - **상태:** **통제 접근 (Controlled Access)**
  - **경로:** 데이터 접근 신청 및 기관 승인이 필수적입니다. 데이터 접근 위원회(DAC) ID: `HDAC000135`.
  - **신청 링크:** [Request Data](https://ngdc.cncb.ac.cn/gsa-human/browse/request/HRA000870)
  
- **Ke et al. 2025 (Commun Biol) — [HRA007561](https://ngdc.cncb.ac.cn/gsa-human/browse/HRA007561)** (BioProject: PRJCA025456)
  - **상태:** **공개 접근 (Open Access) - raw FASTQ 만 공개**
  - **다운로드 경로:** 
    - HTTP: `https://download.cncb.ac.cn/gsa-human/HRA007561/`
    - FTP: `ftp://download.big.ac.cn/gsa-human/HRA007561/`
  - **주의:** 100개 이상의 run 폴더(HRR1795807~HRR1795978)에 각 sample당 수십 GB의 raw FASTQ 파일이 들어있어, 전체 용량이 1TB를 넘습니다.
  - **대안 (가장 권장):** 논문 Data Availability 선언에 따라 교신저자에게 직접 가공 완료된 Seurat/AnnData 매트릭스를 이메일로 요청합니다.
    - 교신저자 이메일: `wups@mail2.sysu.edu.cn` (또는 `suwenru@mail.sysu.edu.cn`)
    - 분석 코드 저장소: [liuzh295/Graves-ophthalmopathy](https://github.com/liuzh295/Graves-ophthalmopathy.git)

### Route D — GEO (NCBI) 공개 scRNA-seq 데이터셋
- **Wu et al. 2022 (Front Endocrinol) — [GSE194323](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194323)** (SuperSeries: GSE194324)
  - **조직:** 안와 지방 조직 (Orbital adipose tissue) scRNA-seq (질환 TAO vs 대조군 HC)
  - **상태:** **공개 다운로드 가능** (GSM5833506, GSM5833507 등)

## 권장 실행 순서
1. **이메일 요청 병행:** HRA007561 및 HRA000870 교신저자에게 메일로 가공된 matrix (`.h5ad` 또는 `.rds`)를 요청합니다.
2. **GSE194323 활용:** 즉시 분석 가능한 공개 GEO 데이터셋인 GSE194323의 processed matrix를 다운로드하여 1차 probe에 사용합니다.
3. **가공 도구 활용:** 확보된 counts matrix를 `scripts/convert_gsa.py`를 통해 규격화된 `.h5ad`로 변환하여 분석에 투입합니다.

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
