# ML Movie Recommendation Engine

A simple movie recommendation web app built with Streamlit that suggests similar movies and displays their posters using The Movie Database (TMDb). The app uses a precomputed similarity matrix and a movies dataset to find recommendations.

## Features
- Select a movie from the dataset and get the top 5 similar movie recommendations.
- Fetches and displays movie posters from TMDb.
- Automatically downloads the similarity matrix (similarity.pkl) from a hosted Hugging Face URL if not present.

## Demo
Run the app locally and open the Streamlit UI in your browser to choose a movie and view recommendations (poster + title).

## Requirements
- Python 3.8+
- pip

Recommended Python packages (example):
- streamlit
- pandas
- numpy
- requests

You can create a `requirements.txt` with:
```
streamlit
pandas
numpy
requests
```

Install with:
```
pip install -r requirements.txt
```

## Files
- `app.py` — Streamlit app that loads `movies.pkl` and `similarity.pkl`, finds recommendations, and displays posters.
- `movies.pkl` — Pickled pandas DataFrame with movie metadata (title, movie_id, etc.). Place this file in the repository root.
- `similarity.pkl` — Pickled similarity matrix. The app attempts to download it automatically from:
  `https://huggingface.co/datasets/aqeelabdullah654/movie-recommender-files/resolve/main/similarity.pkl`
  If automatic download fails, download it manually and place it in the repository root.

## Setup & Run

1. Clone the repo:
```
git clone https://github.com/Abdullah929-design/ML-MOVIE-RECOMMENDATION-ENGINE.git
cd ML-MOVIE-RECOMMENDATION-ENGINE
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Ensure `movies.pkl` is present in the repository root. If `similarity.pkl` is missing, the app will try to download it automatically from the Hugging Face URL. If that fails, download it manually and place it in the root.

4. TMDb API key:
- The app uses TMDb to fetch posters. Replace the placeholder API key in `app.py` with your own TMDb API key.
- Recommended: export the key as an environment variable and update `app.py` to read it from `os.getenv("TMDB_API_KEY")` to avoid committing secrets.

Example change (recommended):
```python
# in app.py
api_key = os.getenv("TMDB_API_KEY", "your_api_key_here")
```
Then run:
```
export TMDB_API_KEY="your_real_tmdb_api_key"
```
(or set it in your OS/Powershell environment)

5. Run the Streamlit app:
```
streamlit run app.py
```

## Troubleshooting
- If `similarity.pkl` fails to download, ensure you have an internet connection and that the Hugging Face URL is accessible. You can manually download the file from the URL and place it in the repo root.
- If posters don't appear, verify your TMDb API key is valid and network access is allowed.
- If `movies.pkl` cannot be loaded, make sure it exists and is a pickled pandas DataFrame with at least `title` and `movie_id` columns.

## Security note
Do not commit API keys or other secrets to the repository. Use environment variables or secret management solutions.

## Contributing
Contributions are welcome. Suggested improvements:
- Replace the hardcoded TMDb API key with environment variable usage.
- Add unit tests and input validation.
- Add a requirements.txt and a GitHub Actions CI workflow.

## License
This project is provided as-is. Add a license file (e.g., MIT) if you want to make the terms explicit.

## Contact
For questions or help, open an issue or contact the repository owner.
