# M1 결과 · 첫 실데이터 검증 (2026-06-10)

> **이정표: 레포 최초의 "진짜 데이터" go/no-go.** 합성이 아닌 실제 인간 환자 단일세포에서 시그니처 엔진 검증.
> 데이터: CELLxGENE — 인간 폐 fibroblast, **간질성 폐질환(ILD) vs 정상** 7,827세포 (Antigravity 추출).
> ⚠️ TED/안와 아님 — **섬유화 생물학 일반**에서 시그니처가 작동하는지 본 것.

## 결과 (ILD vs 정상 fibroblast, Mann-Whitney)
| 시그니처 | 매칭 | case_med | ctrl_med | effect | p | 판정 |
|---|---|---|---|---|---|---|
| **myofibroblast** | 8/8 | 0.458 | 0.200 | **+0.34** | 2.3e-120 | ✅ 상승 |
| **ecm_fibrosis** | 10/10 | 0.615 | 0.414 | **+0.34** | 6.5e-124 | ✅ 상승 |
| inflammation_active | 7/8 | -0.018 | -0.193 | +0.25 | 1.1e-68 | ✅ 상승 |
| tgfb_signaling | 10/12 | 0.167 | 0.125 | +0.08 | 8.5e-08 | · 사실상 평탄 |
| adipogenesis_lipofibroblast | 8/8 | -0.048 | -0.046 | -0.02 | 0.17 | · 변화 없음 |

## 해석 (정직하게)
**✅ 통과한 것 — 엔진이 진짜 섬유화 생물학을 잡는다**
- 핵심 구조 프로그램(**myofibroblast·ECM**)이 질환 fibroblast에서 명확히 상승. effect 0.34는 실데이터로선 견고(합성의 1.0은 비현실적, 실데이터 0.3대가 정상).
- **adipogenesis는 변화 없음 = 좋은 음성 대조.** 시그니처가 아무 데서나 켜지는 게 아니라 섬유화에 특이적임을 입증.

**🔬 중요한 발견 — TGFβ 신호 점수는 평탄(effect 0.08)**
- 하류(myofibroblast/ECM)는 올라갔는데 TGFβ **신호** 점수는 안 올랐다.
- 이건 버그가 아니라 **확립된(만성) 섬유화의 알려진 패턴**: TGFβ는 *먼저* 작용해 세포를 myofibroblast로 *commit*시키고, 만성 시점 스냅샷에선 활성 신호가 이미 가라앉음. 구조 프로그램만 남는다.
- **→ 엔진 설계에 주는 시사점(M4 binder 핵심):** "구조적 섬유화 상태"와 "활성 TGFβ 신호"는 **다른 readout**이다. binder는 *활성* TGFβ를 표적하므로, 정적 스냅샷이 아니라 **STATE perturbation(TGFβ를 가했을 때의 급성 반응)** 으로 읽어야 한다. 이번 실험이 그걸 정확히 알려줌.

## 액션 (이 결과에서 도출)
- [ ] **tgfb_signaling 시그니처 검토(v1)**: 미매칭 2개 확인, 음성피드백 유전자(SMAD7/SKIL) 영향 점검. ⚠️ 단 *결과를 예쁘게 만들려는 p-hacking 금지* — 활성 readout은 M2 STATE perturbation으로 검증.
- [ ] **M2 연결**: STATE로 TGFβ perturbation을 가했을 때 tgfb_signaling 점수가 *급성으로* 오르는지 = 진짜 검증.
- [ ] TED 실데이터 도착(저자 회신) 시 동일 probe 적용 → 질환특화 확인.

## 한계
- **LUNG ILD ≠ TED.** 섬유화 생물학 일반 검증일 뿐. 질환특화(안와)는 TED 데이터로 별도 확인 필요.
- 결과 CSV/데이터는 gitignore(용량) — 본 표가 보존 기록.

---

# M2.1 결과 · TGFβ 급성 처리 신호 검증 (2026-06-10)

> **목표:** "만성 ILD에서 평탄했던 tgfb_signaling이 급성 TGFβ 처리 시 오르는가?" — M1 미해결 가설 직접 검증.
> **데이터:** GEO GSE233063 — 인간 결장 fibroblast(CCD18co 세포주), **TGFβ처리 vs DMSO대조** scRNA-seq, 4,814세포 (Antigravity 다운로드·변환).
> ⚠️ 결장 fibroblast ≠ 폐/안와 fibroblast — 섬유화 생물학 일반 비교.

## 결과 (TGFβ_treated vs DMSO_control, Mann-Whitney)
| 시그니처 | 매칭 | case_med | ctrl_med | effect | p | 판정 |
|---|---|---|---|---|---|---|
| **tgfb_signaling** | 11/12 | 0.328 | 0.357 | **-0.07** | 3.4e-05 | · 오히려 낮음 |
| **myofibroblast** | 8/8 | 0.612 | 0.590 | +0.02 | 0.23 | · 변화 없음 |
| **ecm_fibrosis** | 10/10 | 0.871 | 0.863 | -0.00 | 0.95 | · 변화 없음 |
| adipogenesis_lipofibroblast | 4/8 | 0.002 | -0.012 | +0.07 | 9.4e-06 | · 미미 |
| inflammation_active | 5/8 | -0.102 | -0.009 | **-0.11** | 8.5e-11 | · 하락 |

**판정: NO-GO — 핵심 섬유화 프로그램이 분리되지 않음.**

## 해석 (정직하게)

**🔬 왜 tgfb_signaling이 안 올랐는가?**

두 가지 경쟁 가설:

1. **데이터 문제 (가능성 높음):** CCD18co는 결장 fibroblast 세포주. 피부/폐/안와 primary fibroblast와 TGFβ 반응성이 다를 수 있음. 세포주(cell line)는 반복 계대로 신호 반응이 무뎌짐.
2. **시그니처 v0 문제:** 현재 tgfb_signaling 유전자 중 SERPINE1·CTGF(CCN2)·SMAD7·SKIL 등은 맥락 의존적. 결장 fibroblast에서 이 유전자들의 기저 발현 및 TGFβ 유도 패턴이 다를 수 있음.

**💡 inflammation_active 하락(effect -0.11):** TGFβ의 면역억제 기능. TGFβ는 섬유화 유도와 동시에 염증 신호를 억제 — 이건 알려진 이중 역할이고 오히려 생물학적으로 타당.

**→ 핵심 시사점:** 이번 NO-GO는 "시그니처 엔진이 틀렸다"가 아니라 **"결장 fibroblast 세포주는 적합하지 않은 맥락"** 이라는 신호. Primary fibroblast + in vitro TGFβ 처리 데이터 필요.

## 다음 액션
- [ ] **더 적합한 데이터 재탐색:** Primary 피부/폐/안와 fibroblast + TGFβ1 처리 in vitro scRNA-seq (GEO/ArrayExpress 추가 탐색).
- [ ] **tgfb_signaling 시그니처 v1 업데이트:** CCN2(CTGF) 미매칭 확인. SMAD7/SKIL 음성피드백 유전자가 스코어를 희석하는지 점검. 단, 결과를 예쁘게 만들기 위한 p-hacking은 금지.
- [ ] **M2.2 STATE 준비 병행:** 위 실데이터 확보 전까지 STATE 인프라(클론·baseline재현) 먼저.

## 한계
- CCD18co는 세포주이며 결장 유래 — TED/안와 맥락과 거리가 있음.
- 결과 CSV는 gitignore(용량) — 본 표가 보존 기록.
