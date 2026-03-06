# Arena Business Model

## One-Line

The competition is free. The data is the product.

## The Flywheel

```
Free competitions → Engineers compete → Workflow data captured
       ↑                                        ↓
  Bigger bounties ← Revenue from data ← AI labs/employers buy insights
```

## Revenue Streams

### 1. AI Lab Benchmarking (Primary, B2B)

**Customer:** Anthropic, OpenAI, Google, Mistral, Cohere, xAI
**Product:** "Your model in real engineers' hands"
**Price:** $50K-$500K/year per lab

What they get:
- Per-model efficiency data across challenges (tokens, cost, completion rate)
- Acceptance/rejection rates (how often do engineers keep vs discard output)
- Edit-after-paste ratios (how much human cleanup does each model need)
- Head-to-head comparisons on identical problems
- Technique signature breakdowns (which workflows produce best results with their model)

Why they pay: Every AI lab runs synthetic benchmarks (SWE-bench, HumanEval).
None of them have data on how real engineers use their models on real problems
compared to competitors. This is the only live benchmark that matters.

### 2. Enterprise Proficiency Assessment (B2B)

**Customer:** Companies hiring or training engineers
**Product:** "How well does this candidate wield AI tools?"
**Price:** $200-$500/assessment, $20K-$100K/year enterprise

What they get:
- Standardized AI proficiency score for candidates
- Technique signature profile (what tools, what patterns, what efficiency)
- Comparison to platform benchmarks
- Custom challenge sets for specific tech stacks

Why they pay: Every company wants "AI-native engineers" but has no way to
measure the skill. Arena leaderboard rank is the first standardized credential
for human+AI engineering proficiency.

### 3. Workflow Data Licensing (B2B, Research)

**Customer:** Research institutions, AI labs, tooling companies
**Product:** Anonymized, aggregate human+AI workflow datasets
**Price:** $10K-$100K per dataset release

What they get:
- Keystroke-level recordings of human+AI collaborative coding
- Eye tracking data (how engineers read AI-generated code)
- Decision logs (when and why humans override AI)
- Cross-tool comparisons on identical problems
- Longitudinal skill development data

Why they pay: This dataset doesn't exist. Building it from scratch
requires recruiting participants, designing studies, getting IRB
approval. Arena produces it as a byproduct of competition.

### 4. Challenge Sponsorship (B2B)

**Customer:** Companies with real engineering problems
**Product:** Post your problem as a challenge, get solutions + workflow data
**Price:** Bounty amount + 20% platform fee

What they get:
- Multiple solutions from skilled engineers
- Full workflow data showing how each solution was built
- IP rights to winning solution (per challenge terms)
- Employer branding (your name on the challenge)

Why they pay: Better than posting a job. You get the solution AND the
data showing how it was built. If you like the technique signature,
hire the engineer.

### 5. Recruiting Marketplace (B2B, later)

**Customer:** Employers
**Product:** Filter and contact engineers by technique signature
**Price:** Placement fee or subscription

"Show me engineers who solve infrastructure problems in <20 min
with <15K tokens using Claude Code, ranked by composite score."

### 6. Certification (B2C, later)

**Customer:** Individual engineers
**Product:** "Arena-certified centaur engineer"
**Price:** $99-$299/certification

Complete a curated set of challenges, achieve minimum composite scores,
submit verified session data. Credential is tied to your technique
signature profile — it proves HOW you work, not just THAT you passed.

## Unit Economics (v0 → v1)

### v0: GitHub-native, $0 infrastructure

| Item | Cost |
|------|------|
| GitHub Actions | Free (2,000 min/month for public repos) |
| GitHub Pages | Free |
| Bounties | $500-$1,000 seed money |
| **Total** | **$500-$1,000** |

Revenue: $0. Building the dataset and community.

### v0.5: First revenue

| Item | Cost |
|------|------|
| Scoring infrastructure (Judge0/DMOJ) | $50/month |
| Stripe Connect (payments) | 2.9% + $0.30 per payout |
| Bounties | $2,000-$5,000/month |
| **Total** | **$2,000-$5,000/month** |

Revenue: First AI lab pilot ($50K), first enterprise assessment contracts.

### v1: Data capture at scale

| Item | Cost |
|------|------|
| Infrastructure | $500/month |
| IDE extension development | $15K one-time |
| Bounties | $10,000/month |
| **Total** | **$10,000-$15,000/month** |

Revenue: Multiple AI lab contracts, enterprise assessments, first
dataset licensing deals. Target: $30K-$50K MRR.

## Defensibility

1. **Network effect:** More engineers → more data → better benchmarks → more AI labs pay → bigger bounties → more engineers
2. **Data moat:** The workflow dataset is unique and grows with every competition. No one else has keystroke + eye tracking + AI interaction logs on identical problems from multiple participants.
3. **Technique signature IP:** The measurement methodology, normalization algorithms, and derived metrics are proprietary.
4. **Community:** Leaderboard reputation is non-transferable. Your Arena rank means something because of who else is competing.

## What This Is NOT

- Not a freelancing platform (bounties are prizes, not contracts)
- Not a hiring platform (initially — recruiting is a later add-on)
- Not an LLM benchmark (humans are always in the loop)
- Not an education platform (competition, not courses)
