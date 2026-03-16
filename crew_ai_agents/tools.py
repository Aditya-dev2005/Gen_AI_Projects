from dotenv import load_dotenv
import os
load_dotenv()

from sentence_transformers import SentenceTransformer
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

import chromadb.utils.embedding_functions.openai_embedding_function as oai_ef
import chromadb.api.models.CollectionCommon as cc

class _LocalEF:
    def __call__(self, input):
        return _model.encode(list(input)).tolist()
    
    def name(self):
        return "default"

_local_ef = _LocalEF()

# Patch OpenAI EF class
oai_ef.OpenAIEmbeddingFunction = type(
    "OpenAIEmbeddingFunction", (), {
        "__call__": lambda self, input: _local_ef(input),
        "__init__": lambda self, *a, **kw: None,
        "name": lambda self: "default"
    }
)

# Patch CollectionCommon default
cc.DEFAULT_EMBEDDING_FUNCTION = _local_ef

from crewai_tools import YoutubeChannelSearchTool

yt_tool = YoutubeChannelSearchTool(
    youtube_channel_handle="https://www.youtube.com/channel/UCNU_lfiiWBdtULKOw6X0Dig"
)