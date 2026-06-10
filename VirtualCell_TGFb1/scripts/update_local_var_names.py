#!/usr/bin/env python3
import fsspec
import h5py
import anndata as ad
import os

def main():
    url = 'https://datasets.cellxgene.cziscience.com/3d984e8c-bc37-4d36-8a3c-6651aa9a27e4.h5ad'
    local_path = '/Users/jungyulpark/2026_Project/JungyulPark/runs/lung_fibroblasts.h5ad'
    
    print("Opening remote file to read gene symbols...")
    with fsspec.open(url, 'rb').open() as f:
        with h5py.File(f, 'r') as h:
            cats = [x.decode('utf-8') for x in h['var/feature_name/categories'][:]]
            codes = h['var/feature_name/codes'][:]
            gene_symbols = [cats[code] for code in codes]
            
    print(f"Read {len(gene_symbols)} gene symbols. Example: {gene_symbols[:10]}")
    
    print("Loading local H5AD file...")
    adata = ad.read_h5ad(local_path)
    print(f"Local shape: {adata.shape}")
    
    # Replace var_names
    print("Replacing Ensembl IDs with gene symbols...")
    adata.var_names = gene_symbols
    adata.var_names_make_unique()
    
    print("Saving updated H5AD file...")
    adata.write_h5ad(local_path)
    print("Successfully updated local var_names!")

if __name__ == '__main__':
    main()
