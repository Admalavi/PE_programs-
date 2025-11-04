# 🩺 Expert System: Disease Diagnosis with Weighted Symptoms and Confidence Scores
# 💻 Developed by: Akshata Malavi

import tkinter as tk
from tkinter import ttk, messagebox

# --- Weighted rule base ---
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


# --- Diagnosis Logic ---
def diagnose():
    answers = {sym.lower(): var.get() for sym, var in symptom_vars.items()}
    results = []

    for disease, symptoms in rules.items():
        total_weight = sum(symptoms.values())
        matched_weight = sum(weight for sym, weight in symptoms.items() if answers.get(sym.lower(), 0) == 1)
        confidence = (matched_weight / total_weight) * 100 if total_weight > 0 else 0
        results.append((disease, matched_weight, total_weight, confidence))

    results.sort(key=lambda x: x[3], reverse=True)
    display_results(results, answers)


def display_results(results, answers):
    for widget in result_frame.winfo_children():
        widget.destroy()

    ttk.Label(result_frame, text="--- Diagnosis Results ---", font=("Helvetica", 14, "bold")).pack(pady=5)

    for disease, matched, total, conf in results:
        bar_frame = ttk.Frame(result_frame)
        bar_frame.pack(fill="x", padx=10, pady=3)

        label = ttk.Label(bar_frame, text=f"{disease:15} ({conf:.1f}%)")
        label.pack(side="left")

        progress = ttk.Progressbar(bar_frame, length=200, value=conf, maximum=100)
        progress.pack(side="left", padx=5)

    # Top result
    top_disease, _, _, top_conf = results[0]
    high_threshold = 70
    medium_threshold = 40

    ttk.Separator(result_frame, orient="horizontal").pack(fill="x", pady=8)
    ttk.Label(result_frame, text="--- Diagnosis Summary ---", font=("Helvetica", 12, "bold")).pack()

    if top_conf >= high_threshold:
        msg = f"✅ Most likely: {top_disease} ({top_conf:.1f}%)"
    elif top_conf >= medium_threshold:
        msg = f"⚠️ Possible: {top_disease} ({top_conf:.1f}%)"
    else:
        msg = f"❓ Low confidence ({top_conf:.1f}%). Consult a doctor."

    ttk.Label(result_frame, text=msg, foreground="blue", font=("Helvetica", 11)).pack(pady=3)

    # Explanation
    ttk.Label(result_frame, text=f"\n--- Explanation for {top_disease} ---", font=("Helvetica", 12, "bold")).pack()
    matched = [sym for sym in rules[top_disease] if answers.get(sym.lower(), 0) == 1]
    unmatched = [sym for sym in rules[top_disease] if answers.get(sym.lower(), 0) == 0]

    ttk.Label(result_frame, text=f"Matched Symptoms: {', '.join(matched) or 'None'}").pack()
    ttk.Label(result_frame, text=f"Unmatched Symptoms: {', '.join(unmatched) or 'None'}").pack()


# --- GUI Setup ---
root = tk.Tk()
root.title("🩺 Disease Diagnosis Expert System")
root.geometry("700x650")
root.config(bg="#E9F6FF")

title = ttk.Label(root, text="Disease Diagnosis Expert System", font=("Helvetica", 18, "bold"))
title.pack(pady=10)

frame = ttk.LabelFrame(root, text="Select Your Symptoms", padding=10)
frame.pack(padx=10, pady=10, fill="both", expand=True)

canvas = tk.Canvas(frame)
scroll_y = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

symptom_vars = {}
for symptom in all_symptoms:
    var = tk.IntVar()
    chk = ttk.Checkbutton(scrollable_frame, text=symptom.capitalize(), variable=var)
    chk.pack(anchor="w", padx=10, pady=2)
    symptom_vars[symptom] = var

ttk.Button(root, text="🔍 Diagnose", command=diagnose).pack(pady=10)

result_frame = ttk.LabelFrame(root, text="Results", padding=10)
result_frame.pack(padx=10, pady=10, fill="both", expand=True)

footer = ttk.Label(root, text="Take care", font=("Helvetica", 10, "italic"), foreground="gray")
footer.pack(pady=5)

root.mainloop()
