# Café Proteus — Local Setup

## What you need
- Python 3.x installed
- An Anthropic API key (console.anthropic.com)
- The two files: `cafe_proteus_research.html` and `proxy.py`

---

## One-time setup

Open Command Prompt and run:

```
pip install flask flask-cors requests
```

Open `proxy.py` in a text editor and paste your API key:

```python
API_KEY = "sk-ant-YOUR-KEY-HERE"
```

Open `cafe_proteus_research.html` in a text editor and make sure the `callAPI` function points to the proxy:

```js
const r = await fetch('http://localhost:5000/v1/messages', {
```

---

## Every time you want to run it

You need **two Command Prompt windows open at the same time**.

**Window 1 — API proxy** (handles Anthropic API calls):
```
cd C:\Users\YOUR_NAME\Downloads
python proxy.py
```
You should see: `Proxy running on http://localhost:5000`

**Window 2 — file server** (serves the HTML file):
```
cd C:\Users\YOUR_NAME\Downloads
python -m http.server 8000
```
You should see: `Serving HTTP on 0.0.0.0 port 8000`

Then open your browser and go to:
```
http://localhost:8000/cafe_proteus_research.html
```

---

## To stop

Press `CTRL+C` in each Command Prompt window.

---

## Running the analysis

Once you have a `proteus_data.csv` from the experiment, put it in the same folder as `proteus_analysis.py` and run:

```
pip install pandas matplotlib seaborn scipy
python proteus_analysis.py
```

Plots are saved to a `plots/` folder at 300dpi.
