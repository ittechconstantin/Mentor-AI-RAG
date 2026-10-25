import os

import chromadb
from chromadb.utils import embedding_functions


functie_embedding = embedding_functions.OpenAIEmbeddingFunction(
    api_key = os.environ["OPENAI_API_KEY"],
    model_name="text-embedding-3-small"
)

client = chromadb.Client()
colectie = client.create_collection(
    name="s50_ghiduri",
    embedding_function=functie_embedding,
)


def indexeaza_ghid(ghid):
    colectie.add(ids =[str(ghid.id)],documents = [ghid.continut],metadatas =[{"titlu": ghid.titlu}])

def indexeaza_toate(ghiduri):
    for ghid in ghiduri:
        indexeaza_ghid(ghid)
    return (f"Index RAG: {colectie.count()} ghiduri.")

def sterge_din_index(ghid_id):
    colectie.delete(ids=[str(ghid_id)])


def cauta(intrebare, n_rezultate=2):
    rezultat = colectie.query(query_texts=[intrebare], n_results=n_rezultate)
    texte = rezultat["documents"][0]
    metadate = rezultat["metadatas"][0]
    distante = rezultat["distances"][0]
    lista = []
    for i in range(len(texte)):
        lista.append({"titlu" :metadate[i]["titlu"],
                      "text" :texte[i],
                      "distanta": round(distante[i], 3)})
    return lista

