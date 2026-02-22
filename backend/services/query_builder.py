def build_query_from_structured_data(structured_data: list):

    findings = []

    for item in structured_data:
        status = item["status"].lower()

        if status != "normal":
            test_name = item["test_name"]
            value = item["value"]
            unit = item["unit"]

            if "sugar" in test_name.lower() or "glucose" in test_name.lower():
                findings.append(
                    f"Elevated fasting blood glucose ({value} {unit}), possible impaired fasting glucose or diabetes."
                )

            elif "vitamin d" in test_name.lower():
                findings.append(
                    f"Vitamin D deficiency ({value} {unit})."
                )

            else:
                findings.append(
                    f"{test_name} is {item['status']} ({value} {unit})."
                )

    if not findings:
        return "All lab findings are normal."

    return "Clinical interpretation required for: " + " ".join(findings)

    # Optional personalization layer (future-ready)
    if patient_info:
        age = patient_info.get("age", "")
        gender = patient_info.get("gender", "")
        base_query = f"{age}-year-old {gender} patient has the following abnormal lab findings: "

    return base_query + findings_text