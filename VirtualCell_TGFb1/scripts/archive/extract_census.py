#!/usr/bin/env python3
import cellxgene_census
import os

def main():
    out_dir = '/Users/jungyulpark/2026_Project/JungyulPark/runs'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'lung_fibroblasts.h5ad')
    
    print("Opening CELLxGENE Census...")
    with cellxgene_census.open_soma() as census:
        print("Querying and downloading subset (fibroblasts in ILD dataset)...")
        # Query for the specific dataset ID and fibroblast cell types
        adata = cellxgene_census.get_anndata(
            census,
            organism="Homo sapiens",
            measurement_name="RNA",
            obs_value_filter="dataset_id == 'f14bc322-1322-4184-8d16-409557525ea5' and cell_type in ['adventitial fibroblast', 'myofibroblast cell', 'alveolar type 1 fibroblast cell']"
        )
        print("Successfully retrieved subset.")
        print("adata shape:", adata.shape)
        
        # Display value counts of the disease column
        print("\nDisease distribution:")
        print(adata.obs['disease'].value_counts())
        
        # Display cell type distribution
        print("\nCell type distribution:")
        print(adata.obs['cell_type'].value_counts())
        
        # Make gene names unique and standard
        adata.var_names_make_unique()
        
        print(f"\nWriting to {out_path}...")
        adata.write_h5ad(out_path)
        print("Successfully saved subset AnnData!")

if __name__ == '__main__':
    main()
