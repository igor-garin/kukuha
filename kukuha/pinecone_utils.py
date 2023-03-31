import hashlib
from typing import List, Dict, Any

import pinecone

import settings

pinecone.init(
    api_key=settings.PINECONE_API_KEY,
    environment=settings.PINECONE_ENV
)


def pinecone_get_or_create_index(index_name: str) -> pinecone.Index:
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            index_name,
            dimension=settings.EMB_DIMENSION,
            metric='cosine'
        )
    # connect to index
    index = pinecone.Index(index_name)

    # view index stats
    # index.describe_index_stats()
    # {'dimension': 1536,
    #  'index_fullness': 0.1,
    #  'namespaces': {'': {'vector_count': 48688}},
    #  'total_vector_count': 48688}

    return index


def pinecone_upsert_embeds(index: pinecone.Index,
                           embeds: List[List[float]],
                           embeds_meta: List[Dict[str, str]]) -> None:
    embeds_ids = []
    for meta in embeds_meta:
        m = hashlib.sha256()
        m.update(meta['text'].encode('utf-8'))
        embeds_ids.append(m.hexdigest())

    to_upsert = list(zip(embeds_ids, embeds, embeds_meta))
    index.upsert(vectors=to_upsert)


def pinecone_upsert_single_embed(index: pinecone.Index,
                                 embed: List[float],
                                 embed_meta: Dict[str, str]) -> None:
    pinecone_upsert_embeds(index, [embed], [embed_meta])


def pinecone_query_embed(index: pinecone.Index, embed: List[float]) -> List[Dict[str, Any]]:
    query_res = index.query(embed, top_k=3, include_metadata=True)
    matches = [
        q['metadata']
        for q in query_res['matches']
    ]
    return matches
