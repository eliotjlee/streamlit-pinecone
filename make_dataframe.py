import pandas as pd

# Inject results into a dataframe for display on Streamlit app
def make_result_dataframe(results):
    # load the movie dataset as a DataFrame
    data_frame = pd.read_csv("./data/wiki_movie_plots_deduped_with_id.csv")

    # create an empty DataFrame to store your results
    result_df = pd.DataFrame(columns=["Year", "Title", "Genre", "Director", "Nationality", "Synopsis", "Similarity Score", "Wikipedia Link"])

    # iterate over the results in the JSON object
    for match in results['matches']:
        # extract the id and score
        movie_id = match['id']
        similarity_score = match['score']
        
        # find the movie in your data_frame
        movie_data = data_frame[data_frame["id"] == int(movie_id)].iloc[0]
        
        # create a dictionary with the movie data and similarity score
        movie_dict = {
            "Year": movie_data["Release Year"],
            "Title": movie_data["Title"],
            "Genre": movie_data["Genre"],
            "Director": movie_data["Director"],
            "Nationality": movie_data["Origin/Ethnicity"],
            "Synopsis": movie_data["Plot"],
            "Similarity Score": similarity_score,
            "Wikipedia Link": movie_data["Wiki Page"]
        }
        
        # append this data to result DataFrame
        result_df = pd.concat([result_df, pd.DataFrame(movie_dict, index=[0])], ignore_index=True)

    return result_df