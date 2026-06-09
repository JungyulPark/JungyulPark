# 2026 집중 계획 — 압축의 해

> 작성 기준일: 2026-06-09 · 메인 트랙 확정: **TGFβ1 force-state-selective binder (바이오텍)**
> 이 문서는 CLAUDE.md(헌장)의 2026년 실행 레이어다. 매주 이 문서를 열고 움직인다.

---

## 0. 한 문장 통합 논제 (The One Thesis)

> **오픈 virtual cell 파운데이션 모델(Arc STATE · CZI VCP · rBio) 위에,
> TED/안와 섬유화 특화 TGFβ1 perturbation 레이어를 얹어,
> force-state-selective TGFβ1 binder를 in silico로 설계·검증하는 질환특화 엔진을 만든다.**

- 이것이 RF diffusion · Virtual Cell project · Virtual Cell Challenge 3축을 **하나로 묶는 단일 미션**이다.
- 새 작업은 이 한 문장을 강화하는가로만 판단한다. 강화 못 하면 버린다.

---

## 1. 왜 이 방향인가 (저커버그/CZI 참고의 올바른 해석)

CZI(Chan Zuckerberg Initiative)/Biohub는 2026.4 **Virtual Biology Initiative($500M/5년)**, Arc Institute는 **STATE 모델**(관측 1.7억 + perturbation 1억 세포 학습)로 **범용** virtual cell 모델을 만든다. → 컴퓨팅·데이터 군비경쟁.

**따라가지 않는다. 올라탄다.**

| 그들(CZI/Arc) | 우리(박정열) |
|---|---|
| 범용 파운데이션 모델, 모든 세포주 | **질환특화**: TED·안와 섬유아세포·fibrocyte |
| $500M 컴퓨팅·데이터 스케일 | 오픈 모델을 **인프라로 사용** (재구축 X) |
| 일반 생물학 | **임상 근거 + IP**(TSHR-ATrap 등) |
| 데이터 없음(우리 도메인) | **독점 임상 데이터**(Fibrocytes/TED/TRAb) 보유 |

→ 해자(moat)는 컴퓨팅이 아니라 **임상 데이터 + IP + 질환 전문성**. 이게 "10년 독점적 지위"의 정체다.

---

## 2. 지금 당장 — 임박 마감 (D-day 우선)

| 마감 | 항목 | 트랙 | 상태 |
|---|---|---|---|
| **~6/15 (D-6)** | 2027 전임교원 충원신청서(공채) 제출 | 土 기반 — **최우선** | ☐ |
| **6/19 (D-10)** | Samsung 미래기술육성 제안서 (TGFβ1 binder, GATE 1 전산 예비결과) | 1순위 핵심 | ☐ |

> ⚠️ 전임교원 전환(비전임→전임)은 단순 커리어가 아니라 **연구 신뢰도 = 회사 신뢰도**의 토대(土). 바이오텍 제안서보다 먼저, 확실히 제출한다.
> ⚠️ Samsung 제안서는 10일 안에 full GATE 1 파이프라인을 끝낼 수 없다 — **접근법 + 예비 in silico 결과 + 질환특화 차별점(위 1번 표)을 novelty로** 제시하는 게 정직하고 강한 전략.

---

## 3. 2026 GATE 시퀀스 (in silico 후보 좁히기)

메인 트랙의 기술 경로. 상세는 `RFdiffusion_TGFb1/README.md` · `VirtualCell_TGFb1/README.md`.

```
GATE 0  타깃 정의       proTGFβ1 latent/active 구조 확보, force-state 구분 가설 정식화
GATE 1  binder 생성     RFdiffusion → ProteinMPNN → AF2/AF3 필터링 → 후보 셋
GATE 2  in silico 검증  질환특화 virtual cell 레이어로 binder perturbation 효과 예측
GATE 3  좁히기          상위 후보 N개 → in vitro 발주 우선순위
```

- **2026 목표 = GATE 1 완료 + GATE 2 셋업.** in vitro는 2027.
- 이 환경(레포)에서는 코드·문서·PRD·재현 파이프라인을 자산화한다. GPU 실행은 별도 인프라.

---

## 4. 2026 분기별 미션

| 분기 | 미션 | 산출물(자산) |
|---|---|---|
| Q2 (지금) | 전임교원 신청 + Samsung 제안서 + GATE 0 확정 | 제안서, 타깃 정의 문서 |
| Q3 | GATE 1 binder 생성 파이프라인 재현 가능화 | RFdiffusion 파이프라인, 후보 셋 |
| Q3–Q4 | 질환특화 virtual cell 레이어 셋업(STATE/VCP 기반) | 데이터 매핑, 벤치마크 |
| Q4 | Arc Virtual Cell Challenge 참가(credibility) + TSHR-ATrap 후속 IP | 챌린지 제출, IP 전략서 |

---

## 5. 거름망 (새 아이디어가 떠오를 때 — 식상 과잉 경계)

1. 이게 위 **통합 논제 한 문장**을 강화하는가? (아니면 버린다)
2. 논문·데이터·IP·기업가치로 남는가?
3. 그냥 재밌는 사이드인가? → 메인 시간 쓰지 않는다.

> 2026은 **"많이 하는 해가 아니라 하나를 남기는 해."** 분산하면 2029 황금기를 빈손으로 맞는다.
