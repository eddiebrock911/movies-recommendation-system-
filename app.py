import streamlit as st
import pickle
import pandas as pd

# streamlit run app.py

# Page configuration
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# Load the data
@st.cache_data
def load_data():
    #movies = pickle.load(open('movies.pkl', 'rb'))
    # Google Drive file ID extract karo
    

    # Movies pickle
    #sim_file_id = "1xrydZhyakntow9_IZSmsx_bGEYQxVWCG"

    #movies = pickle.load(open('movies.pkl', 'rb'))

    # Similarity.pkl download
    ##similarity = f"https://drive.google.com/uc?id={sim_file_id}"
    return movies_df, similarity

try:
    sim_file_id = "1xrydZhyakntow9_IZSmsx_bGEYQxVWCG"
    sim_url = f"https://drive.google.com/uc?id={sim_file_id}"
    movies_df = pickle.load(open('movies.pkl', 'rb'))
    similarity = f"https://drive.google.com/uc?id={sim_file_id}"
    #movies_df, similarity = load_data()
except:
    st.error("⚠️ Error loading data files. Please ensure 'movies.pkl' and 'similarity.pkl' are in the same directory.")
    st.stop()

# Recommendation function
def recommend(movie_title):
    try:
        movie_index = movies_df[movies_df['title'] == movie_title].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append({
                'title': movies_df.iloc[i[0]].title,
                'similarity': f"{i[1]:.2%}"
            })
        return recommended_movies
    except IndexError:
        return None

# Header
st.title("🎬 Movie Recommendation System")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info(
        "This recommendation system suggests movies based on content similarity. "
        "Select a movie you like, and we'll recommend similar ones!"
    )
    st.markdown("---")
    st.markdown("**Features:**")
    st.markdown("- 🎯 Content-based filtering")
    st.markdown("- 🔍 5000+ movies database")
    st.markdown("- ⚡ Fast recommendations")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Select a Movie")
    selected_movie = st.selectbox(
        "Choose a movie you like:",
        movies_df['title'].values,
        index=None,
        placeholder="Search for a movie..."
    )

with col2:
    st.subheader("Get Recommendations")
    recommend_button = st.button("🎯 Find Similar Movies", use_container_width=True)

# Display recommendations
if recommend_button and selected_movie:
    with st.spinner('Finding similar movies...'):
        recommendations = recommend(selected_movie)
        
        if recommendations:
            st.success(f"✨ Movies similar to **{selected_movie}**:")
            st.markdown("---")
            
            # Display in cards
            cols = st.columns(5)
            for idx, movie in enumerate(recommendations):
                with cols[idx]:
                    st.markdown(
                        f"""
                        <div style='
                            background-color: #8edbe6;
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                            height: 150px;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                        '>
                            <h4 style='font-size: 16px; margin-bottom: 10px;'>{idx + 1}. {movie['title']}</h4>
                            <p style='color: #666; font-size: 14px;'>Match: {movie['similarity']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Alternative list view
            st.markdown("---")
            with st.expander("📋 View as List"):
                for idx, movie in enumerate(recommendations, 1):
                    st.write(f"{idx}. **{movie['title']}** - Similarity: {movie['similarity']}")
        else:
            st.error("Movie not found in database. Please try another one.")

elif recommend_button and not selected_movie:
    st.warning("⚠️ Please select a movie first!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with Ankit ❤️ using Streamlit | Data: TMDB 5000 Movies Dataset"
    "</div>",
    unsafe_allow_html=True
)