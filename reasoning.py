from compliance_graph import compliance_graph


def analyze(bmr, regulations):

    reasoning = []
    cited_regulations = []

    severity = "MINOR"

    bmr_text = str(bmr).lower()

    # -----------------------------
    # Compliance Graph Reasoning
    # -----------------------------

    for node in compliance_graph:

        if node in bmr_text:

            rule = compliance_graph[node]

            reasoning.append(
                f"{node.capitalize()} parameter linked to risk: {rule['risk']}"
            )

            cited_regulations.append(rule["regulation"])

            if rule["severity"] == "CRITICAL":
                severity = "CRITICAL"

            elif rule["severity"] == "MAJOR" and severity != "CRITICAL":
                severity = "MAJOR"

    # -----------------------------
    # Temperature excursion check
    # -----------------------------

    if "temperature" in bmr:

        try:

            temp = bmr["temperature"]

            value = int(str(temp).replace("C", ""))

            if value > 25:

                reasoning.append(
                    f"Recorded temperature {temp} exceeds validated limit (25C)"
                )

                reasoning.append("Possible drug stability risk")

                severity = "CRITICAL"

        except:
            reasoning.append("Temperature format unclear")

    # -----------------------------
    # Sterilization check
    # -----------------------------

    if "sterilization" in bmr:

        if "not recorded" in str(bmr["sterilization"]).lower():

            reasoning.append("Sterilization step not recorded")

            reasoning.append("Risk of microbial contamination")

            severity = "CRITICAL"

    # -----------------------------
    # No issues detected
    # -----------------------------

    if len(reasoning) == 0:

        reasoning.append("No major compliance issues detected")

    # -----------------------------
    # Add retrieved regulations
    # -----------------------------

    for r in regulations:
        cited_regulations.append(r.strip())

    # Remove duplicates
    cited_regulations = list(set(cited_regulations))

    return severity, reasoning, cited_regulations