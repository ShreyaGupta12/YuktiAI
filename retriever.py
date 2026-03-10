def retrieve_regulation(query):

    with open("regulations.txt") as f:
        docs = f.readlines()

    query = str(query).lower()

    results = []

    for d in docs:

        line = d.lower()

        if "temperature" in query and "temperature" in line:
            results.append(d)

        elif "sterilization" in query and "sterilization" in line:
            results.append(d)

        elif "operator" in query and "operator" in line:
            results.append(d)

        elif "contamination" in query and "contamination" in line:
            results.append(d)

    # fallback if nothing found
    if len(results) == 0:
        results = docs[:2]

    return results[:3]
