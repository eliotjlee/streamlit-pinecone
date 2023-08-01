from streamlit.connections import ExperimentalBaseConnection
import streamlit as st
import pinecone

class PineconeConnection(ExperimentalBaseConnection[pinecone.Index]):
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
