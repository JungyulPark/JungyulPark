#!/usr/bin/env python3
import urllib.request
import threading
import os
import time

def download_chunk(url, start, end, out_path, chunk_id, progress):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    req.add_header('Range', f'bytes={start}-{end}')
    try:
        with urllib.request.urlopen(req) as r:
            with open(out_path, 'r+b') as f:
                f.seek(start)
                buffer_size = 1024*1024  # 1MB buffer
                downloaded = 0
                while True:
                    chunk = r.read(buffer_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress[chunk_id] = downloaded
    except Exception as e:
        print(f"\nChunk {chunk_id} failed: {e}")

def main():
    url = "https://datasets.cellxgene.cziscience.com/3d984e8c-bc37-4d36-8a3c-6651aa9a27e4.h5ad"
    out_dir = "/Users/jungyulpark/2026_Project/JungyulPark/runs"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "lung_full.h5ad")
    
    print("Checking file size...")
    # Get Content-Length using a partial GET request
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    req.add_header('Range', 'bytes=0-0')
    with urllib.request.urlopen(req) as r:
        content_range = r.headers.get('Content-Range')
        if content_range:
            total_size = int(content_range.split('/')[-1])
        else:
            total_size = int(r.headers.get('Content-Length', 0))
        print(f"Total file size: {total_size / (1024*1024):.1f} MB ({total_size} bytes)")
        
    # Pre-allocate local file
    print("Pre-allocating local file...")
    with open(out_path, 'wb') as f:
        f.truncate(total_size)
        
    num_threads = 16
    chunk_size = total_size // num_threads
    threads = []
    progress = [0] * num_threads
    
    print(f"Starting parallel download with {num_threads} threads...")
    start_time = time.time()
    
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size - 1 if i < num_threads - 1 else total_size - 1
        t = threading.Thread(target=download_chunk, args=(url, start, end, out_path, i, progress))
        t.start()
        threads.append(t)
        
    # Monitor progress
    while any(t.is_alive() for t in threads):
        time.sleep(2)
        total_downloaded = sum(progress)
        pct = (total_downloaded / total_size) * 100
        elapsed = time.time() - start_time
        speed = total_downloaded / (1024 * 1024 * elapsed) if elapsed > 0 else 0
        print(f"Progress: {pct:.1f}% | Downloaded: {total_downloaded / (1024*1024):.1f}/{total_size / (1024*1024):.1f} MB | Speed: {speed:.2f} MB/s | Elapsed: {elapsed:.1f}s", end='\n')
        
    for t in threads:
        t.join()
        
    print(f"\nDownload finished in {time.time() - start_time:.1f} seconds total!")

if __name__ == '__main__':
    main()
