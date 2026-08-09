import streamlit as st
import pickle
import requests
import os

# -----------------------------
# Function to fetch movie poster
# -----------------------------
def fetch_poster(movie_id):
    api_key = "117c8d6e27ad7ccca41f4b79f4534b4f"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        data = requests.get(url, timeout=10).json()
    except Exception:
        return "https://via.placeholder.com/500x750?text=No+Image"
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


# -----------------------------
# Function to recommend movies
# -----------------------------
def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies_df.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


# -----------------------------
# Download + validation helpers
# -----------------------------
def download_file(url, dest):
    """Download a file, following redirects, and raise if it fails."""
    response = requests.get(url, stream=True, timeout=60, allow_redirects=True)
    response.raise_for_status()
    with open(dest, 'wb') as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)


def is_valid_pickle_file(path, min_size_bytes=1000):
    """Reject files that are too small, HTML pages, or git-lfs pointer stubs."""
    if not os.path.exists(path):
        return False
    if os.path.getsize(path) < min_size_bytes:
        return False
    with open(path, 'rb') as f:
        header = f.read(50)
    if header.startswith(b'<') or header.startswith(b'version https://git-lfs'):
        return False
    return True


def ensure_file(url, dest, label):
    """Make sure `dest` exists locally and is a real pickle file, downloading (and retrying with
    ?download=true) if needed."""
    if not is_valid_pickle_file(dest):
        if os.path.exists(dest):
            os.remove(dest)
        st.info(f"Downloading {label}...")
        try:
            download_file(url, dest)
        except Exception as e:
            st.error(f"Failed to download {label}: {e}")

        # If still invalid, retry once with the forced-download query param (common HF fix)
        if not is_valid_pickle_file(dest):
            if os.path.exists(dest):
                os.remove(dest)
            forced_url = url if 'download=true' in url else url + ('&' if '?' in url else '?') + 'download=true'
            try:
                download_file(forced_url, dest)
            except Exception as e:
                st.error(f"Retry failed to download {label}: {e}")

    if not is_valid_pickle_file(dest):
        st.error(
            f"{label} could not be downloaded correctly (file is missing, too small, "
            f"an HTML page, or a git-lfs pointer). Check the source URL and sharing settings."
        )
        st.stop()


# -----------------------------
# Load data
# -----------------------------
MOVIES_URL = 'https://huggingface.co/datasets/aqeelabdullah654/movie-recommender-files/resolve/main/movies.pkl'
SIMILARITY_URL = 'https://huggingface.co/datasets/aqeelabdullah654/movie-recommender-files/resolve/main/similarity.pkl'

MOVIES_PATH = 'movies.pkl'
SIMILARITY_PATH = 'similarity.pkl'

ensure_file(MOVIES_URL, MOVIES_PATH, 'movies.pkl')
ensure_file(SIMILARITY_URL, SIMILARITY_PATH, 'similarity.pkl')

try:
    movies_df = pickle.load(open(MOVIES_PATH, 'rb'))
    similarity = pickle.load(open(SIMILARITY_PATH, 'rb'))
except Exception as e:
    st.error(f"Failed to load pickle files even after download: {e}")
    st.stop()

movies_list = movies_df['title'].values

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Select a Movie", movies_list)

if st.button("Show Recommendations"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)  # 5 columns for 5 recommendations
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        col.text(name)
        col.image(poster, use_container_width=True)
