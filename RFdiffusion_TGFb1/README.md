# RFdiffusion_TGFb1 — binder 생성 엔진 (GATE 1)

> 통합 미션 中 **"분자 생성"** 축. force-state-selective TGFβ1 binder 후보를 de novo 설계한다.
> 전략 맥락: `../00_STRATEGY/2026_focus_plan.md`.

## 목표
proTGFβ1의 **latent(잠재형) vs active(활성형)** 상태를 force-state에 따라 선택적으로 구분/포획하는 단백질 binder 후보 셋 생성.

## 파이프라인
```
GATE 0  타깃 준비
  - proTGFβ1 latent / active 구조 확보 (PDB / AF3 예측)
  - force-state 차이가 드러나는 epitope/표면 정의
  - "구분 가설": 어떤 conformation 차이를 binder가 읽을 것인가

GATE 1  생성 → 필터
  1. RFdiffusion        : 타깃 epitope에 대한 binder 백본 생성
  2. ProteinMPNN        : 서열 설계
  3. AF2/AF3 + ipTM/pAE : 복합체 예측으로 in silico 필터링
  4. (선택) Rosetta/FoldX: 인터페이스 에너지 평가
  → 상위 후보 셋 산출

GATE 2  in silico 효과 검증  → ../VirtualCell_TGFb1/
GATE 3  좁히기 → in vitro 발주 우선순위 (2027)
```

## 도구 스택 (오픈)
- RFdiffusion (Baker lab), ProteinMPNN, AlphaFold2/3, ColabFold
- 평가: ipTM/pTM, PAE, interface ΔG

## 어려운 점 (정직하게)
- **force-state 선택성**은 RFdiffusion(정적 구조 설계)만으로 직접 다루기 어렵다. conformation별 epitope 분리 + MD/기계화학 보강 필요.
- 최대 병목은 설계가 아니라 **wet lab 검증**. in silico는 후보를 좁힐 뿐, 증명하지 않는다.

## 산출물(자산화)
- 재현 가능한 파이프라인(스크립트 + config)
- 후보 셋 + 랭킹 표 + 근거 figure
- PRD `LTGFB1_LATENT_TRAP` 버전 추적

## 상태
- [ ] GATE 0 타깃 정의 문서
- [ ] GATE 1 파이프라인 스크립트
- [ ] 후보 셋 v0
