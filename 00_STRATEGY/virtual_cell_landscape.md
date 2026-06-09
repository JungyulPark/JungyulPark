# Virtual Cell 지형도 & 차별화 전략

> 목적: "저커버그(CZI)의 virtual cell"이 정확히 무엇인지 파악하고, 우리가 **따라가지 않고 올라타는** 길을 정의한다.
> 조사 기준일: 2026-06-09.

---

## 1. 누가 무엇을 하고 있나 (2025–2026)

### CZI / Biohub (저커버그) — 범용 + 자본 규모
- **Virtual Biology Initiative (2026.4.29)**: 5년 **$500M**. 예측 가능한 생명 모델 구축. ($100M 글로벌 데이터 생성 + $400M 차세대 측정·이미징·엔지니어링)
- **rBio (2025.8)**: virtual cell 시뮬레이션으로 학습한 **추론 모델**. 일부 실험을 in silico로 대체.
- **GREmLN**: 유전자 조절망(gene regulatory) 임베딩 모델, 수백만 단일세포 학습.
- **CZI × NVIDIA (2025.10)**: 페타바이트·수십억 세포로 스케일.
- 공개 플랫폼 **VCP**: virtualcellmodels.cziscience.com (모델·데이터·벤치마크 무료 공개).

### Arc Institute — 모델 + 벤치마크 대회
- **STATE 모델**: State Embedding(SE) + State Transition(ST). 관측 1.7억 세포 + perturbation 1억 세포(70 세포주) 학습. 코드 오픈(github.com/ArcInstitute/state).
- **Virtual Cell Challenge**: 반복·공개 벤치마크 대회. 평가지표 **PDS**(Perturbation Discrimination Score). "virtual cell의 튜링 테스트"(Cell, 2025).

### 시사점
- 범용 FM·대규모 컴퓨팅·데이터는 **이미 거인들의 전장**이다. 정면 경쟁 = 패배.
- **그러나** 이들은 전부 **오픈**(모델·코드·플랫폼·벤치마크)이다 → **우리의 인프라로 무료 사용 가능**.

---

## 2. 우리의 차별화 — 질환특화 응용 레이어

> 거인은 **범용 엔진**을 만든다. 우리는 그 엔진 위에 **TGFβ1/섬유화 질환특화 응용 레이어**를 만든다.

근거(이미 활발한 연구영역):
- 단일세포로 TGF-β1 유도 섬유화 세포별 반응 해석 가능(간 microtissue scRNA-seq 등).
- 단일세포 TGF-β/SMAD 신호는 **dose-dependent 확률적 버스트** → 미검 조건 예측 모델 존재.
- **SCALE**(Scalable Conditional Atlas-Level Endpoint transport) 등 cytokine perturbation 예측 프레임워크 등장.
- 파운데이션 모델로 섬유화 단계 간 세포 유사성·perturbation 영향 예측 가능.

우리만의 자산:
- **Fibrocytes** 데이터 — fibrocyte는 TED 병태·TGFβ 신호의 핵심 세포.
- **TED_Diplopia / TED_Calculator / TED_Dyslipidemia** — 안와 질환 임상 표현형.
- **TRAb in GD** — Graves병 자가항체 동역학(TSHR ↔ TGFβ 축 연결).
- → 거인들이 **갖지 못한 질환특화·임상연계 데이터**. 여기에 IP(TSHR-ATrap)가 붙는다.

---

## 3. 전략: 따라가지 말고 올라타라 (Build on top, don't rebuild)

```
[오픈 인프라 — 거인들이 만든 것]
  Arc STATE (perturbation 예측)  ·  CZI VCP/rBio  ·  공개 atlas
                    │  (우리는 이걸 fine-tune / 프롬프트 / 벤치마크로 사용)
                    ▼
[우리 레이어 — 우리만 만들 수 있는 것]
  TED/안와 섬유화 특화 TGFβ1 perturbation 모델
  + 독점 임상 데이터(Fibrocytes/TED/TRAb)
  + force-state-selective binder 효과 in silico 예측
                    │
                    ▼
[자산화]  논문(土) · IP · binder 후보 우선순위 · 데이터 플랫폼 후보
```

**하지 말 것**: 범용 FM 자체를 처음부터 재학습. (컴퓨팅·데이터에서 진다, 분산이다)
**할 것**: 오픈 모델을 깔고, 질환특화 데이터·IP·임상근거로 차별화.

---

## 4. 출처 (Sources)

- [Biohub — Virtual Biology Initiative ($500M)](https://biohub.org/news/virtual-biology-initiative/)
- [CZI × NVIDIA, virtual cell 모델 가속 (2025.10)](https://chanzuckerberg.com/newsroom/nvidia-partnership-virtual-cell-model/)
- [CZI rBio 추론 모델](https://chanzuckerberg.com/blog/rbio-reasoning-ai-model/)
- [CZI AI Virtual Cell 플랫폼](https://virtualcellmodels.cziscience.com/)
- [Arc Institute — STATE 모델](https://arcinstitute.org/news/virtual-cell-model-state)
- [Arc STATE 코드(GitHub)](https://github.com/ArcInstitute/state)
- [Virtual Cell Challenge — Turing test (Cell, 2025)](https://www.cell.com/cell/fulltext/S0092-8674(25)00675-0)
- [SCALE: virtual cell perturbation prediction (arXiv)](https://arxiv.org/pdf/2603.17380)
- [Single-cell TGF-β1 pro-fibrotic 반응 (PMC8122664)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8122664/)
