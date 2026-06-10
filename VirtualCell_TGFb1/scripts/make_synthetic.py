#!/usr/bin/env python
"""
make_synthetic.py — probe_signatures.py 검증용 합성 anndata 생성 (실데이터 아님)

목적: 실데이터 없이 probe 파이프라인이 옳은지 증명.
  --signal on  : 질환(TAO)에서 섬유화 시그니처 유전자를 상향 → probe가 GO 내야 함
  --signal off : 차이 없음 → probe가 NO-GO 내야 함 (위양성 점검)
"""
import argparse, numpy as np, anndata as ad, yaml, os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--signal", choices=["on", "off"], default="on")
    ap.add_argument("--sig", default=os.path.join(os.path.dirname(__file__), "..", "signatures", "tgfb_fibrosis_signatures.yaml"))
    ap.add_argument("--n-per-group", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    sigs = yaml.safe_load(open(args.sig))["signatures"]
    sig_genes = sorted({g for d in sigs.values() for g in d["genes"]})
    # 배경 유전자 + 시그니처 유전자
    bg = [f"BG{i}" for i in range(2000)]
    genes = bg + sig_genes
    n = args.n_per_group
    cond = np.array(["Control"] * n + ["TAO"] * n)

    # 음이항 유사 count (배경)
    X = rng.poisson(2.0, size=(2 * n, len(genes))).astype(np.float32)

    if args.signal == "on":
        # TAO 세포에서 섬유화 시그니처 유전자만 상향 (myofibroblast/TGFβ/ECM)
        fib_idx = [genes.index(g) for d_name, d in sigs.items()
                   if d_name in ("tgfb_signaling", "myofibroblast", "ecm_fibrosis")
                   for g in d["genes"]]
        X[n:, fib_idx] += rng.poisson(6.0, size=(n, len(fib_idx))).astype(np.float32)

    A = ad.AnnData(X=X)
    A.var_names = genes
    A.obs["disease"] = cond
    A.obs["cell_type"] = "Fibroblast"
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    A.write_h5ad(args.out)
    print(f"[synth] {args.out}  shape={A.shape}  signal={args.signal}  "
          f"groups={dict(zip(*np.unique(cond, return_counts=True)))}")

if __name__ == "__main__":
    main()
