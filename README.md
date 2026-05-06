# FDE Codebase Scout

AI-powered codebase analysis tool for Forward Deployed Engineers. Built for the Tenex.co FDE role interview.

## Features

- **Health Score** — 0-100 gauge with visual indicator
- **Architecture Breakdown** — Layer-by-layer analysis with status indicators
- **Visual Architecture Diagram** — Mermaid diagram showing system connections
- **File Tree Visualization** — Estimated repo structure
- **Prioritized Quick Wins** — Actionable items with impact/effort/risk scoring
- **4-Week Sprint Plan** — Onboarding plan with velocity chart
- **Export Report** — Downloadable markdown report

## Setup

1. Clone the repository:
```bash
cd fde-codebase-scout
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. Run the app:
```bash
streamlit run app.py
```

## Tech Stack

- **Frontend**: Streamlit
- **AI**: Anthropic Claude API (claude-sonnet-4-20250514)
- **Charts**: Plotly
- **Diagrams**: streamlit-mermaid

## Usage

1. Paste a GitHub repo URL or describe a codebase in the sidebar
2. Click "Analyze" or use one of the sample repos
3. Explore results across tabs: Overview, Architecture, Quick Wins, Sprint Plan, Report
4. Download the full analysis as a markdown report

## Built By

[Isha Madhurendra](https://github.com/isha-madhurendra)
