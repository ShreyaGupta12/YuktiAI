def analyze(bmr, regulations):

    deviation = bmr["deviation"]

    reasoning = []

    if "temperature" in deviation.lower():

        reasoning.append("Temperature exceeded validated limit")
        reasoning.append("Possible stability risk")
        reasoning.append("Deviation investigation required")

        severity = "CRITICAL"

    else:

        reasoning.append("Deviation within acceptable range")

        severity = "MINOR"

    return severity, reasoning