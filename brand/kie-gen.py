#!/usr/bin/env python3
"""Generate brand assets via Kie.ai nano-banana-2.

Usage: kie-gen.py <slug> <aspect> <promptfile>
Writes <slug>.png into brand/assets/ and records the CDN url alongside it.
"""
import json, os, sys, time, urllib.request

KEY = os.environ["KIE_API_KEY"]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
HDRS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
        "User-Agent": UA}
CREATE = "https://api.kie.ai/api/v1/jobs/createTask"
INFO = "https://api.kie.ai/api/v1/jobs/recordInfo"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def req(url, body=None, timeout=120):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, headers=HDRS,
                               method="POST" if data else "GET")
    with urllib.request.urlopen(r, timeout=timeout) as f:
        return json.loads(f.read())


def fetch(url, out):
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=600) as src, open(out, "wb") as f:
        f.write(src.read())


def main():
    slug, aspect, promptfile = sys.argv[1], sys.argv[2], sys.argv[3]
    prompt = open(promptfile).read().strip()
    d = req(CREATE, {"model": "nano-banana-2",
                     "input": {"prompt": prompt, "aspect_ratio": aspect,
                               "resolution": "2K", "output_format": "png"}})
    if d.get("code") != 200:
        sys.exit(f"{slug}: createTask failed — {d.get('msg')}")
    tid = d["data"]["taskId"]
    print(f"{slug}: task {tid}", flush=True)
    for _ in range(150):
        time.sleep(4)
        s = req(f"{INFO}?taskId={tid}")["data"]
        if s.get("state") == "success":
            url = json.loads(s["resultJson"])["resultUrls"][0]
            path = os.path.join(OUT, f"{slug}.png")
            fetch(url, path)
            open(os.path.join(OUT, f"{slug}.url"), "w").write(url + "\n")
            print(f"{slug}: OK -> {path}", flush=True)
            return
        if s.get("state") == "fail":
            sys.exit(f"{slug}: FAILED — {s.get('failMsg')}")
    sys.exit(f"{slug}: timed out")


main()
