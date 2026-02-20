# Agent Think

Give Claude a domain expert's mental model — not just tools or behavior guides, but **how to think**.

## The Problem

Most people use AI like this:
> "I already know what I want, help me execute it."

So Claude's output is bounded by the user's own thinking. **Agent Think** breaks that boundary by loading domain-specific reasoning frameworks into Claude before the conversation starts.

## Two Layers

Every Think file has two layers working together:

| Layer | Purpose |
|---|---|
| **视角层 (Perspective)** | Domain-specific mental models — how an expert in this field naturally sees problems |
| **质疑层 (Challenge)** | Questions that challenge the framework itself — prevents the think from becoming a new cage |

## Available Thinks (18)

### Core Domains
| Think | Core Lens |
|---|---|
| `financial` | ROI first, risk before reward, opportunity cost, time value |
| `engineering` | Measure before optimizing, find the bottleneck, reversibility, simplicity first |
| `product` | User behavior > user words, validate assumptions cheaply, problem before solution |
| `startup` | MVP first, growth hacking, resource constraints, fast failure signals |
| `marketing` | User segmentation, channel mix, value exchange, funnel analysis |

### Professional & Institutional
| Think | Core Lens |
|---|---|
| `legal` | Exact definitions, exhaustive exceptions, procedural justice, rights-obligations symmetry |
| `medical` | History first, differential diagnosis, evidence-based, risk stratification |
| `scientific` | Falsifiability, controlled variables, correlation ≠ causation, confidence intervals |
| `political` | Power mapping, agenda control, resource flows, coalition building |
| `military` | Assume resistance, target decomposition, intelligence-driven, redundant backups |

### Advanced Analytical
| Think | Core Lens |
|---|---|
| `intelligence` | Competing hypotheses, source motivation analysis, mirror thinking, confidence levels |
| `cybersecurity` | Attacker-first perspective, attack surface enumeration, zero trust, defense in depth |
| `actuarial` | Tail risk first, frequency vs. severity, 10,000-run simulation, correlation risk |
| `ecological` | Cascade effects, carrying capacity, keystone species, emergence over design |
| `psychological` | Resistance as signal, surface vs. deep layer, defense mechanisms, non-judgment |

### Creative & Humanistic
| Think | Core Lens |
|---|---|
| `creative` | Why not?, SCAMPER, prototype over discussion, differentiation first |
| `philosophy` | Chase definitions, expose hidden assumptions, counter-hypothesis, distinguish fact from value |
| `education` | Learning objective first, zone of proximal development, feedback loops, intrinsic motivation |

## Usage

Load a think file at the start of a conversation:

```
@thinks/financial.md — load financial thinking framework
@thinks/cybersecurity.md — load cybersecurity thinking framework
```

Stack multiple thinks to get multi-lens analysis:

```
@thinks/financial.md @thinks/engineering.md
```

When thinks conflict (financial says "cut it", product says "users need it") — **the tension is the insight**.

## How Thinks Work

```
You: @thinks/intelligence.md  Analyze why our competitor suddenly dropped prices.

Claude (with Intelligence Think loaded):
  [Activates competing hypotheses framework]
  Hypothesis A: Cost reduction (operational). Hypothesis B: Market share grab. Hypothesis C: Distress signal.
  
  Source check: Their CFO's recent interviews show... (confidence: medium)
  Mirror question: If we wanted competitors to misread this move, how would we frame it?
  
  [Challenge layer activates]
  Warning: This analysis assumes the price drop is intentional strategy. 
  What if it's an error or internal miscommunication? Switch signal: if this is 
  about competitive response → stack Military Think.
```

## File Structure

```
agent-think/
├── thinks/              ← 18 domain thinking frameworks
│   ├── financial.md
│   ├── engineering.md
│   ├── product.md
│   ├── startup.md
│   ├── marketing.md
│   ├── legal.md
│   ├── medical.md
│   ├── scientific.md
│   ├── political.md
│   ├── military.md
│   ├── intelligence.md
│   ├── cybersecurity.md
│   ├── actuarial.md
│   ├── ecological.md
│   ├── psychological.md
│   ├── creative.md
│   ├── philosophy.md
│   └── education.md
├── THINK_CRITERIA.md    ← quality evaluation rubric (5 dimensions)
└── eval_all.py          ← batch evaluation script (requires GEMINI_API_KEY)
```

## Adding a New Think

Any domain expert can contribute a think file. Core structure:

```markdown
# [Domain] Think

## 视角层 — Core mental models
### 核心本能
- Trigger-action format: "When X, automatically do Y"

### 分析习惯
- Domain-specific questions to ask on every problem

## 质疑层 — Challenge the framework
1. When is this the wrong lens?
2. What does this framework make invisible?
3. Who/what gets ignored by this framework?

## 切换信号
- Specific scenario → stack [Other] Think
```

See `THINK_CRITERIA.md` for the 5-dimension quality rubric.

## Why This Is Different From a Skill

| | Skill | Think |
|---|---|---|
| Scope | Specific task ("how to write a migration") | Entire conversation ("how to see all problems") |
| Output | Steps to follow | A reasoning lens to apply |
| Duration | Single task | Whole session |
| Self-limits | No | Yes — challenge layer tells you when to stop |
