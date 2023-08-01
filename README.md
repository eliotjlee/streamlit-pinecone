# Movie Matcher 

Movie Matcher is a web application built with Streamlit and Pinecone that uses semantic similarity search to find movies with plot descriptions similar to a user-provided description.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [License](#license)
- [Attributions](#attributions)

## Overview

This application allows users to explore a dataset of approximately 35,000 movies by inputting a description of a movie plot. The provided description is transformed into a vector using OpenAI's Embeddings API. This vector is then used to query a Pinecone index containing vectors of movie plot descriptions. The application returns the top 10 movies from the dataset whose plot descriptions are most semantically similar to the input.

This project was developed as part of Streamlit's Connections Hackathon and showcases the functionality of Streamlit's data connections functionality (ExperimentalBaseConnection).

## Getting Started

To set up and run this application, you will need to:

1. Clone this repository.
2. Install the required dependencies. These can be found in the `requirements.txt` file.
3. Run the application with Streamlit using `streamlit run app/app.py`

## Usage

After starting the application, simply enter a description of a movie plot into the input box and click the 'Find Similar Movies' button. The application will return a list of 10 movies with similar plot descriptions from the dataset, along with their year of release, title, director, nationality, genre, synopsis, similarity score, and a link to their Wikipedia page.

## License

This project is licensed under the terms of the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License](https://creativecommons.org/licenses/by-sa/4.0/).

## Attributions

This application uses a dataset of movie plots derived from Wikipedia, made available on [Kaggle](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots) by user jrobischon. Modifications were made to the dataset to include an index row for vector identification. This dataset is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License](https://creativecommons.org/licenses/by-sa/4.0/). In accordance with this license, any adaptations of this dataset must also be released under the same license.
