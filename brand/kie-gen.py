#!/usr/bin/env python3
"""Generate brand assets via Kie.ai.

Usage: kie-gen.py <slug> <aspect> <promptfile> [model]
Models on this account: nano-banana-2 (fast), bytedance/seedream-v4-text-to-image,
google/imagen4-ultra.
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
    model = sys.argv[4] if len(sys.argv) > 4 else "nano-banana-2"
    prompt = open(promptfile).read().strip()
    inp = {"prompt": prompt, "aspect_ratio": aspect, "output_format": "png"}
    if model == "nano-banana-2":
        inp["resolution"] = "2K"
    elif "seedream" in model:
        # seedream takes aspect via image_size, not aspect_ratio
        inp.pop("aspect_ratio", None)
        inp["image_size"] = {"3:4": "portrait_4_3", "4:3": "landscape_4_3",
                             "16:9": "landscape_16_9", "9:16": "portrait_16_9",
                             "1:1": "square"}.get(aspect, "portrait_4_3")
        inp["image_resolution"] = "2K"
    d = req(CREATE, {"model": model, "input": inp})
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
