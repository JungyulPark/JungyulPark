#!/usr/bin/env python
"""
fetch_geo_supp.py — GEO Series의 supplementary 파일 목록/다운로드 (로컬 실행)

GEO의 표준 경로 규칙으로 supplementary(matrix, .h5, .h5ad 등)를 받는다.
작업환경(원격)은 외부망 차단 → 반드시 당신 로컬(3070)에서 실행.

사용:
  python fetch_geo_supp.py GSE308553                # 파일 목록만
  python fetch_geo_supp.py GSE308553 --download -o ../data/GSE308553

주의: 일부 GEO는 raw만 있고 processed matrix가 없을 수 있다. 목록 먼저 확인.
"""
import argparse, os, sys, urllib.request, html.parser

def geo_suppl_url(gse: str) -> str:
    # 예: GSE308553 -> .../series/GSE308nnn/GSE308553/suppl/
    digits = gse[3:]
    stub = "GSE" + (digits[:-3] + "nnn" if len(digits) > 3 else "nnn")
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/{stub}/{gse}/suppl/"

class _Links(html.parser.HTMLParser):
    def __init__(self): super().__init__(); self.files = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v not in ("../",) and not v.startswith("?"):
                    self.files.append(v)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gse")
    ap.add_argument("--download", action="store_true")
    ap.add_argument("-o", "--outdir", default=".")
    args = ap.parse_args()

    base = geo_suppl_url(args.gse.upper())
    print(f"[geo] index: {base}")
    try:
        with urllib.request.urlopen(base, timeout=60) as r:
            page = r.read().decode("utf-8", "replace")
    except Exception as e:
        sys.exit(f"인덱스 접근 실패({e}). GSE 번호/네트워크 확인. (원격 작업환경은 외부망 차단 — 로컬에서 실행)")

    p = _Links(); p.feed(page)
    files = [f for f in p.files if not f.endswith("/")]
    if not files:
        sys.exit("supplementary 파일 없음 — GEO 페이지에서 직접 확인 필요.")
    print(f"[geo] {len(files)} files:")
    for f in files: print("   ", f)

    if args.download:
        os.makedirs(args.outdir, exist_ok=True)
        for f in files:
            dst = os.path.join(args.outdir, f)
            print(f"[geo] download {f}")
            urllib.request.urlretrieve(base + f, dst)
        print(f"[geo] saved -> {args.outdir}")
        print("다음: scanpy.read_10x_mtx / read_h5 / read_h5ad 로 로드 후 probe 실행.")

if __name__ == "__main__":
    main()
