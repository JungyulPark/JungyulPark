# M1 · 공개 단일세포 데이터셋 카탈로그 (TED/안와)

> 목적: STATE/VCP 엔진의 **연료** 확보. 2026 엔진은 공개 scRNA-seq로 만들고, 보유 임상데이터는 **결과 앵커**로 결합.
> 작성: 2026-06-09 · 출처: PubMed/문헌 검색 (아래 각 항목 DOI 참조).
> ⚠️ GSE 접근번호는 각 논문 "Data Availability"에서 **최종 확인 필요**(표시: 🔎confirm).

## 선정 기준 (엔진에 쓸 수 있는가)
1. **조직 = 안와(orbital connective tissue / fat / EOM)** — fibroblast/fibrocyte 존재 필수
2. **raw counts(UMI matrix) 공개** — STATE 입력 가능 (요약통계만 있으면 탈락)
3. **질환 + 대조군** 동시 포함 (perturbation/대조 비교 축)
4. **TGFβ/섬유화 신호** 관찰 가능 (lipofibroblast, myofibroblast, ECM)
5. 10x Genomics 등 표준 플랫폼 (배치보정 용이)

## 후보 데이터셋

| # | 연구 | 조직/플랫폼 | 질환 | 엔진 적합성 | 비고 |
|---|---|---|---|---|---|
| **D1 ★앵커** | Li et al. 2022, *Cell Rep Med* [DOI](https://doi.org/10.1016/j.xcrm.2022.100699) | 안와 결합조직 / 10x | TAO vs 대조 | **높음** — lipofibroblast(RASD1), myeloid, CD8 T | 안와 fibroblast 직접. GSE 🔎confirm |
| D2 | 안와조직 transcriptome 2025, *Sci Rep* [DOI](https://doi.org/10.1038/s41598-025-30716-9) | 안와조직 | TED vs 대조 | 중(bulk 가능성 확인) | **GSE308553** (검색 확인) |
| D3 | Single-cell multiomic, *Commun Biol* 2025 (s42003-025-08115-7) | 면역 landscape | GO | 중 — 면역축 보강 | GSE 🔎confirm |
| D4 | Single-cell BCR+transcriptome, PMC11132005 | **말초혈액** | TAO | 낮음(안와 아님) | fibrocyte 순환 연결엔 유용 |
| D5 | Six1-Eya1 extraocular myopathy, *Cells* 2025 [DOI](https://doi.org/10.3390/cells14211708) | 외안근(EOM) | TED 섬유화 | 중-높음 — **myofiber 섬유화** | TGFβ/섬유화 직접 관련 |

> 리뷰 길잡이: "Single-cell transcriptomics in thyroid eye disease" (PMC11717346, 2025) — 데이터셋 총정리. 접근해 GSE 목록 확정에 사용.

## 보유 임상데이터 → 엔진 결과 앵커 매핑
엔진(공개 scRNA-seq 학습)이 **예측해야 할 임상 표현형**을 우리 데이터가 정의·검증한다.

| 보유 데이터 | 제공 앵커(라벨) | 엔진에서의 역할 |
|---|---|---|
| `Fibrocytes`(41명, FibroT1/TSHRT1/IGFT1) | fibrocyte %·마커 발현 ↔ CAS | 분자 상태 → fibrocyte 부하 검증 |
| `TRAb in GD`(403, imp/adj 시계열) | 자가항체 동역학(TSHR축) | perturbation 강도 ↔ 활성도 |
| `TED_Dys`(330, 지질·NLR·CAS) | 전신 염증/대사 표현형 | 환자 계층화·외적타당도 |
| `TED_Diplopia`,`TED_Calculator` | 감압술/복시, ROC 라벨 | 임상 엔드포인트 정의 |

## 다음 행동 (M1 실행 순서)
1. D1(Li 2022) GSE 확정 → 다운로드 → scanpy 로드 → QC → fibroblast subset 추출
2. D5(EOM 섬유화) 확보 → TGFβ/myofibroblast 축 확인
3. D2/D3로 확장(배치 통합), D4는 fibrocyte 순환 연결용 보조
4. 보유 임상데이터 → 엔드포인트 정의서(`02_clinical_anchors.md`)로 정식화

---
*According to PubMed; 위 DOI는 원저자 귀속을 위한 것. GSE 번호는 게재본 Data Availability에서 확정할 것.*
