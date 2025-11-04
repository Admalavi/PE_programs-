# Expert System: Disease Diagnosis with Weighted Symptoms and Confidence Scores
# Developed by Akshata Malavi 

def run_weighted_expert_system(predefined_answers=None):
    # Weighted rule base: disease -> {symptom: weight}
    rules = {
        "Common Cold": {
            "sneezing": 2, "sore throat": 1.5, "runny nose": 2, "mild fever": 1
        },
        "Flu": {
            "high fever": 3, "body ache": 2.5, "fatigue": 2, "dry cough": 2
        },
        "Allergy": {
            "sneezing": 2, "itchy eyes": 2.5, "runny nose": 1.5, "no fever": 1
        },
        "COVID-19": {
            "fever": 3, "dry cough": 2, "loss of taste or smell": 3, "difficulty breathing": 2.5
        },
        "Strep Throat": {
            "sore throat": 3, "high fever": 2.5, "swollen lymph nodes": 2, "no cough": 1.5
        }
    }

    # Collect all unique symptoms
    all_symptoms = sorted({s for disease in rules.values() for s in disease})

    def key(sym): 
        return sym.lower()

    # ✅ Ask user for each symptom
    answers = {}
    print("Answer the following with 'y' (yes) or 'n' (no):\n")
    for s in all_symptoms:
        while True:
            resp = input(f"Do you have '{s}'? [y/n]: ").lower().strip()
            if resp in ("y", "n", "yes", "no"):
                answers[key(s)] = 1 if resp.startswith("y") else 0
                break
            print("Please answer 'y' or 'n'.")

    # Weighted reasoning
    results = []
    for disease, symptoms in rules.items():
        total_weight = sum(symptoms.values())
        matched_weight = sum(weight for sym, weight in symptoms.items() if answers.get(key(sym), 0) == 1)
        confidence = (matched_weight / total_weight) * 100 if total_weight > 0 else 0
        results.append((disease, matched_weight, total_weight, confidence))

    results.sort(key=lambda x: x[3], reverse=True)

    # Display reasoning
    print("\n--- Reasoning Trace ---")
    for disease, matched, total, conf in results:
        bar = "█" * int(conf / 5) + "-" * (20 - int(conf / 5))
        print(f"{disease.ljust(15)} | Confidence: {conf:5.1f}% | {bar}")

    high_threshold = 70
    medium_threshold = 40

    top_disease, _, _, top_conf = results[0]
    print("\n--- Diagnosis Result ---")

    if top_conf >= high_threshold:
        print(f"✅ Most likely diagnosis: **{top_disease}** (Confidence: {top_conf:.1f}%)")
        print("→ High confidence based on your symptoms.")
    elif top_conf >= medium_threshold:
        print(f"⚠️ Possible diagnosis: **{top_disease}** (Confidence: {top_conf:.1f}%)")
        print("→ Medium confidence; further tests or observation advised.")
    else:
        print(f"❓ Low confidence in diagnosis (Top match: {top_disease}, {top_conf:.1f}%)")
        print("→ Insufficient data. Please provide more symptoms or consult a doctor.")

    # Explanation
    print(f"\n--- Explanation for {top_disease} ---")
    print("Rules:", list(rules[top_disease].keys()))
    print("Matched Symptoms:",
          [sym for sym in rules[top_disease] if answers.get(key(sym), 0) == 1])
    print("Unmatched Symptoms:",
          [sym for sym in rules[top_disease] if answers.get(key(sym), 0) == 0])

    return results


# --- RUN SYSTEM ---
run_weighted_expert_system()
