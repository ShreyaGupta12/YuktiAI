def retrieve_regulation(query):

    with open("regulations.txt") as f:
        docs = f.readlines()

    results = []

    for d in docs:
        if "temperature" in query.lower():
            results.append(d)

    return results[:2]