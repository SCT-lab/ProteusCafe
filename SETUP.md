# Local Setup Guide

How to run Café Proteus on your own machine with a live API connection.

---

## What you need

- Python 3.x installed
- An Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com)
- The files: `cafe_proteus_research.html` and `proxy.py`

---

## One-time setup

Install the required Python packages:

```
pip install flask flask-cors requests
```

Open `proxy.py` in a text editor and paste your API key:

```python
API_KEY = "sk-ant-YOUR-KEY-HERE"
```

Open `cafe_proteus_research.html` in a text editor and make sure the `callAPI` function at the bottom points to the local proxy:

```js
const r = await fetch('http://localhost:5000/v1/messages', {
```

---

## Running the application

You need **two Command Prompt / Terminal windows open at the same time**.

**Window 1 — API proxy:**
```
cd path/to/your/files
python proxy.py
```
Expected output: `Proxy running on http://localhost:5000`

**Window 2 — file server:**
```
cd path/to/your/files
python -m http.server 8000
```
Expected output: `Serving HTTP on 0.0.0.0 port 8000`

Then open your browser and go to:
```
http://localhost:8000/cafe_proteus_research.html
```

---

## Running the analysis

Once you have exported `proteus_data.csv` from the experiment runner, place it in the same folder as `proteus_analysis.py` and run:

```
pip install pandas matplotlib seaborn scipy
python proteus_analysis.py
```

Plots are saved to a `plots/` folder at 300dpi, ready for publication.

---

## Stopping the servers

Press `CTRL+C` in each Command Prompt window.

---

## Notes

- Keep both server windows open for the duration of the experiment — closing either will break the connection
- The proxy holds your API key server-side so it does not need to appear in the HTML file
- University or institutional networks may block external API calls — use a personal hotspot if you encounter connection errors
