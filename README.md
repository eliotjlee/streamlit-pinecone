## Streamlit Pinecone Connection

This repo includes the `PineconeConnection` class, an `st.connection` wrapper for integrating the Pinecone API into Streamlit applications. It facilitates the use of Pinecone's powerful indexing and querying capabilities directly within Streamlit, making it ideal for building sophisticated search and data retrieval applications.

### Features

- **Instantiate Pinecone Index**: Seamlessly connect to a Pinecone index.
- **Rich Query Capabilities**: Perform queries with embeddings, retrieve top_k similar items.
- **Index Insights**: Gather statistics about the Pinecone index's contents.
- **Comprehensive Vector Operations**: Includes methods for deleting, updating, fetching, and upserting vectors in a namespace.
- **Caching for Performance**: Results from various methods are cached to enhance the performance of your Streamlit app.

### Installation

Install the package using pip:

```
pip install streamlit-pinecone
```

### Usage

Import and initialize the connection in your Streamlit app:

```python
from streamlit_pinecone import PineconeConnection

# Initialize the connection
conn = PineconeConnection(api_key='your_api_key', environment='your_environment', index_name='your_index_name')

# Use the connection
results = conn.query([...])
```

### Example

![Movie Matcher Demo](https://i.imgur.com/JMEepUP.jpg)

For a live demo, check out [Movie Matcher](movie-matcher.streamlit.app)!

You can find the source code under `\demo\` directory.



## Documentation

### PineconeConnection Class

The `PineconeConnection` class provides methods to interact with Pinecone indexes within a Streamlit app.

---

#### `index()`
**Returns**: `pinecone.Index`  
**Description**: Returns the Pinecone index instance.

---

#### `query(embeddings, top_k=10, ttl=3600, **kwargs)`
**Parameters**:
  - `embeddings`: List of embeddings for the query.
  - `top_k` (int, optional): Number of top similar items to return. Default is 10.
  - `ttl` (int, optional): Time-to-live for cache in seconds. Default is 3600.  
**Returns**: Dictionary of query results.  
**Description**: Queries the Pinecone index with provided embeddings.

---

#### `describe_index_stats(ttl=3600, **kwargs)`
**Parameters**:
  - `ttl` (int, optional): Time-to-live for cache in seconds. Default is 3600.  
**Returns**: String describing index statistics.  
**Description**: Provides statistics about the Pinecone index's contents.

---

#### `delete(ids, delete_all=None, namespace=None, filter=None, ttl=3600, **kwargs)`
**Parameters**:
  - `ids` (list): List of IDs to delete.
  - `delete_all` (bool, optional): Flag to delete all vectors.
  - `namespace` (str, optional): Namespace from which to delete.
  - `filter` (dict, optional): Filter criteria for deletion.
  - `ttl` (int, optional): Time-to-live for cache in seconds.  
**Returns**: Dictionary of deletion results.  
**Description**: Deletes vectors by ID from a namespace.

---

#### `update(id, values=None, sparse_values=None, set_metadata=None, namespace=None, ttl=3600, **kwargs)`
**Parameters**:
  - `id` (str): ID of the vector to update.
  - `values`, `sparse_values`, `set_metadata`: Data for update.
  - `namespace` (str, optional): Namespace to update.
  - `ttl` (int, optional): Time-to-live for cache in seconds.  
**Returns**: Dictionary of update results.  
**Description**: Updates a vector in a namespace.

---

#### `fetch(ids, ttl=3600, namespace=None, **kwargs)`
**Parameters**:
  - `ids` (list): List of IDs to fetch.
  - `ttl` (int, optional): Time-to-live for cache in seconds.
  - `namespace` (str, optional): Namespace to fetch from.  
**Returns**: Dictionary of fetched vectors.  
**Description**: Fetches vectors by ID from a namespace.

---

#### `upsert(vectors, ttl=3600, namespace=None, **kwargs)`
**Parameters**:
  - `vectors` (list): List of vectors to upsert.
  - `ttl` (int, optional): Time-to-live for cache in seconds.
  - `namespace` (str, optional): Namespace to upsert into.  
**Returns**: Dictionary of upsert results.  
**Description**: Writes vectors into a namespace.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For more information, visit the [GitHub repository](https://github.com/yourusername/your-repo).

### Contact

Eliot Lee - eliotlee2026@u.northwestern.edu

### Acknowledgments

Special thanks to the Streamlit team and the Streamlit Developer Relations team for their support and for featuring this project in the Streamlit components gallery.

