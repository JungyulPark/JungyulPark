#!/usr/bin/env python3
import fsspec
import h5py
import numpy as np
import scipy.sparse as sp
import pandas as pd
import anndata as ad
import os
import time

def main():
    url = 'https://datasets.cellxgene.cziscience.com/3d984e8c-bc37-4d36-8a3c-6651aa9a27e4.h5ad'
    out_dir = '/Users/jungyulpark/2026_Project/JungyulPark/runs'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'lung_fibroblasts.h5ad')
    
    print("=== Opening Remote H5AD (fsspec background caching enabled) ===")
    start_time = time.time()
    
    with fsspec.open(url, 'rb', cache_type='background', block_size=1024*1024).open() as f:
        with h5py.File(f, 'r') as h:
            print("Successfully opened remote file.")
            
            print("Reading var (genes)...")
            var_names = [x.decode('utf-8') for x in h['var/_index'][:]]
            
            print("Reading obs (cells metadata)...")
            cell_types_cat = [x.decode('utf-8') for x in h['obs/cell_type/categories'][:]]
            cell_types_codes = h['obs/cell_type/codes'][:]
            
            disease_cat = [x.decode('utf-8') for x in h['obs/disease/categories'][:]]
            disease_codes = h['obs/disease/codes'][:]
            
            donor_cat = [x.decode('utf-8') for x in h['obs/donor_id/categories'][:]]
            donor_codes = h['obs/donor_id/codes'][:]
            
            print("Reading indptr...")
            indptr = h['X/indptr'][:]
            
            print(f"Metadata read completed in {time.time() - start_time:.2f} seconds.")
            
            # Filter cells: fibroblast cell types AND (normal OR interstitial lung disease)
            target_cell_types = ['adventitial fibroblast', 'myofibroblast cell', 'alveolar type 1 fibroblast cell']
            target_diseases = ['normal', 'interstitial lung disease']
            
            selected_indices = []
            selected_cell_types = []
            selected_diseases = []
            selected_donors = []
            
            for idx in range(len(cell_types_codes)):
                ct = cell_types_cat[cell_types_codes[idx]]
                dis = disease_cat[disease_codes[idx]]
                if ct in target_cell_types and dis in target_diseases:
                    selected_indices.append(idx)
                    selected_cell_types.append(ct)
                    selected_diseases.append(dis)
                    selected_donors.append(donor_cat[donor_codes[idx]])
            
            num_selected = len(selected_indices)
            print(f"Selected {num_selected} fibroblast cells.")
            
            if num_selected == 0:
                print("No cells matched.")
                return
            
            # Group nearby range requests
            ranges = []
            for idx in selected_indices:
                ranges.append((indptr[idx], indptr[idx+1], idx))
            
            # Merge ranges if the gap between them is less than 100,000 elements (~400KB)
            gap_threshold = 100000
            merged_ranges = []
            if ranges:
                current_start = ranges[0][0]
                current_end = ranges[0][1]
                current_cells = [(ranges[0][2], ranges[0][0], ranges[0][1])]
                
                for r in ranges[1:]:
                    gap = r[0] - current_end
                    if gap < gap_threshold:
                        current_end = r[1]
                        current_cells.append((r[2], r[0], r[1]))
                    else:
                        merged_ranges.append((current_start, current_end, current_cells))
                        current_start = r[0]
                        current_end = r[1]
                        current_cells = [(r[2], r[0], r[1])]
                merged_ranges.append((current_start, current_end, current_cells))
            
            print(f"Merged {num_selected} individual cell queries into {len(merged_ranges)} range queries.")
            
            total_elements = sum(end - start for start, end, _ in merged_ranges)
            print(f"Total elements to download: {total_elements} (approx. {total_elements * 8 / (1024 * 1024):.1f} MB for indices and data combined)")
            
            print("=== Extracting Expression Matrix (X/data and X/indices) ===")
            start_extract = time.time()
            
            indices_ds = h['X/indices']
            data_ds = h['X/data']
            
            new_data = []
            new_indices = []
            new_indptr = [0]
            
            for i, (m_start, m_end, cells_info) in enumerate(merged_ranges):
                if i % 20 == 0:
                    pct_chunk = (i / len(merged_ranges)) * 100
                    elapsed_chunk = time.time() - start_extract
                    print(f"  Progress: {pct_chunk:.1f}% | Fetching chunk {i}/{len(merged_ranges)} ({m_end - m_start} elements) | Elapsed: {elapsed_chunk:.1f}s")
                
                # Fetch bulk range
                bulk_indices = indices_ds[m_start:m_end]
                bulk_data = data_ds[m_start:m_end]
                
                # Slices for individual cells in this bulk chunk
                for cell_idx, row_start, row_end in cells_info:
                    rel_start = row_start - m_start
                    rel_end = row_end - m_start
                    
                    new_indices.extend(bulk_indices[rel_start:rel_end])
                    new_data.extend(bulk_data[rel_start:rel_end])
                    new_indptr.append(len(new_indices))
                    
            print(f"Extraction completed in {time.time() - start_extract:.2f} seconds.")
            
            # Build CSR matrix
            print("Building CSR matrix...")
            num_genes = len(var_names)
            new_X = sp.csr_matrix((new_data, new_indices, new_indptr), shape=(num_selected, num_genes))
            
            # Create AnnData object
            print("Creating AnnData object...")
            obs_df = pd.DataFrame({
                'cell_type': selected_cell_types,
                'disease': selected_diseases,
                'donor_id': selected_donors
            }, index=[f"cell_{i}" for i in range(num_selected)])
            
            var_df = pd.DataFrame(index=var_names)
            
            adata = ad.AnnData(X=new_X, obs=obs_df, var=var_df)
            adata.var_names_make_unique()
            
            # Save to file
            print(f"Saving to {out_path}...")
            adata.write_h5ad(out_path)
            print(f"Successfully finished in {time.time() - start_time:.1f} seconds total!")

if __name__ == '__main__':
    main()
