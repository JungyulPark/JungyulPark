# VirtualCell_TGFb1 — 질환특화 perturbation 레이어 (GATE 2)

> 통합 미션 中 **"효과 예측"** 축. binder가 세포 상태를 어떻게 바꾸는지 in silico로 예측한다.
> 전략 맥락: `../00_STRATEGY/2026_focus_plan.md` · 지형도: `../00_STRATEGY/virtual_cell_landscape.md`.

## 핵심 원칙 — 따라가지 말고 올라타라
범용 virtual cell 모델(Arc STATE, CZI VCP/rBio)을 **인프라로 사용**한다. 처음부터 재학습하지 않는다.
우리의 차별점은 **TED/안와 섬유화 특화 + 독점 임상 데이터 + IP**.

## 무엇을 예측하나
TGFβ1 신호 조절(=binder가 latent/active TGFβ1을 포획) 시,
**안와 섬유아세포·fibrocyte의 세포 상태(transcriptome) 변화**를 예측 → binder 후보의 생물학적 효과 우선순위화.

## 데이터 매핑 (우리 자산 → 모델 입력)
| 레포 자산 | 역할 |
|---|---|
| `../Fibrocytes/` | fibrocyte 상태 — TED·TGFβ 신호 핵심 세포 |
| `../TED_Diplopia/`, `../TED_Calculator/`, `../TED_Dyslipidemia/` | 안와 질환 임상 표현형 라벨 |
| `../TRAb in GD/` | Graves 자가항체 동역학 (TSHR↔TGFβ 축) |
| 공개 atlas (CZI/Arc) | 배경 단일세포 분포 |

## 도구 스택 (오픈)
- **Arc STATE** (SE/ST, perturbation 예측, github.com/ArcInstitute/state)
- **CZI VCP / rBio / GREmLN** (virtualcellmodels.cziscience.com)
- scanpy / anndata, fine-tune or 프롬프트 기반 적용
- 평가: PDS(Perturbation Discrimination Score) 등 챌린지 지표

## 자산화
- 질환특화 벤치마크 + 논문(土)
- binder 후보 ↔ 예측 효과 연결 표 (→ GATE 3 발주 우선순위)
- 데이터 플랫폼 후보(제약·의료기기 협업)

## 상태
- [ ] STATE/VCP 환경 셋업 + 공개 데이터로 baseline 재현
- [ ] 우리 데이터 매핑/정제
- [ ] TGFβ perturbation 예측 프로토타입
- [ ] GATE 1 후보와 연결
