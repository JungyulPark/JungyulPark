#!/usr/bin/env python
"""
search_cellxgene.py — CELLxGENE Census를 API로 검색 (로컬 실행)

용도:
  1) TED/안와 데이터가 정말 없는지 코드로 확정 (2126개 수동 스크롤 대체)
  2) 있으면 obs 메타데이터로 즉시 후보 추출
  3) 없으면 → 인접 섬유화(폐/피부/심장 fibroblast) TGFβ 참조군 확보용으로 전환

설치(로컬, GPU 불필요):
  pip install cellxgene-census

주의: 작업환경(원격)은 외부망 차단 → 반드시 당신 로컬에서 실행.
"""
import argparse, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--terms", nargs="*",
                    default=["thyroid", "orbit", "graves", "ophthalmopathy"],
                    help="disease/tissue 검색어(부분일치)")
    ap.add_argument("--census-version", default="stable")
    ap.add_argument("--show-fibrosis", action="store_true",
                    help="TED 없을 때: 섬유화 참조 후보(폐/피부/심장) 함께 출력")
    args = ap.parse_args()

    try:
        import cellxgene_census
    except ImportError:
        sys.exit("pip install cellxgene-census 필요. (로컬에서 실행)")

    terms = [t.lower() for t in args.terms]
    with cellxgene_census.open_soma(census_version=args.census_version) as census:
        # 사람 datasets 메타데이터 테이블
        ds = census["census_info"]["datasets"].read().concat().to_pandas()
        cols = [c for c in ("collection_name", "dataset_title", "dataset_id") if c in ds.columns]
        print(f"[census] {len(ds)} datasets total. 검색어: {terms}\n")

        def hit(row):
            blob = " ".join(str(row.get(c, "")) for c in cols).lower()
            return any(t in blob for t in terms)

        m = ds[ds.apply(hit, axis=1)]
        if len(m):
            print(f"=== TED/안와 후보 {len(m)}건 ===")
            for _, r in m.iterrows():
                print(" •", r.get("dataset_title", "?"), "|", r.get("collection_name", ""))
                print("   id:", r.get("dataset_id", ""))
        else:
            print("=== TED/안와 데이터: 0건 (CELLxGENE에 없음 확정) ===")
            print("→ Route C(GEO, Li 2022)로 전환. fetch_geo_supp.py 사용.")

        if args.show_fibrosis and not len(m):
            print("\n=== 섬유화 참조 후보(폐/피부/심장 fibroblast 포함 컬렉션) ===")
            fib = ds[ds.apply(lambda r: any(k in " ".join(str(r.get(c,"")) for c in cols).lower()
                              for k in ("fibros", "fibroblast", "pulmonary fibros", "scleroderma")), axis=1)]
            for _, r in fib.head(20).iterrows():
                print(" •", r.get("dataset_title","?"), "|", r.get("collection_name",""))

if __name__ == "__main__":
    main()
