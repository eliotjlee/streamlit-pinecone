"""
This module provides the PineconeConnection class, which allows Streamlit users to instantiate a Pinecone index object and use all of the Pinecone API's operations on it. 
This is an implementation of Streamlit's BaseConnection for Pinecone, written for Streamlit's connections hackathon.

The class includes the following public methods:

- `index()`: Returns the Pinecone index.
- `query(embeddings: list, top_k: int = 10, ttl: int = 3600, **kwargs) -> dict`: Queries the Pinecone index with the provided embeddings and returns the top_k similar items.
- `describe_index_stats(ttl: int = 3600, **kwargs) -> str`: Returns statistics about the Pinecone index's contents.
- `delete(ids: list = None, delete_all: bool = None, namespace: str = None, filter: dict = None, ttl: int = 3600, **kwargs) -> dict`: Deletes vectors, by id, from a single namespace.
- `update(id: str, values: list = None, sparse_values: dict = None, set_metadata: dict = None, namespace: str = None, ttl: int = 3600, **kwargs) -> dict`: Updates a vector in a namespace.
- `fetch(ids: list, ttl: int = 3600, namespace: str = None, **kwargs) -> dict`: Looks up and returns vectors, by ID, from a single namespace.
- `upsert(vectors: list, ttl: int = 3600, namespace: str = None, **kwargs) -> dict`: Writes vectors into a namespace.

Results from `query`, `describe_index_stats`, `delete`, `update`, `fetch`, and `upsert` methods are cached for a specified ttl (time-to-live) duration to optimize the performance of your Streamlit app.
"""

from streamlit.connections import BaseConnection
import streamlit as st
import pinecone


class PineconeConnection(BaseConnection[pinecone.Index]):
    def _connect(self, **kwargs) -> pinecone.Index:
        """Connects to a Pinecone index."""
        if 'api_key' in kwargs:
            api_key = kwargs.pop('api_key')
        else:
            api_key = self._secrets['api_key']

        if 'environment' in kwargs:
            environment = kwargs.pop('environment')
        else:
            environment = self._secrets['environment']

        pinecone.init(api_key=api_key, environment=environment)

        if 'index_name' in kwargs:
            index_name = kwargs.pop('index_name')
        else:
            index_name = self._secrets['index_name']

        return pinecone.Index(index_name)

    def index(self) -> pinecone.Index:
        """Returns the Pinecone index."""
        return self._instance

    def query(self, embeddings: list, top_k: int = 10, ttl: int = 3600, **kwargs) -> dict:
        """
        Queries the Pinecone index with the provided embeddings.
        Returns top_k similar items from the index.
        Results are cached for ttl seconds.
        """

        @st.cache_data(ttl=ttl)
        def _query(embeddings: list, top_k: int, **kwargs) -> dict:
            # Query the Pinecone index
            try:
                results = self.index().query(vector=embeddings, top_k=top_k, **kwargs)
                results_dict = results.to_dict()
            except Exception as e:
                # Return an error message if the query fails
                return {"error": f"Query failed: {str(e)}"}
            return results_dict

        return _query(embeddings, top_k, **kwargs)

    def describe_index_stats(self, ttl: int = 3600, **kwargs) -> str:
        """
        Returns statistics about the Pinecone index's contents.
        Statistics include the vector count per namespace and the number of dimensions.
        Results are cached for ttl seconds.
        """

        @st.cache_data(ttl=ttl)
        def _describe_index_stats(**kwargs) -> str:
            # Describe the Pinecone index stats
            try:
                response = self.index().describe_index_stats(**kwargs)
            except Exception as e:
                # Return an error message if the operation fails
                return {"error": f"Describe index stats failed: {str(e)}"}

            return response

        return _describe_index_stats(**kwargs)

    def delete(self, ids: list = None, delete_all: bool = None, namespace: str = None, filter: dict = None,
               ttl: int = 3600, **kwargs) -> dict:
        """
        Deletes vectors, by id, from a single namespace.
        You can delete items by their id, from a single namespace.
        Results are cached for ttl seconds.
        """

        @st.cache_data(ttl=ttl)
        def _delete_vectors(ids: list, delete_all: bool, namespace: str, filter: dict, **kwargs) -> dict:
            # Delete vectors from the Pinecone index
            try:
                if ids is None and delete_all is None and filter is None:
                    raise ValueError("At least one of 'ids', 'delete_all', or 'filter' must be provided.")

                response = self.index().delete(ids=ids, delete_all=delete_all, namespace=namespace, filter=filter,
                                               **kwargs)
            except Exception as e:
                # Return an error message if the operation fails
                return {"error": f"Delete vectors failed: {str(e)}"}

            return response

        return _delete_vectors(ids, delete_all, namespace, filter, **kwargs)

    def update(self, id: str, values: list = None, sparse_values: dict = None, set_metadata: dict = None,
               namespace: str = None, ttl: int = 3600, **kwargs) -> dict:
        """
        Updates a vector in a namespace.
        If a value is included, it will overwrite the previous value.
        If set_metadata is included, the values of the fields specified in it will be added or overwrite the previous value.
        Results are cached for ttl seconds.
        """

        @st.cache_data(ttl=ttl)
        def _update_vector(id: str, values: list, sparse_values: dict, set_metadata: dict, namespace: str,
                           **kwargs) -> dict:
            # Update vector in the Pinecone index
            try:
                if values is None and sparse_values is None and set_metadata is None:
                    raise ValueError("At least one of 'values', 'sparse_values', or 'set_metadata' must be provided.")

                response = self.index().update(id=id, values=values, sparse_values=sparse_values,
                                               set_metadata=set_metadata, namespace=namespace, **kwargs)
            except Exception as e:
                # Return an error message if the operation fails
                return {"error": f"Update vector failed: {str(e)}"}

            return response

        return _update_vector(id, values, sparse_values, set_metadata, namespace, **kwargs)

    def fetch(self, ids: list, ttl: int = 3600, namespace: str = None, **kwargs) -> dict:
        """
        Looks up and returns vectors, by ID, from a single namespace.
        The returned vectors include the vector data and/or metadata.
        Results are cached for ttl seconds.
        """

        @st.cache_data(ttl=ttl)
        def _fetch_vectors(ids: list, namespace: str, **kwargs) -> dict:
            # Fetch vectors from the Pinecone index
            try:
                if not ids:
                    raise ValueError("'ids' must be provided.")

                response = self.index().fetch(ids=ids, namespace=namespace, **kwargs)
                response_dict = response.to_dict()
            except Exception as e:
                # Return an error message if the operation fails
                return {"error": f"Fetch vectors failed: {str(e)}"}

            return response_dict

        return _fetch_vectors(ids, namespace, **kwargs)

    def upsert(self, vectors: list, ttl: int = 3600, namespace: str = None, **kwargs) -> dict:
        """
        Writes vectors into a namespace.
        If a new value is upserted for an existing vector id, it will overwrite the previous value.
        Results are cached for ttl seconds.
        """

        @st.cache_data(ttl=ttl)
        def _upsert_vectors(vectors: list, namespace: str, **kwargs) -> dict:
            # Upsert vectors in the Pinecone index
            try:
                if not vectors:
                    raise ValueError("'vectors' must be provided.")

                response = self.index().upsert(vectors=vectors, namespace=namespace, **kwargs)
                response_dict = response.to_dict()
            except Exception as e:
                # Return an error message if the operation fails
                return {"error": f"Upsert vectors failed: {str(e)}"}

            return response_dict

        return _upsert_vectors(vectors, namespace, **kwargs)
