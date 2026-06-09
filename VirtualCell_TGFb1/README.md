# VirtualCell_TGFb1 — 질환특화 Virtual Cell 엔진 (메인 트랙 ★)

> **이 폴더가 레포의 중심이다.** 2026 모든 본업 시간이 여기 들어간다.
> 전략: `../00_STRATEGY/2026_focus_plan.md` · 지형도: `../00_STRATEGY/virtual_cell_landscape.md`.

## 한 문장
오픈 virtual cell 모델(Arc STATE, CZI VCP)을 **인프라로 깔고**, TED/안와 섬유화 특화 **TGFβ perturbation 레이어**를 얹어, 거인이 못 가는 질환 vertical을 독점하는 엔진을 만든다.

## 핵심 원칙 — 따라가지 말고 올라타라
- ❌ 범용 FM 재학습 (컴퓨팅에서 진다)
- ✅ STATE/VCP를 fine-tune·프롬프트·벤치마크로 사용, **질환특화 데이터·IP로 차별화**

---

## 완성 로드맵 (M0 → M5) — 하나하나 완성

### M0 · 인프라 셋업
- [ ] `git clone github.com/ArcInstitute/state`, 환경 구성(conda/uv)
- [ ] CZI VCP(virtualcellmodels.cziscience.com) 계정·모델 접근
- [ ] 공개 perturbation 데이터로 **STATE baseline 재현 → PDS 측정**
- [ ] scanpy/anndata 파이프라인 골격
- 산출물: 재현 가능한 환경 + baseline 수치

### M1 · 데이터 자산화 (우리만의 해자)
| 레포 자산 | 역할 |
|---|---|
| `../Fibrocytes/` | fibrocyte 상태 — TED·TGFβ 신호 핵심 세포 |
| `../TED_Diplopia/` `../TED_Calculator/` `../TED_Dyslipidemia/` | 안와 질환 임상 표현형 라벨 |
| `../TRAb in GD/` | Graves 자가항체 동역학 (TSHR↔TGFβ 축) |
- [ ] 보유 데이터 인벤토리 + 결측/포맷/단위 점검
- [ ] anndata(.h5ad)로 통일, QC(품질·배치·정규화)
- [ ] 안와 섬유아세포/fibrocyte **reference 셋** 구축
- [ ] data card(출처·동의·한계) 작성
- 산출물: 정제 데이터셋 + data card

### M2 · 질환특화 perturbation 레이어
- [ ] perturbation 정의: **TGFβ 신호 조절**(latent/active 포획 = binder 작용) → 세포상태 변화
- [ ] STATE 적응(fine-tune or 프롬프트), 또는 rBio/GREmLN 비교
- [ ] TED 맥락에서 TGFβ dose-response 재현 시도
- 산출물: 질환특화 모델 v0

### M3 · 벤치마크 & 검증
- [ ] 질환특화 평가지표 정의(PDS + 임상 표현형 정합성)
- [ ] hold-out 검증, baseline 대비 우위 입증
- [ ] 실패모드 분석(과적합·배치효과)
- 산출물: 벤치마크 표 + figure

### M4 · binder 결합 (다운스트림 응용)
- [ ] `../RFdiffusion_TGFb1/` GATE 1 후보 → 엔진으로 예측 효과
- [ ] 후보 ↔ 예측 perturbation 효과 **우선순위표** (→ in vitro 발주)
- 산출물: 후보↔효과 연결표

### M5 · 자산화
- [ ] 논문/preprint (土 — academic credibility)
- [ ] IP(TSHR-ATrap 연계) 전략
- [ ] 파트너십 가능 데이터 플랫폼 데모
- 산출물: 논문, IP, 데모

---

## 도구 스택 (전부 오픈)
- **Arc STATE** (SE/ST) — github.com/ArcInstitute/state
- **CZI VCP / rBio / GREmLN** — virtualcellmodels.cziscience.com
- scanpy, anndata, scvi-tools / 평가: PDS

## 정직한 리스크
- 보유 데이터가 **단일세포(scRNA-seq)인지** 확인 필요. bulk/임상지표뿐이면 perturbation 모델 직접 학습은 제한 → 공개 단일세포 + 우리 라벨 결합 전략으로 전환.
- 엔진은 후보를 **좁힐 뿐 증명하지 않는다.** 최종 검증은 wet lab(2027~).
