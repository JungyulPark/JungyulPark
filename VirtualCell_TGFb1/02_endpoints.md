# M1 · 엔진 엔드포인트 정의 (문헌 기반 — 우리 데이터로 정의 X)

> 원칙: **엔드포인트는 41명 biased 데이터가 아니라 TED 분야 합의(문헌)에서 가져온다.**
> 엔진이 *예측할 타깃* = 분자/세포 프로그램. *해석의 잣대* = 검증된 임상 척도. 둘의 연결은 문헌이 이미 입증.
> 출처: Li et al. 2022 *Cell Rep Med* [DOI](https://doi.org/10.1016/j.xcrm.2022.100699), Wiersinga et al. 2025 *Lancet D&E* [DOI](https://doi.org/10.1016/S2213-8587(25)00066-X). (According to PubMed)

## A. 임상 엔드포인트 (field consensus — 재발명 금지)
| 척도 | 내용 | 역할 |
|---|---|---|
| **CAS** (Clinical Activity Score) | 활성도 7/10점 | 활성 vs 비활성 라벨 |
| **EUGOGO 중증도** | mild / mod-severe / sight-threatening | 중증도 계층 |
| **Proptosis** (Hertel) | 안구돌출 mm | 연속 표현형 |
| **Diplopia** (Gorman) | 복시 등급 | 기능 결과 |
| **DON** | 시신경병증 | 위중 결과 |
| 치료반응 | teprotumumab/스테로이드 반응 | perturbation 검증축 |

## B. 분자/세포 엔드포인트 — **엔진이 실제로 예측하는 타깃**
공개 scRNA-seq에서 정의되는, perturbation에 반응하는 프로그램. **이게 엔진의 출력.**

| 프로그램 | 마커/시그니처(예) | TGFβ/섬유화 관련성 |
|---|---|---|
| **Myofibroblast 분화** | ACTA2, TAGLN, POSTN | TGFβ 핵심 하류 ★ |
| **TGFβ 신호 활성 점수** | SERPINE1(PAI-1), CTGF/CCN2, SMAD7 | binder 작용의 직접 readout ★ |
| **ECM/섬유화** | COL1A1, COL3A1, FN1 | 안와 섬유화 표현형 ★ |
| **Lipofibroblast/adipogenesis** | RASD1, PPARG | TAO 지방생성(Li 2022) |
| **염증** | IFNG, IL6, CXCL8 | 활성기 염증축 |

> **엔진 과제 정의**: "TGFβ perturbation(=binder가 latent/active 포획)을 가했을 때 안와 fibroblast의
> *myofibroblast/TGFβ/ECM 점수*가 어떻게 이동하는가"를 예측. 이 점수들은 **B(분자)** 에서 측정,
> **A(임상)** 와의 연결은 문헌이 보증.

## C. 연결고리 (우리가 입증할 필요 없음 — 인용)
- TGFβ → myofibroblast 분화 → ECM 축적 → 안와 섬유화 → proptosis/제한성 사시: 확립된 경로.
- CAS 활성 ↔ 염증 시그니처, 섬유화 ↔ 비가역 중증도: 문헌 합의.
→ 엔진은 **분자 점수**를 예측하고, 임상적 의미는 **이 인용 사슬**로 해석한다.

## D. 검증 전략 (bias 데이터에 기대지 않음)
1. **1차 검증 = 공개 데이터 내부** hold-out (TAO vs 대조에서 프로그램 점수 분리되는가).
2. **2차 = 문헌 정합성** (teprotumumab/스테로이드가 줄이는 프로그램을 엔진도 줄인다고 예측하는가).
3. **우리 데이터 = 약한 보조 calibration만** (방향성 일치 점검, 정의 근거 ✗).
4. **결정적 검증은 2027 wet lab** 자체 perturbation scRNA-seq (POC).

## 다음 행동
- [ ] B의 시그니처 유전자셋을 표준 소스로 확정(MSigDB HALLMARK_TGF_BETA_SIGNALING 등) → `signatures/` 로 고정
- [ ] D1(Li 2022)에서 프로그램 점수 산출 파이프라인(scanpy `score_genes`) — **3070 로컬 가능**
- [ ] 우리 CSV는 별도 `pilot/`에서 illustrative로만 다룸 (메인 경로에서 분리)
