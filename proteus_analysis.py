"""
Café Proteus — Analysis Script
================================
Reads proteus_data.csv and produces:
  - Console summary table (inter-agent variance by condition)
  - plots/01_hedge_density.png
  - plots/02_word_count.png
  - plots/03_sentiment.png
  - plots/04_variance_table.png
  - plots/05_topic3_all_agents.png  (the privacy topic — all 5 agents)

Usage:
    pip install pandas matplotlib seaborn scipy
    python proteus_analysis.py

Put proteus_data.csv in the same folder as this script.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# ── Config ────────────────────────────────────────────────────────────────────
CSV_FILE = "proteus_data.csv"
OUTPUT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Plotting style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

COND_COLORS = {
    'full_embodiment':  '#378ADD',
    'persona_only':     '#D85A30',
    'neutral_baseline': '#888780',
}
COND_LABELS = {
    'full_embodiment':  'Full embodiment',
    'persona_only':     'Persona only',
    'neutral_baseline': 'Neutral baseline',
}
AGENT_COLORS = {
    'HERO':    '#22dddd',
    'SHADOW':  '#dd44cc',
    'MIRROR':  '#44dd66',
    'ANON':    '#dddd22',
    'CODEC':   '#ff8833',
    'AGENT-1': '#aaaaaa',
    'AGENT-2': '#aaaaaa',
    'AGENT-3': '#aaaaaa',
    'AGENT-4': '#aaaaaa',
    'AGENT-5': '#aaaaaa',
}
NAMED_AGENTS = ['HERO', 'SHADOW', 'MIRROR', 'ANON', 'CODEC']

# ── Load & clean data ─────────────────────────────────────────────────────────
print(f"Loading {CSV_FILE}...")
df = pd.read_csv(CSV_FILE)
print(f"  Raw rows: {len(df)}")

# Drop empty/near-empty responses
df = df[df['wc'] > 5].copy()
print(f"  Valid rows (wc > 5): {len(df)}")
print(f"  Conditions: {df['condition'].unique()}")
print(f"  Agents: {df['agent'].unique()}\n")

# ── Helper functions ──────────────────────────────────────────────────────────
def agent_means(df, condition, metric):
    """Return per-agent mean for a given condition and metric."""
    sub = df[df['condition'] == condition]
    return sub.groupby('agent')[metric].mean()

def inter_agent_variance(df, condition, metric):
    """Variance of per-agent means within a condition."""
    means = agent_means(df, condition, metric)
    if len(means) < 2:
        return np.nan
    return means.var()

# ── Print summary to console ──────────────────────────────────────────────────
print("=" * 60)
print("INTER-AGENT VARIANCE BY CONDITION")
print("(Higher = more behavioural differentiation between agents)")
print("=" * 60)

metrics = ['hd', 'ir', 'qr', 'sent', 'wc']
metric_labels = {
    'hd':   'Hedge %',
    'ir':   'I-rate %',
    'qr':   'Q-rate %',
    'sent': 'Sentiment',
    'wc':   'Word count',
}

conds = ['full_embodiment', 'persona_only', 'neutral_baseline']
header = f"{'Condition':<20}" + "".join(f"{metric_labels[m]:>12}" for m in metrics)
print(header)
print("-" * 80)
for c in conds:
    row = f"{COND_LABELS[c]:<20}"
    for m in metrics:
        v = inter_agent_variance(df, c, m)
        row += f"{v:>12.3f}" if not np.isnan(v) else f"{'n/a':>12}"
    print(row)

print("\nPer-agent means (full embodiment):")
print(df[df['condition']=='full_embodiment'].groupby('agent')[metrics].mean().round(3).to_string())

# ── Plot 1: Hedge density by agent × condition ────────────────────────────────
print("\nGenerating plots...")

fig, ax = plt.subplots(figsize=(10, 5))
named_df = df[df['agent'].isin(NAMED_AGENTS)]
cond_agent = named_df.groupby(['condition', 'agent'])['hd'].mean().reset_index()

x = np.arange(len(NAMED_AGENTS))
width = 0.28
for i, cond in enumerate(['full_embodiment', 'persona_only']):
    vals = [cond_agent[(cond_agent['condition']==cond) & (cond_agent['agent']==a)]['hd'].values[0]
            if len(cond_agent[(cond_agent['condition']==cond) & (cond_agent['agent']==a)]) > 0
            else 0 for a in NAMED_AGENTS]
    bars = ax.bar(x + (i-0.5)*width, vals, width, label=COND_LABELS[cond],
                  color=COND_COLORS[cond], alpha=0.85)
    for bar, val in zip(bars, vals):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels(NAMED_AGENTS)
ax.set_ylabel('Mean hedge density (%)')
ax.set_title('Hedge density by agent × embodiment condition', fontweight='500')
ax.legend(framealpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_hedge_density.png")
plt.close()
print(f"  Saved {OUTPUT_DIR}/01_hedge_density.png")

# ── Plot 2: Word count by agent × condition ───────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
all_agents = sorted(df['agent'].unique())
wc_data = df.groupby(['condition', 'agent'])['wc'].mean().reset_index()

x = np.arange(len(all_agents))
width = 0.25
for i, cond in enumerate(conds):
    vals = [wc_data[(wc_data['condition']==cond) & (wc_data['agent']==a)]['wc'].values[0]
            if len(wc_data[(wc_data['condition']==cond) & (wc_data['agent']==a)]) > 0
            else 0 for a in all_agents]
    ax.bar(x + (i-1)*width, vals, width, label=COND_LABELS[cond],
           color=COND_COLORS[cond], alpha=0.85)

ax.set_xticks(x)
ax.set_xticklabels(all_agents, rotation=20, ha='right')
ax.set_ylabel('Mean word count')
ax.set_title('Word count by agent × condition', fontweight='500')
ax.legend(framealpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_word_count.png")
plt.close()
print(f"  Saved {OUTPUT_DIR}/02_word_count.png")

# ── Plot 3: Sentiment by agent × condition ────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
sent_data = named_df.groupby(['condition', 'agent'])['sent'].mean().reset_index()

for cond in ['full_embodiment', 'persona_only']:
    sub = sent_data[sent_data['condition']==cond].set_index('agent')
    vals = [sub.loc[a, 'sent'] if a in sub.index else np.nan for a in NAMED_AGENTS]
    ax.plot(NAMED_AGENTS, vals, 'o-', label=COND_LABELS[cond],
            color=COND_COLORS[cond], linewidth=2, markersize=7)

ax.axhline(0, color='gray', linestyle='--', alpha=0.4, linewidth=1)
ax.set_ylabel('Mean sentiment score')
ax.set_title('Sentiment by agent × condition', fontweight='500')
ax.legend(framealpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_sentiment.png")
plt.close()
print(f"  Saved {OUTPUT_DIR}/03_sentiment.png")

# ── Plot 4: Variance table as heatmap ─────────────────────────────────────────
variance_data = {}
for c in conds:
    variance_data[COND_LABELS[c]] = {
        metric_labels[m]: round(inter_agent_variance(df, c, m), 3)
        for m in metrics
    }

var_df = pd.DataFrame(variance_data).T
fig, ax = plt.subplots(figsize=(8, 3))
mask = var_df.isnull()
sns.heatmap(var_df.astype(float), annot=True, fmt='.3f', cmap='Blues',
            ax=ax, linewidths=0.5, mask=mask,
            annot_kws={'size': 10})
ax.set_title('Inter-agent variance by condition\n(higher = more differentiation)', fontweight='500')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_variance_heatmap.png")
plt.close()
print(f"  Saved {OUTPUT_DIR}/04_variance_heatmap.png")

# ── Plot 5: Topic 3 (privacy) — all 5 named agents, full embodiment ───────────
topic3 = df[(df['ti']==3) & (df['condition']=='full_embodiment') & (df['agent'].isin(NAMED_AGENTS))]

if len(topic3) > 0:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle('Topic 3 (privacy) — full embodiment, all agents', fontweight='500', y=1.02)

    plot_metrics = [('hd', 'Hedge density (%)'), ('sent', 'Sentiment'), ('wc', 'Word count')]
    for ax, (m, label) in zip(axes, plot_metrics):
        colors = [AGENT_COLORS.get(a, '#aaaaaa') for a in topic3['agent']]
        bars = ax.bar(topic3['agent'], topic3[m], color=colors, alpha=0.85, edgecolor='white')
        ax.set_ylabel(label)
        ax.set_title(label, fontweight='500')
        for bar, val in zip(bars, topic3[m]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01*max(topic3[m]),
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/05_topic3_privacy.png")
    plt.close()
    print(f"  Saved {OUTPUT_DIR}/05_topic3_privacy.png")
else:
    print("  Skipping topic 3 plot — no valid data for all agents")

# ── Done ──────────────────────────────────────────────────────────────────────
print(f"\nDone. All plots saved to ./{OUTPUT_DIR}/")
print("Tip: run a cleaner experiment (independent responses per agent) for publishable variance data.")
