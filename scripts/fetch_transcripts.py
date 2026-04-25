# fetch_transcripts.py
# Used to collect YouTube transcripts via Supadata API
# Run this script to reproduce the transcript collection in /research/youtube-transcripts/

import requests
import os

SUPADATA_API_KEY = "sd_a1d105d855167e93cb6006313a5143ca"

videos = {
    "russell_brunson_perfect_webinar": "https://youtu.be/r5RDc_wqmiU?si=6CQfy1C-Za32gvbS",
    "amy_porterfield_webinar":  "https://youtu.be/zf7mzsXVqfA?si=2JsqkVmIIrdaFR9h",
    "jason_fladlien_webinar":        "https://youtu.be/AwZbMUoRKcg?si=e1xbTPmf58rZnHyK",
    "rand_fishkin_b2b_storytelling_webinar":        "https://youtu.be/yDc3Fp4KMPs?si=q5sR7IDfGE5y78j2",
    "nathan_barry_b2b_scaling_webinar":           "https://youtu.be/pE7bwiFkx6Q?si=M9cj472BsLJAiS4E",
}

output_dir = "research/youtube-transcripts"
os.makedirs(output_dir, exist_ok=True)

failed_log_path = "failed_fetches.txt"
success_count = 0
failure_count = 0

for name, url in videos.items():
    print(f"Fetching: {name}")
    response = requests.get(
        "https://api.supadata.ai/v1/youtube/transcript",
        headers={"x-api-key": SUPADATA_API_KEY},
        params={"url": url, "text": True}
    )
    if response.status_code == 200:
        transcript = response.json().get("content", "")
        filepath = os.path.join(output_dir, f"{name}.md")
        with open(filepath, "w") as f:
            f.write(f"# {name.replace('_', ' ').title()}\n\n")
            f.write(f"Source: {url}\n\n")
            f.write(f"Collected via: Supadata API\n\n")
            f.write(f"---\n\n## Transcript\n\n{transcript}")
        print(f"  Saved to {filepath}")
        success_count += 1
    else:
        print(f"  Error {response.status_code} for {name}")
        failure_count += 1
        with open(failed_log_path, "a") as f:
            f.write(f"{name}: {response.status_code}\n")

print("\nFetch summary:")
print(f"  Succeeded: {success_count}")
print(f"  Failed: {failure_count}")
