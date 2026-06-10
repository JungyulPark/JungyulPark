#!/usr/bin/env python3
"""
check_raw_targets.py — 개별 유전자 raw 발현 직접 진단
점수 없이, 핵심 마커 유전자의 조건별 중앙값을 직접 출력.
"양쪽 다 TGFβ" 설계 함정, 매핑 오류, 배치효과 탐지에 사용.

사용:
  python check_raw_targets.py --h5ad runs/foo.h5ad --condition-col treatment \\
      --case TGFb_treated --control DMSO_control
"""
import argparse, sys
import numpy as np

TARGETS = {
    "TGFβ 하류 (acute signal)": ["SERPINE1", "TGFB1", "SMAD3", "SMAD7", "SKIL", "JUNB", "ID1", "THBS1", "TGFBI", "SERPINE2"],
    "myofibroblast (구조)":     ["ACTA2", "TAGLN", "POSTN", "CNN1", "MYL9", "TPM1", "TPM2", "FN1"],
    "ECM fibrosis (구조)":      ["COL1A1", "COL1A2", "COL3A1", "COL5A1", "LOX", "SPARC", "FBN1", "DCN"],
    "염증 (양성 대조)":          ["IL6", "CXCL8", "IL1B", "CCL2"],
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True)
    ap.add_argument("--condition-col", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--control", required=True)
    args = ap.parse_args()

    try:
        import anndata as ad
        import scanpy as sc
    except ImportError:
        sys.exit("anndata/scanpy 필요: pip install anndata scanpy")

    print(f"[diag] loading {args.h5ad}")
    adata = ad.read_h5ad(args.h5ad)
    print(f"[diag] shape: {adata.shape}")

    if args.condition_col not in adata.obs.columns:
        sys.exit(f"컬럼 '{args.condition_col}' 없음. obs 컬럼: {list(adata.obs.columns)}")

    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)

    mask_case = adata.obs[args.condition_col] == args.case
    mask_ctrl = adata.obs[args.condition_col] == args.control
    n_case = mask_case.sum()
    n_ctrl = mask_ctrl.sum()

    if n_case == 0 or n_ctrl == 0:
        sys.exit(f"case({n_case}셀) 또는 control({n_ctrl}셀) 없음.")

    print(f"\n[diag] case='{args.case}'({n_case}셀) | control='{args.control}'({n_ctrl}셀)")
    print(f"{'유전자':<12} {'case_med':>10} {'ctrl_med':>10} {'log2FC':>8}  해석")
    print("-" * 60)

    import scipy.sparse as sp

    for group, genes in TARGETS.items():
        print(f"\n  ── {group} ──")
        for g in genes:
            if g not in adata.var_names:
                print(f"  {g:<12} {'(없음)':>10}")
                continue
            idx = adata.var_names.get_loc(g)
            X = adata.X

            if sp.issparse(X):
                case_vals = np.asarray(X[np.array(mask_case), :][:, idx].todense()).flatten()
                ctrl_vals = np.asarray(X[np.array(mask_ctrl), :][:, idx].todense()).flatten()
            else:
                case_vals = X[np.array(mask_case), idx]
                ctrl_vals = X[np.array(mask_ctrl), idx]

            case_med = float(np.median(case_vals))
            ctrl_med = float(np.median(ctrl_vals))
            fc = case_med - ctrl_med  # log-space => log2FC approx

            flag = ""
            if abs(fc) < 0.1 and case_med > 0.5:
                flag = "⚠ 양쪽 다 높음(둘 다 TGFβ?)"
            elif fc > 0.5:
                flag = "↑ case 상승"
            elif fc < -0.5:
                flag = "↓ case 하락"

            print(f"  {g:<12} {case_med:>10.3f} {ctrl_med:>10.3f} {fc:>8.3f}  {flag}")

    print("\n[diag] 완료.")

if __name__ == "__main__":
    main()
