# Analysis Guide

How to run the automated linguistic analysis pipeline on experiment data exported from Café Proteus.

---

## What you need

- Python 3.x installed
- `proteus_analysis.py`
- `proteus_data.csv` exported from the experiment runner

Place both files in the same folder before running.

---

## One-time setup

Install the required packages:

```
pip install pandas matplotlib seaborn scipy
```

---

## Running the analysis

```
python proteus_analysis.py
```

---

## Output

### Console
Prints two tables:
- Inter-agent variance by condition across all five metrics
- Per-agent means for the full embodiment condition

### plots/ folder

| File | Description |
|------|-------------|
| `01_hedge_density.png` | Mean hedge density (%) per agent — full embodiment vs persona only |
| `02_word_count.png` | Mean word count per agent across all three conditions |
| `03_sentiment.png` | Mean sentiment score per agent — full embodiment vs persona only |
| `04_variance_heatmap.png` | Inter-agent variance across all conditions — key finding table |
| `05_topic3_privacy.png` | Privacy topic — all five agents in full embodiment side by side |

All plots are saved at 300dpi, suitable for publication.

---

## Metrics computed

| Metric | Description |
|--------|-------------|
| `hd` — hedge density | Frequency of uncertainty markers (perhaps, maybe, might...) per 100 words |
| `ir` — I-rate | Frequency of first-person singular "I" as a proportion of total words |
| `qr` — question rate | Proportion of sentences ending in "?" |
| `sent` — sentiment | Positive minus negative lexicon matches, normalised by response length |
| `wc` — word count | Total words per response |

---

## Data quality

Responses with word count ≤ 5 are automatically excluded as failed calls. If a condition has fewer than two agents with valid responses, inter-agent variance cannot be computed and will display as `n/a`. A full experiment run (5 agents × 5 topics × 3 conditions) produces 75 responses before filtering.

---

## Changing the input file

If your CSV has a different filename, open `proteus_analysis.py` and change line 24:

```python
CSV_FILE = "proteus_data.csv"
```

---

## Replication

The script is self-contained and produces identical output given the same input CSV. It is included as supplementary material to support replication of the analysis reported in the paper.
