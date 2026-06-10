#!/usr/bin/env python3
"""
convert_gsa.py — GSA / 10x / Tabular Count Matrix to AnnData (.h5ad) Converter

This utility prepares public datasets (e.g., GSA HRA007561, HRA000870 or GEO matrices)
for the VirtualCell validation pipeline. It standardizes input counts, transposes
matrices if necessary, appends sample metadata, and outputs a clean .h5ad file.

Example:
    python convert_gsa.py --input path/to/10x_dir --output data/HRA007561.h5ad --obs-set disease=GO,celltype=immune
"""
import argparse
import os
import sys
import pandas as pd
import numpy as np

def log(m):
    print(f"[convert] {m}", flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Input directory (for 10x mtx) or file (for CSV/TSV)")
    ap.add_argument("-o", "--output", required=True, help="Output .h5ad file path")
    ap.add_argument("-f", "--format", choices=["auto", "10x_mtx", "csv", "tsv"], default="auto",
                    help="Input format (default: auto-detect by path)")
    ap.add_argument("--obs-set", help="Metadata key=value pairs to inject into obs, comma-separated (e.g., disease=TAO,batch=B1)")
    ap.add_argument("--transpose", action="store_true", help="Transpose input matrix (use if genes are rows and cells are columns)")
    ap.add_argument("--filter-cells-genes", type=int, default=200, help="Min genes per cell to keep (default: 200)")
    ap.add_argument("--filter-genes-cells", type=int, default=3, help="Min cells expressing a gene to keep (default: 3)")
    ap.add_argument("--normalize", action="store_true", help="Perform normalize_total + log1p transformation")
    args = ap.parse_args()

    # Load dependencies
    try:
        import scanpy as sc
        import anndata as ad
    except ImportError:
        sys.exit("Error: scanpy and anndata packages are required. Please run: pip install scanpy anndata")

    # 1. Determine Format & Load Data
    fmt = args.format
    if fmt == "auto":
        if os.path.isdir(args.input):
            fmt = "10x_mtx"
        elif args.input.endswith(".csv") or args.input.endswith(".csv.gz"):
            fmt = "csv"
        elif args.input.endswith(".tsv") or args.input.endswith(".tsv.gz") or args.input.endswith(".txt") or args.input.endswith(".txt.gz"):
            fmt = "tsv"
        else:
            sys.exit(f"Could not auto-detect format for input: {args.input}. Specify --format.")

    log(f"Loading input as {fmt}: {args.input}")
    
    if fmt == "10x_mtx":
        try:
            adata = sc.read_10x_mtx(args.input, var_names='gene_symbols', cache=False)
        except Exception as e:
            sys.exit(f"Failed to read 10x MTX directory: {e}")
    else:
        # Load tabular counts
        sep = "," if fmt == "csv" else "\t"
        try:
            df = pd.read_csv(args.input, sep=sep, index_col=0)
            log(f"Tabular matrix shape read: {df.shape} (rows x columns)")
            
            # Construct AnnData
            adata = ad.AnnData(X=df.values.astype(np.float32))
            adata.obs_names = df.index.astype(str)
            adata.var_names = df.columns.astype(str)
        except Exception as e:
            sys.exit(f"Failed to read tabular matrix: {e}")

    # 2. Transpose if requested
    if args.transpose:
        log("Transposing matrix (cells <-> genes)...")
        adata = adata.T
        
    log(f"AnnData initialized: {adata.n_obs} cells x {adata.n_vars} genes")

    # Ensure var_names are unique
    adata.var_names_make_unique()
    adata.obs_names_make_unique()

    # 3. Apply Quality Control Filters
    if args.filter_cells_genes > 0:
        log(f"Filtering cells with fewer than {args.filter_cells_genes} genes...")
        sc.pp.filter_cells(adata, min_genes=args.filter_cells_genes)
        
    if args.filter_genes_cells > 0:
        log(f"Filtering genes expressed in fewer than {args.filter_genes_cells} cells...")
        sc.pp.filter_genes(adata, min_cells=args.filter_genes_cells)
        
    log(f"Post-filtering shape: {adata.n_obs} cells x {adata.n_vars} genes")

    # 4. Inject Metadata into obs
    if args.obs_set:
        pairs = args.obs_set.split(",")
        for pair in pairs:
            if "=" not in pair:
                log(f"Warning: Skipping invalid obs-set pair: {pair}")
                continue
            key, val = pair.split("=", 1)
            adata.obs[key.strip()] = val.strip()
            log(f"Injected metadata: obs['{key.strip()}'] = '{val.strip()}'")

    # 5. Optional normalization
    if args.normalize:
        log("Running normalize_total (target_sum=10000) and log1p...")
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)

    # 6. Save output
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    log(f"Saving AnnData object to: {args.output}")
    adata.write_h5ad(args.output)
    log("Conversion complete successfully.")

if __name__ == "__main__":
    main()
