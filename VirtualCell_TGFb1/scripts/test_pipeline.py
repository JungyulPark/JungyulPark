#!/usr/bin/env python3
"""
test_pipeline.py — Verification script for the Virtual Cell data preparation pipeline.
"""
import os
import subprocess
import scanpy as sc
import pandas as pd

def run_cmd(cmd):
    print(f"\n[test_pipeline] Running: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error stdout:\n{res.stdout}")
        print(f"Error stderr:\n{res.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    print(res.stdout)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    runs_dir = os.path.join(base_dir, "runs")
    os.makedirs(runs_dir, exist_ok=True)

    synth_h5ad = os.path.join(runs_dir, "test_synth.h5ad")
    test_csv = os.path.join(runs_dir, "test_counts.csv")
    converted_h5ad = os.path.join(runs_dir, "test_converted.h5ad")

    print("[test_pipeline] 1. Extracting synthetic data to CSV to simulate external GSA counts...")
    adata = sc.read_h5ad(synth_h5ad)
    # Convert to df (cells as columns, genes as rows - typical GSA processed count matrix format)
    df = pd.DataFrame(adata.X.T, index=adata.var_names, columns=[f"cell_{i}" for i in range(adata.n_obs)])
    df.to_csv(test_csv)
    print(f"[test_pipeline] Saved tabular counts matrix to: {test_csv} with shape: {df.shape}")

    print("[test_pipeline] 2. Converting CSV counts to AnnData using convert_gsa.py...")
    # Since we transposed (genes as rows, cells as columns), we use --transpose
    # We also inject the metadata since tabular CSV doesn't store obs columns
    convert_cmd = (
        f"python {base_dir}/scripts/convert_gsa.py "
        f"--input {test_csv} "
        f"--output {converted_h5ad} "
        f"--transpose "
        f"--obs-set disease=TAO,cell_type=Fibroblast "
        f"--filter-cells-genes 10 "
        f"--filter-genes-cells 1"
    )
    run_cmd(convert_cmd)

    # Let's manually set the first 400 cells to Control to test contrast (since in df they are all TAO due to --obs-set)
    print("[test_pipeline] 3. Editing cell group labels to create contrast (Control vs TAO)...")
    adata_conv = sc.read_h5ad(converted_h5ad)
    # Assign first half as Control, second half as TAO
    disease_labels = ["Control"] * 400 + ["TAO"] * 400
    adata_conv.obs["disease"] = disease_labels[:adata_conv.n_obs]
    adata_conv.write_h5ad(converted_h5ad)
    print(f"[test_pipeline] Updated obs['disease'] with Control/TAO labels. Shape: {adata_conv.shape}")

    print("[test_pipeline] 4. Running probe_signatures.py on the converted dataset...")
    probe_cmd = (
        f"python {base_dir}/scripts/probe_signatures.py "
        f"--h5ad {converted_h5ad} "
        f"--condition-col disease "
        f"--case TAO "
        f"--control Control "
        f"--outdir {runs_dir}/probe_test_run"
    )
    run_cmd(probe_cmd)

    print("[test_pipeline] Verification complete successfully.")

if __name__ == "__main__":
    main()
