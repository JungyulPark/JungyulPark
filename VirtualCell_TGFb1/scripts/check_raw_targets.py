#!/usr/bin/env python
"""
check_raw_targets.py — 시그니처 점수 믿기 전에, 정준 TGFβ 표적의 RAW 발현을 두 조건에서 직접 비교.

왜: TGFβ를 fibroblast에 처리하면 SERPINE1/CTGF/COL1A1 등은 *반드시* 오른다(교과서).
   이게 안 오르면 → 라벨/설계/매핑 문제이지, 엔진 문제가 아니다. (null 오진 방지)

사용:
  python check_raw_targets.py --h5ad merged.h5ad --condition-col condition --case TGFb --control Control
"""
import argparse, sys, numpy as np

CANON = ["SERPINE1","CTGF","CCN2","COL1A1","COL1A2","COL3A1","FN1","ACTA2","TAGLN","POSTN","TGFBI","SMAD7"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--condition-col", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--control", required=True)
    ap.add_argument("--already-normalized", action="store_true")
    a = ap.parse_args()

    import scanpy as sc
    ad = sc.read_h5ad(a.h5ad)
    if a.condition_col not in ad.obs:
        sys.exit(f"'{a.condition_col}' obs에 없음. 컬럼: {list(ad.obs.columns)}")
    if not a.already_normalized:
        sc.pp.normalize_total(ad, target_sum=1e4); sc.pp.log1p(ad)

    case = ad[ad.obs[a.condition_col] == a.case]
    ctrl = ad[ad.obs[a.condition_col] == a.control]
    print(f"case({a.case})={case.n_obs}세포  control({a.control})={ctrl.n_obs}세포\n")
    print(f"{'gene':10} {'case':>8} {'control':>8} {'logFC':>7}  판정")
    missing, up = 0, 0
    for g in CANON:
        if g not in ad.var_names:
            print(f"{g:10} {'—':>8} {'—':>8} {'—':>7}  ❌ var_names에 없음(매핑 문제)")
            missing += 1; continue
        tc = float(np.asarray(case[:, g].X.mean()))
        cc = float(np.asarray(ctrl[:, g].X.mean()))
        fc = tc - cc
        flag = "▲ UP" if fc > 0.05 else ("▼ down" if fc < -0.05 else "· flat")
        if fc > 0.05: up += 1
        print(f"{g:10} {tc:>8.3f} {cc:>8.3f} {fc:>7.2f}  {flag}")

    print("\n=== 진단 ===")
    if missing >= 6:
        print("→ 유전자 매핑 실패 (Ensembl→HGNC 안 됨). update_local_var_names.py 재실행 필요. 결과 무효.")
    elif up >= 4:
        print("→ 정준 TGFβ 표적이 case에서 상승함 = TGFβ 대비 진짜 존재.")
        print("  그런데 시그니처 점수가 평탄했다면 → 점수화/시그니처 v0 문제 (v1 검토 정당).")
    else:
        print("→ 정준 TGFβ 표적이 case에서 안 오름 = 이 대비엔 TGFβ 효과가 없음.")
        print("  (양쪽 다 TGFβ인 약물스크린일 가능성 ↑) → 데이터 설계 문제. 깨끗한 ±TGFβ 데이터로 교체.")

if __name__ == "__main__":
    main()
