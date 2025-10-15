#expert system: disease diagnosis

def run_weighted_expert_system(predefined_answers=None):
    #weighted rule base:disase 
    rules = {
        "common cold":{
            "sneezing":2, "sore throat":1.5, "runny nose":2, "mild fever":1
        },
        "flu":{
            "high fever":3, "body ache":2.5, "fatigue":2, "dry cough":2
        },
        "Allergy":{
            "sneezing":2, "itchy eyes":2.5, "runny nose":1.5, "no fever":1
        },
        "COVID-19":{
            "fever":3, "dry cough":2, "loss of taste and smell":3, "difficulty breathing":2.5
        },
        "strep throat":{
            "sore throat":3, "high fever":2.5, "swollen lymph nodes":2, "no cold":1.5
        }
    }


    #collect all unique symptoms
    all_symptoms = sorted({s for disease in rules.values() for s in disease})

    #helper to normalize keys
    def key(sym): return sym.lower()


    #collect answers
    answers = {}

    if predefined_answers is None:
        print("answer the following with 'y'(yes) or 'n'(no):")
        for s in all_symptoms:
            while True:
                resp = input(f"do you have '{s}' ? [y/n]: ").lower().strip()
                if resp in ("y","n","yes","no"):
                    answers[key(s)]= 1 if resp.startswith("y") else 0
                    break
                print("please answer 'y' or 'n'.")

    else:
        for s in all_symptoms:
            val = predefined_answers.get(s, predefined_answers.get(key(s), "n"))
            if isinstance(val, str):
                answers[key(s)] = 1 if val.lower().startswith("y") else 0

            else:
                answers[key(s)] = 1 if bool(val) else 0


    #weighted reasoning

    results = []
    for disease, symptoms in rules.items():
        total_weight = sum(symptoms.values())
        matched_weight = sum(weight for sym, weight in symptoms.items() if answers.get(key(sym), 0) == 1)
        confidence = (matched_weight / total_weight) * 100 if total_weight > 0 else 0
        results.append((disease, matched_weight, total_weight, confidence))


    #sort by confidence descending
    results.sort(key=lambda x: x[3], reverse = True)

    #display reasoning
    print("\n---Reasoning Trace---")
    for disease, matched, total, conf in results:
     bar = "█" * int(conf / 5) + "-" * (20 - int(conf / 5))
    print(f"{disease.ljust(15)}  | confindence: {conf:5.1f}%  | {bar}")



    #decision based on confience thresholds
    high_threshold = 70
    low_threshold = 40

    top_disease, _, _, top_conf = results[0]
    print("\n---Diagnosis Results[0]")



    if top_conf >= high_threshold:
     print(f"✅most likely diagnosis :  **{top_disease} ** (confidence: {top_conf: .1f}%)")
     print("→ High confidence based on your symptoms.")

    elif top_conf >= medium_threshold:
        print(f"⚠️ Possible diagnosis: **{top_disease}** (Confidence: {top_conf:.1f}%)")
        print("→ Medium confidence; further tests or observation advised.")
    else:
        print(f"❓ Low confidence in diagnosis (Top match: {top_disease}, {top_conf:.1f}%)")
        print("→ Insufficient data. Please provide more symptoms or consult a doctor.")

    # Explain reasoning for top disease
    print(f"\n--- Explanation for {top_disease} ---")
    print("rules:", list(rules[top_disease].keys()))
    print("Matched Symptoms:",
          [sym for sym in rules[top_disease] if answers.get(key(sym), 0) == 1])
    print("Unmatched Symptoms:",
          [sym for sym in rules[top_disease] if answers.get(key(sym), 0) == 0])

    return results


# --- DEMO RUN ---
sample_input = {
    "high fever": "y",
    "body ache": "y",
    "fatigue": "y",
    "dry cough": "y",
    "runny nose": "n",
    "itchy eyes": "n",
    "sore throat": "n",
    "loss of taste or smell": "n",
    "difficulty breathing": "n"
}

run_weighted_expert_system(sample_input)



