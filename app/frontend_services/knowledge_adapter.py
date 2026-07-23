from services.runtime import kernel


def search_knowledge(query: str):

    agent = kernel.registry.get(
        "knowledge"
    )

    if agent is None:
        return []


    documents = agent.retriever.retrieve(
        query
    )


    results = []

    for doc in documents:

        results.append(
            {
                "Title": doc.metadata.get(
                    "source",
                    "Unknown"
                ),

                "Summary": doc.page_content[:300],

                "Confidence": "Retrieved"
            }
        )


    return results