def retrieve_regulation(query):

    with open("regulations.txt") as f:
        docs = f.readlines()

    query = query.lower()

    keywords = {
        "temperature": ["temperature", "heat", "cold"],
        "sterilization": ["sterilization", "sterile", "microbial"],
        "documentation": ["record", "document", "log"],
        "operator": ["operator", "personnel", "staff"]
    }

    results = []

    for doc in docs:

        doc_lower = doc.lower()

        for key in keywords:

            if any(word in query for word in keywords[key]) and key in doc_lower:
                results.append(doc)
                break

    # fallback if nothing matched
    if not results:
        results = docs[:2]

    return results[:2]