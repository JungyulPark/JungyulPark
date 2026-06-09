# 시그니처 유전자셋 (curated v0)

> `02_endpoints.md` B(분자 엔드포인트)를 **실행 가능한 자산**으로 고정.
> scanpy `sc.tl.score_genes(adata, gene_list)` 입력으로 직접 사용.

## 정직성 등급 — 반드시 읽을 것
- 아래는 **curated core panel v0** = 문헌상 잘 확립된 핵심 마커만 손으로 모은 것. **완전한 통계적 시그니처 아님.**
- ❌ 기억으로 54개 전체를 나열하지 않음(오류 위험). ✅ 핵심 마커 + 출처 + **권장: 런타임에 표준 DB와 교집합/보강**.
- 표준 DB(코드에서 fetch 권장):
  - **MSigDB `HALLMARK_TGF_BETA_SIGNALING`** (TGFβ 신호 정준)
  - **MSigDB `NABA_MATRISOME` / `NABA_CORE_MATRISOME`** (ECM)
  - **MSigDB `HALLMARK_ADIPOGENESIS`**, **`HALLMARK_INFLAMMATORY_RESPONSE`**
- v0로 먼저 probe → 신호 보이면 표준셋으로 교체/확장 후 동결(v1).

## 사용 예
```python
import yaml, scanpy as sc
sigs = yaml.safe_load(open("signatures/tgfb_fibrosis_signatures.yaml"))
for name, d in sigs["signatures"].items():
    genes = [g for g in d["genes"] if g in adata.var_names]
    sc.tl.score_genes(adata, genes, score_name=f"score_{name}")
```

## 출처
- TGFβ 정준 표적·섬유화: 확립된 분자생물학 + MSigDB Hallmark.
- 안와 lipofibroblast(RASD1)·adipogenesis: Li et al. 2022 *Cell Rep Med* [DOI](https://doi.org/10.1016/j.xcrm.2022.100699).
- (According to PubMed)
