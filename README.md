# Rugby Festival Planner

A Streamlit app for planning junior rugby festival squads and tracking playing time.

## Features

- Choose an RFU age group from U7 to U11 and see the players-per-side requirement.
- Generate a fair half-by-half schedule for 3 to 6 games, with opposition names.
- Compare scheduled and actual playing time, including changes for substitutions or injuries.
- Export the playing-time comparison as a CSV file.
- Navigate between Home, Age regulations, and Videos.
- Open official RFU age-grade regulations from the app. The Age regulations and Videos tabs are ready for summaries and coaching links to be added.
- Use the app on desktop or portrait mobile screens.

Player names must be unique. The app starts with example player names, which can be edited in the squad editor.

## Project files

```text
play_time/
├── app.py            # Streamlit interface and page navigation
├── utils.py          # Squad allocation and schedule generation
├── requirements.txt  # Python dependencies
└── README.md
```

## Run locally

Python 3 and pip are required.

```bash
cd play_time
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints the local URL, usually http://localhost:8501.

## Deploy to Streamlit Community Cloud

1. Push the project to a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository and select the branch.
3. Set the main file path to `play_time/app.py` when the repository root contains this folder. If this folder is itself the repository root, use `app.py`.
4. Deploy. Streamlit installs dependencies from `requirements.txt`.

## Add page content

- Add age-group summaries to the corresponding U7-U11 sections in the Age regulations page in `app.py`.
- Add coaching video links to the Videos page in `app.py`.
- Update the RFU links in `app.py` if the official destinations change.

The dependency list is maintained in `requirements.txt` (`streamlit>=1.35.0`).