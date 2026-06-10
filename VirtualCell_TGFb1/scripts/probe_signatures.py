#!/usr/bin/env python
"""
probe_signatures.py — go/no-go 검증 (파이프라인 아님, 단일 가설 검정)

질문 하나에만 답한다:
  "signatures/ 의 TGFβ/섬유화/myofibroblast 점수가 공개 안와 scRNA-seq에서
   TAO(질환) vs 대조를 실제로 분리하는가?"

분리되면 → 엔진 방향의 첫 증거(go). 안 되면 → 싸게 일찍 실패(시그니처/데이터 재검토).
RTX 3070(8GB)/CPU에서 동작. 학습 없음, score_genes + 통계만.

사용 예:
  python probe_signatures.py \
      --h5ad /path/to/TAO_orbital.h5ad \
      --condition-col disease \
      --case TAO --control Control \
      --sig ../signatures/tgfb_fibrosis_signatures.yaml \
      --outdir ../runs/probe_li2022

주의: 데이터의 condition 컬럼명/값은 데이터셋마다 다르다. 먼저 --list-obs 로 확인할 것.
"""
import argparse, os, sys, yaml
import numpy as np

def log(m): print(f"[probe] {m}", flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--h5ad", required=True, help="입력 anndata (.h5ad)")
    ap.add_argument("--sig", default=os.path.join(os.path.dirname(__file__), "..", "signatures", "tgfb_fibrosis_signatures.yaml"))
    ap.add_argument("--condition-col", help="질환/대조 구분 obs 컬럼명")
    ap.add_argument("--case", help="질환 라벨 값 (예: TAO)")
    ap.add_argument("--control", help="대조 라벨 값 (예: Control)")
    ap.add_argument("--celltype-col", default=None, help="(선택) fibroblast subset 컬럼")
    ap.add_argument("--celltype-val", default=None, help="(선택) fibroblast 라벨 값")
    ap.add_argument("--outdir", default="probe_out")
    ap.add_argument("--list-obs", action="store_true", help="obs 컬럼/값만 출력하고 종료")
    ap.add_argument("--already-normalized", action="store_true", help="이미 normalize+log1p 된 데이터")
    args = ap.parse_args()

    try:
        import scanpy as sc
        from scipy.stats import mannwhitneyu
    except ImportError as e:
        sys.exit(f"의존성 필요: pip install scanpy scipy pyyaml matplotlib  ({e})")

    os.makedirs(args.outdir, exist_ok=True)
    log(f"loading {args.h5ad}")
    adata = sc.read_h5ad(args.h5ad)
    log(f"shape: {adata.shape}  (cells x genes)")

    # --- obs 탐색 모드: 컬럼명/값을 모를 때 먼저 실행 ---
    if args.list_obs:
        print("\n=== obs columns ===")
        for c in adata.obs.columns:
            vals = adata.obs[c].unique()
            shown = vals[:12]
            print(f"  {c}: {list(shown)}{' ...' if len(vals) > 12 else ''}")
        return

    if not (args.condition_col and args.case and args.control):
        sys.exit("--condition-col/--case/--control 필요. 먼저 --list-obs 로 확인하라.")
    if args.condition_col not in adata.obs:
        sys.exit(f"'{args.condition_col}' obs에 없음. --list-obs 로 확인.")

    # --- (선택) fibroblast subset ---
    if args.celltype_col and args.celltype_val:
        n0 = adata.n_obs
        adata = adata[adata.obs[args.celltype_col] == args.celltype_val].copy()
        log(f"subset {args.celltype_val}: {n0} -> {adata.n_obs} cells")

    # --- 정규화 (raw count면 수행) ---
    if not args.already_normalized:
        log("normalize_total + log1p")
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)

    # --- 시그니처 로드 & 스코어링 ---
    sigs = yaml.safe_load(open(args.sig))["signatures"]
    var_names = set(adata.var_names)
    results = []
    for name, d in sigs.items():
        present = [g for g in d["genes"] if g in var_names]
        missing = [g for g in d["genes"] if g not in var_names]
        if len(present) < 3:
            log(f"SKIP {name}: 매칭 유전자 {len(present)}개(<3). 누락={missing}")
            continue
        log(f"{name}: {len(present)}/{len(d['genes'])} 유전자 매칭. 누락={missing if missing else '없음'}")
        sc.tl.score_genes(adata, present, score_name=f"score_{name}")

        case = adata.obs[args.condition_col] == args.case
        ctrl = adata.obs[args.condition_col] == args.control
        x = adata.obs.loc[case, f"score_{name}"].values
        y = adata.obs.loc[ctrl, f"score_{name}"].values
        if len(x) < 10 or len(y) < 10:
            log(f"  경고 {name}: 표본 적음 case={len(x)} ctrl={len(y)}")
        try:
            u, p = mannwhitneyu(x, y, alternative="two-sided")
            # rank-biserial effect size: 양수 = 질환(case)에서 상승
            eff = (2 * u) / (len(x) * len(y)) - 1
        except ValueError:
            p, eff = float("nan"), float("nan")
        results.append(dict(program=name, n_genes=len(present),
                            case_median=float(np.median(x)), ctrl_median=float(np.median(y)),
                            effect=float(eff), pvalue=float(p)))

    if not results:
        sys.exit("스코어링된 프로그램 없음 — 유전자 심볼/데이터 확인 필요.")

    # --- 결과 표 + 판정 ---
    import csv
    csvp = os.path.join(args.outdir, "probe_results.csv")
    with open(csvp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader(); w.writerows(results)

    print("\n=== probe 결과 (TAO vs 대조) ===")
    print(f"{'program':28} {'n':>3} {'case_med':>9} {'ctrl_med':>9} {'effect':>7} {'p':>10}")
    go = []
    for r in results:
        flag = "✅" if (r["pvalue"] < 0.05 and abs(r["effect"]) > 0.1) else "·"
        if flag == "✅" and r["program"] in ("tgfb_signaling", "myofibroblast", "ecm_fibrosis"):
            go.append(r["program"])
        print(f"{r['program']:28} {r['n_genes']:>3} {r['case_median']:>9.3f} "
              f"{r['ctrl_median']:>9.3f} {r['effect']:>7.2f} {r['pvalue']:>10.2e} {flag}")

    print("\n=== 판정 ===")
    if go:
        print(f"GO 신호: 핵심 섬유화 프로그램 {go} 가 질환에서 유의 상승.")
        print("→ 엔진 방향 첫 증거. 다음: 다중 데이터셋 재현 후 파이프라인 승격.")
    else:
        print("NO-GO 신호: 핵심 섬유화 프로그램이 분리 안 됨.")
        print("→ 싸게 일찍 실패. 점검: 데이터 적합성, 시그니처 v0, fibroblast subset 여부, 배치효과.")
    log(f"결과 저장: {csvp}")

if __name__ == "__main__":
    main()
