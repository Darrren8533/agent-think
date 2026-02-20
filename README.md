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

## Available Thinks

| Think | Core Lens |
|---|---|
| `financial` | ROI first, risk before reward, opportunity cost, time value |
| `engineering` | Measure before optimizing, find the bottleneck, reversibility, simplicity |
| `product` | User behavior > user words, validate assumptions cheaply, problem before solution |

## Usage

```
/think financial
/think engineering
/think financial engineering   ← stack multiple thinks
```

When thinks conflict (financial says "cut it", product says "users need it") — the tension is the insight.

## File Structure

```
agent-think/
├── thinks/
│   ├── financial.md
│   ├── engineering.md
│   └── product.md
└── .claude/
    └── skills/
        └── think.md     ← /think slash command
```

## Adding a New Think

Any domain expert can contribute a think file. Structure:

```markdown
# [Domain] Think

## 视角层 — Core mental models
### 核心本能
- What does an expert in this field notice first?
- What questions do they ask automatically?

### 分析习惯
- How do they break down a problem?

## 质疑层 — Challenge the framework
1. When is this framework the wrong lens?
2. Whose perspective is missing?
3. What does this framework make invisible?

## 切换信号
- When to suggest switching or stacking another think
```

## Why This Is Different From a Skill

| | Skill | Think |
|---|---|---|
| Scope | Specific task ("how to write a migration") | Entire conversation ("how to see all problems") |
| Output | Steps to follow | A reasoning lens to apply |
| Duration | Single task | Whole session |
