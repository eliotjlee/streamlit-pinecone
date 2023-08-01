import streamlit as st
from connections.pinecone_conn import PineconeConnection
from make_dataframe import make_result_dataframe
from embeddings import get_embeddings
import os

st.set_page_config(page_title="Movie Matcher", page_icon=":film_projector:", layout='wide', initial_sidebar_state='auto')

# Use custom connection to connect to Pinecone index
conn = st.experimental_connection(
    "pinecone", 
    type=PineconeConnection, 
    api_key=os.getenv('PINECONE_API_KEY'),
    environment=os.getenv('PINECONE_REGION'), 
    index_name='movies'
)

st.title("Welcome to Movie Matcher! :clapper:")

st.markdown("## **Enter your movie description below:**")
user_input = st.text_area(label='Type your description...', height=150, max_chars=2000)

st.markdown("<sub><sup>WARNING: Results may contain spoilers!</sup></sub>", unsafe_allow_html=True)

# After the user enters the query and presses Enter (or Ctrl+Enter), query Pinecone.
if st.button('Submit'):
    # Generate embeddings for user query
    embedded_query = get_embeddings(user_input)

    # Use Pinecone connection to query the index (default top_k = 10)
    results = conn.query(embedded_query, top_k=10, ttl=3600, includeValues=False)

    # Check if an error occurred during the query
    if "error" in results:
        st.error(results["error"])
    else:
        # Generate a dataframe using the returned results
        result_df = make_result_dataframe(results)

        if not result_df.empty:
            st.markdown("## **Here are the top 10 matching movies:**")

            # Display the resulting dataframe in a neat, aesthetic table.
            result_df.index = result_df.index + 1
            result_df['Year'] = result_df['Year'].astype(str)
            st.dataframe(result_df)
        else:
            st.markdown("**No matching movies found. Please try again with a different description.**")

st.markdown('''
    ## About
    This web application provides an interactive way to explore a dataset of approximately 35,000 movies using a text description. The movie dataset has been transformed into vector representations using OpenAI's Embeddings API and indexed with Pinecone. When you input a search query, it is also converted into a vector using the same process, and this vector is then used to query the Pinecone index. The application returns the top 10 movies whose plot descriptions are most semantically similar to your query.

    Please note that semantic similarity search relies on the nuanced understanding of language captured in the vector embeddings. It is not 100% perfect and the performance can vary based on the specificities and details provided in your description. The more specific and contextually rich your search query is, the higher the chance of obtaining accurate and relevant results.

    This tool was developed as part of Streamlit's Connections Hackathon and showcases the power and flexibility of Streamlit's data connections functionality (ExperimentalBaseConnection). You can find the source code, along with the custom Pinecone connection class, on [GitHub](https://github.com/eliotjlee/movie-matcher)

    ''')


st.markdown("""
<style>
.small-font {
    font-size:0.8em;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="small-font">
This application uses a dataset of movie plots derived from Wikipedia, made available on 
<a href="https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots" target="_blank">Kaggle</a> by user jrobischon. Modifications were made to the dataset to include an index row for vector identification. This dataset is licensed under a 
<a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License</a>. In accordance with this license, any adaptations of this dataset must also be released under the same license.
</div>
""", unsafe_allow_html=True)