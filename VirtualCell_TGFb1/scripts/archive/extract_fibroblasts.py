#!/usr/bin/env python3
import fsspec
import h5py
import numpy as np
import scipy.sparse as sp
import pandas as pd
import anndata as ad
import os

def main():
    url = 'https://datasets.cellxgene.cziscience.com/3d984e8c-bc37-4d36-8a3c-6651aa9a27e4.h5ad'
    out_dir = '/Users/jungyulpark/2026_Project/JungyulPark/runs'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'lung_fibroblasts.h5ad')
    
    print("Opening remote H5AD file...")
    with fsspec.open(url, 'rb').open() as f:
        with h5py.File(f, 'r') as h:
            print("Successfully opened remote file.")
            
            # Check X format
            x_group = h['X']
            is_sparse = isinstance(x_group, h5py.Group)
            print(f"X encoding: {'Sparse (Group)' if is_sparse else 'Dense (Dataset)'}")
            if is_sparse:
                print("X keys:", list(x_group.keys()))
                print("X attributes:", dict(x_group.attrs))
            
            # Read genes (var)
            # Gene names can be in var/_index or var/feature_name or var/feature_id
            print("Reading gene names (var)...")
            var_keys = list(h['var'].keys())
            print("var keys:", var_keys)
            
            # In H5AD, categorical/string columns in var are stored similarly
            if '_index' in h['var']:
                var_names = [x.decode('utf-8') for x in h['var/_index'][:]]
            elif 'feature_name' in h['var']:
                var_names = [x.decode('utf-8') for x in h['var/feature_name/categories'][:]]
                # Wait, this might be categorical
            else:
                var_names = [str(i) for i in range(h['X'].shape[1])]
            
            print(f"Number of genes: {len(var_names)}")
            
            # Read obs metadata
            print("Reading cell metadata (obs)...")
            cell_types_cat = [x.decode('utf-8') for x in h['obs/cell_type/categories'][:]]
            cell_types_codes = h['obs/cell_type/codes'][:]
            
            disease_cat = [x.decode('utf-8') for x in h['obs/disease/categories'][:]]
            disease_codes = h['obs/disease/codes'][:]
            
            donor_cat = [x.decode('utf-8') for x in h['obs/donor_id/categories'][:]]
            donor_codes = h['obs/donor_id/codes'][:]
            
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
            print(f"Number of selected cells (fibroblasts in normal/ILD): {num_selected}")
            
            if num_selected == 0:
                print("No cells matched target criteria.")
                return
            
            # Extract expression values from X for selected cells
            print("Extracting expression matrix for selected cells...")
            num_genes = len(var_names)
            
            if is_sparse:
                # CSR matrix slicing
                # We can read indptr, data, and indices
                indptr = h['X/indptr'][:]
                indices_ds = h['X/indices']
                data_ds = h['X/data']
                
                # Build a new CSR matrix for selected rows
                new_data = []
                new_indices = []
                new_indptr = [0]
                
                # To minimize HTTP requests, we can read chunks of selected cells
                # or read row by row. Since they are scattered, row-by-row reading is fine
                # but let's print progress
                for i, idx in enumerate(selected_indices):
                    if i % 1000 == 0:
                        print(f"  Processed {i}/{num_selected} cells...")
                    start = indptr[idx]
                    end = indptr[idx + 1]
                    
                    row_indices = indices_ds[start:end]
                    row_data = data_ds[start:end]
                    
                    new_indices.extend(row_indices)
                    new_data.extend(row_data)
                    new_indptr.append(len(new_indices))
                
                new_X = sp.csr_matrix((new_data, new_indices, new_indptr), shape=(num_selected, num_genes))
            else:
                # Dense matrix slicing
                # Reading many individual rows from a dense matrix over HTTP is slow,
                # but let's do it in batches or row by row
                X_ds = h['X']
                new_rows = []
                for i, idx in enumerate(selected_indices):
                    if i % 1000 == 0:
                        print(f"  Processed {i}/{num_selected} cells...")
                    new_rows.append(X_ds[idx, :])
                new_X = np.vstack(new_rows)
            
            # Create AnnData object
            print("Creating AnnData object...")
            obs_df = pd.DataFrame({
                'cell_type': selected_cell_types,
                'disease': selected_diseases,
                'donor_id': selected_donors
            }, index=[f"cell_{i}" for i in range(num_selected)])
            
            var_df = pd.DataFrame(index=var_names)
            
            adata = ad.AnnData(X=new_X, obs=obs_df, var=var_df)
            
            # Save to file
            print(f"Saving to {out_path}...")
            adata.write_h5ad(out_path)
            print("Done! File saved successfully.")

if __name__ == '__main__':
    main()
