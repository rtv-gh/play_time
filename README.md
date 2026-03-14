# U10 Rugby Festival Planner

A Streamlit app that allocates equal playing time across all squad players in a junior rugby union festival (U10, 8-a-side, RFU Age Grade).

## Features
- Set number of games (4 or 5)
- Edit squad names
- Automatic fair half-by-half allocation
- Name each opposition team
- One-tap schedule generation
- Playing-time summary per player

## Folder structure

```
rugby_festival_app/
├── app.py            # Main Streamlit app
├── utils.py          # Allocation & scheduling logic
├── requirements.txt
├── .gitignore
└── README.md
```

## Local development

```bash
# 1. Clone your repo and enter the folder
git clone <your-repo-url>
cd rugby_festival_app

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# or
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at http://localhost:8501.

## Deploy to Streamlit Community Cloud

1. Push this folder to a **public** GitHub repository (or a private one if you have a paid Streamlit plan).
2. Go to https://share.streamlit.io → **New app**.
3. Select your repo, branch (`main`), and set **Main file path** to `app.py`.
4. Click **Deploy** — done!

Streamlit will automatically install `requirements.txt` on every deploy.

## Customising default players

Open `app.py` and edit the `DEFAULT_PLAYERS` list near the top of the file:

```python
DEFAULT_PLAYERS = [
    "Seb", "Albie", "Henry", ...
]
```

These names are pre-filled in the app but coaches can always override them in the text area before generating a schedule.
