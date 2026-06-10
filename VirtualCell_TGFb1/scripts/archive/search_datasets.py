#!/usr/bin/env python3
import urllib.request
import json
import time

def main():
    url = "https://api.cellxgene.cziscience.com/curation/v1/collections"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    print("Fetching collection list...")
    with urllib.request.urlopen(req) as r:
        collections = json.loads(r.read().decode())
    
    print(f"Fetched {len(collections)} collections. Scanning for datasets with IPF/ILD disease annotations...")
    
    results = []
    # Query details for ALL collections to find datasets matching disease
    # To be fast, we can scan the summary list first since it has the 'disease' key!
    # Wait, let's verify if the summary list has the datasets with 'disease' key.
    # Yes, in the list endpoint, ds keys included: ['assay', 'dataset_id', 'dataset_version_id', 'disease', 'genetic_perturbation_strategy', 'is_pre_analysis', 'organism', 'perturbation_types', 'suspension_type', 'tissue']
    # So we don't even need to fetch details for all 379 collections! We can filter the list first and only fetch details for matched collections.
    
    matched_collections = {}
    for col in collections:
        col_name = col.get("name", "") or ""
        col_id = col.get("collection_id") or ""
        for ds in col.get("datasets", []):
            disease_list = ds.get("disease", [])
            is_ipf_ild = False
            for dis in disease_list:
                label = dis.get("label", "").lower()
                if "idiopathic pulmonary fibrosis" in label or "interstitial lung disease" in label or "pulmonary fibrosis" in label:
                    is_ipf_ild = True
                    break
            if is_ipf_ild:
                matched_collections[col_id] = col_name
                break
                
    print(f"Found {len(matched_collections)} collections with matching disease ontology. Fetching details to extract download URLs...")
    
    for i, (col_id, col_name) in enumerate(matched_collections.items()):
        print(f"[{i+1}/{len(matched_collections)}] Fetching: {col_name[:50]}...")
        detail_url = f"https://api.cellxgene.cziscience.com/curation/v1/collections/{col_id}"
        detail_req = urllib.request.Request(detail_url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(detail_req) as r:
                col_detail = json.loads(r.read().decode())
            for ds in col_detail.get("datasets", []):
                # Check if this specific dataset has the disease annotation
                disease_list = ds.get("disease", [])
                is_ipf_ild = False
                for dis in disease_list:
                    label = dis.get("label", "").lower()
                    if "idiopathic pulmonary fibrosis" in label or "interstitial lung disease" in label or "pulmonary fibrosis" in label:
                        is_ipf_ild = True
                        break
                if not is_ipf_ild:
                    continue
                
                ds_title = ds.get("title", "") or ""
                for asset in ds.get("assets", []):
                    if asset.get("filetype") == "H5AD":
                        size_mb = asset.get("filesize", 0) / (1024 * 1024)
                        results.append({
                            "col": col_name,
                            "ds": ds_title,
                            "size": size_mb,
                            "url": asset.get("url"),
                            "id": ds.get("dataset_id")
                        })
            time.sleep(0.1)
        except Exception as e:
            print(f"  Failed for {col_id}: {e}")

    results.sort(key=lambda x: x["size"])
    print(f"\nFound {len(results)} H5AD datasets matching IPF/ILD:")
    for r in results:
        print(f"Size: {r['size']:.1f} MB | Dataset ID: {r['id']} | Collection: {r['col'][:40]} | Dataset: {r['ds'][:40]} | URL: {r['url']}")

if __name__ == "__main__":
    main()
