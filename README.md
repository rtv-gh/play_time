# Rugby Festival Planner

A Streamlit app for planning junior rugby festival squads and tracking playing time.

## Features

- Choose an RFU age group from U7 to U11 and see the players-per-side requirement.
- Generate a fair half-by-half schedule for 3 to 6 games, with opposition names.
- Compare scheduled and actual playing time, including changes for substitutions or injuries.
- Export the playing-time comparison as a CSV file.
- Navigate between Home, Age regulations, and Videos.
- Open official RFU age-grade regulations from the app. The Age regulations page has U7-U11 sections ready for summaries.
- Watch locally stored MP4 coaching videos grouped by topic. Video details are maintained separately from the app in `videos.json`.
- Use the app on desktop or portrait mobile screens.

Player names must be unique. The app starts with example player names, which can be edited in the squad editor.

## Project files

```text
project-root/
├── play_time/
│   ├── app.py            # Streamlit interface and page navigation
│   ├── utils.py          # Squad allocation and schedule generation
│   ├── videos.json       # Video titles, topics, and filenames
│   ├── requirements.txt  # Python dependencies
│   └── README.md
└── videos/
	└── video_tackling_technique_1.mp4
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
3. Keep both `play_time/` and `videos/` in the repository root, and set the main file path to `play_time/app.py`. The app reads media from the sibling `videos/` directory.
4. Deploy. Streamlit installs dependencies from `requirements.txt`.

## Update video content

Put each MP4 file in the project-root `videos/` directory, then add an object to `play_time/videos.json`:

```json
{
	"topic": "Passing",
	"title": "Passing fundamentals",
	"file": "video_passing_fundamentals.mp4"
}
```

The app plays each local file with Streamlit's video player. Videos with matching `topic` values are displayed under the same heading; add more objects to the JSON array to grow a topic or introduce a new one. Keep the JSON valid (double quotes, commas between fields and items).

## Video file considerations

- Keep the `videos/` folder in the deployed repository next to `play_time/`; otherwise the app will show a missing-file warning.
- GitHub blocks individual files larger than 100 MiB and warns for files over 50 MiB. Compress videos before committing, for example as H.264/AAC MP4 at a practical resolution and bitrate.
- Large media makes repository clones and deployments slower, consumes repository storage, and uses app bandwidth each time coaches play videos. Deleting a large file in a later commit does not remove it from Git history.
- Streamlit Community Cloud documents approximate resource limits of 50 GB storage and up to 2.7 GB memory per app; these limits can change. The storage figure is an app resource limit, not a per-video upload allowance. Keep enough headroom for the app and playback, and check current Cloud limits before deploying a large library.
- For a growing library or large originals, consider object storage or a dedicated video host/CDN and store URLs instead of committing the files.
- Test playback on phones and the deployed app. Check that videos are licensed for reuse and avoid including private or sensitive footage.

## Maintain other content

- Add age-group summaries to the corresponding U7-U11 sections in the Age regulations page in `app.py`.
- Update the RFU links in `app.py` if the official destinations change.
- Keep video metadata in `videos.json`, media in the project-root `videos/` folder, and layout/rendering changes in `app.py`.

The dependency list is maintained in `requirements.txt` (`streamlit>=1.35.0`).