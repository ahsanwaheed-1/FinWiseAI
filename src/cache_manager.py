from langchain_core.caches import InMemoryCache
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache

def setup_cache(cache_type):
    """
    Sets up the LangChain cache based on user selection.
    cache_type: "In-Memory" or "SQLite"
    """
    if cache_type == "In-Memory":
        set_llm_cache(InMemoryCache())
    elif cache_type == "SQLite":
        set_llm_cache(SQLiteCache(database_path=".langchain.db"))
    else:
        # Default to no cache if something weird is passed
        set_llm_cache(None)
