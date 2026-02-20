"""
Final evaluation of all 13 think files against THINK_CRITERIA.md
"""
import os
import sys
import json
from google import genai
from google.genai import types

# Force UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Set GEMINI_API_KEY environment variable first")
client = genai.Client(api_key=API_KEY)

def generate(prompt):
    resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return resp.text

THINKS_DIR = os.path.join(os.path.dirname(__file__), "thinks")
CRITERIA_PATH = os.path.join(os.path.dirname(__file__), "THINK_CRITERIA.md")

with open(CRITERIA_PATH, encoding="utf-8") as f:
    criteria = f.read()

think_files = sorted(f for f in os.listdir(THINKS_DIR) if f.endswith(".md"))

PROMPT_TEMPLATE = """
你是 Think 质量评审员。根据以下评分标准，评估这个 Think 文件。

=== 评分标准 ===
{criteria}

=== Think 文件内容 ===
文件名：{filename}
{content}

=== 任务 ===
按以下 5 个维度各给出 0-100 的分数，并给出 1-2 句理由：
1. 视角独特性（uniqueness）权重 25%
2. 质疑层有效性（challenge）权重 25%
3. 可操作性（operability）权重 25%
4. 切换信号清晰度（switch_signal）权重 15%
5. 领域差异度（differentiation）权重 10%

返回 JSON，格式如下（只返回 JSON，不要其他文字）：
{{
  "uniqueness": {{"score": 0, "reason": ""}},
  "challenge": {{"score": 0, "reason": ""}},
  "operability": {{"score": 0, "reason": ""}},
  "switch_signal": {{"score": 0, "reason": ""}},
  "differentiation": {{"score": 0, "reason": ""}},
  "overall_comment": ""
}}
"""

WEIGHTS = {
    "uniqueness": 0.25,
    "challenge": 0.25,
    "operability": 0.25,
    "switch_signal": 0.15,
    "differentiation": 0.10,
}

results = []

for fname in think_files:
    path = os.path.join(THINKS_DIR, fname)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    prompt = PROMPT_TEMPLATE.format(
        criteria=criteria,
        filename=fname,
        content=content,
    )

    try:
        raw = generate(prompt).strip()
        # strip markdown code blocks if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw)
        weighted = sum(data[k]["score"] * WEIGHTS[k] for k in WEIGHTS)
        if weighted >= 80:
            verdict = "[KEEP]"
        elif weighted >= 60:
            verdict = "[REVISE]"
        else:
            verdict = "[REWRITE]"
        results.append({
            "name": fname.replace(".md", ""),
            "scores": {k: data[k]["score"] for k in WEIGHTS},
            "weighted": round(weighted, 1),
            "verdict": verdict,
            "comment": data.get("overall_comment", ""),
            "reasons": {k: data[k]["reason"] for k in WEIGHTS},
        })
        print(f"  OK {fname} -> {weighted:.1f} {verdict}")
    except Exception as e:
        print(f"  ERR {fname} -> ERROR: {e}")
        results.append({"name": fname.replace(".md", ""), "weighted": -1, "verdict": "ERROR", "comment": str(e)})

# Print summary table
print("\n" + "="*70)
print(f"{'Think':<16} {'U':>5} {'C':>5} {'O':>5} {'S':>5} {'D':>5} {'Total':>7}  Verdict")
print("-"*70)
for r in sorted(results, key=lambda x: -x.get("weighted", 0)):
    if "scores" in r:
        s = r["scores"]
        print(f"{r['name']:<16} {s['uniqueness']:>5} {s['challenge']:>5} {s['operability']:>5} {s['switch_signal']:>5} {s['differentiation']:>5} {r['weighted']:>7}  {r['verdict']}")
    else:
        print(f"{r['name']:<16} {'':>5} {'':>5} {'':>5} {'':>5} {'':>5} {'ERR':>7}  {r['verdict']}")

keep = [r for r in results if r["verdict"] == "[KEEP]"]
revise = [r for r in results if r["verdict"] == "[REVISE]"]
rewrite = [r for r in results if r["verdict"] == "[REWRITE]"]
print(f"\n总结：✅ KEEP={len(keep)}  🟡 REVISE={len(revise)}  ❌ REWRITE={len(rewrite)}")

# Print per-think weak spots
print("\n=== 各 Think 最弱维度 ===")
for r in sorted(results, key=lambda x: -x.get("weighted", 0)):
    if "scores" not in r:
        continue
    s = r["scores"]
    weak = min(s, key=lambda k: s[k])
    print(f"{r['name']:<16} 最弱: {weak}={s[weak]}  {r['reasons'].get(weak,'')}")
