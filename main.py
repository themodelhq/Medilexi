import tkinter as tk
from tkinter import messagebox
import json
import pyttsx3
import os
import sys

# Detect runtime path (PyInstaller fix)
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Load symptoms.json
with open(resource_path("data/symptoms.json"), "r", encoding="utf-8") as f:
    symptoms = json.load(f)

# Load and normalize drugs.json keys to lowercase
with open(resource_path("data/drugs.json"), "r", encoding="utf-8") as f:
    original_drugs = json.load(f)
    drugs = {k.strip().lower(): v for k, v in original_drugs.items()}

# Fix: Use a fresh pyttsx3 engine every time to avoid voice lock-up
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Speech error: {e}")

# Core logic
def check_symptoms():
    symptom = symptom_entry.get().strip().lower()
    if symptom in symptoms:
        conditions = symptoms[symptom]
        result = "\n".join(conditions)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result)
        speak(result)
    else:
        messagebox.showwarning("Not Found", "Symptom not found.")

def lookup_drug():
    drug = drug_entry.get().strip().lower()
    if drug in drugs:
        data = drugs[drug]
        result = f"Dosage: {data.get('dosage', {}).get('adult', 'N/A')}\n"
        result += f"Indications: {', '.join(data.get('indications', []))}\n"
        result += f"Interactions: {', '.join(data.get('interactions', []))}\n"
        result += f"Contraindications: {', '.join(data.get('contraindications', []))}\n"
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result)
        speak(result)
    else:
        messagebox.showwarning("Not Found", f"Drug '{drug}' not found.")

# GUI setup
root = tk.Tk()
root.title("MediLexi - Offline Symptom & Drug Checker")
root.geometry("500x500")
root.configure(bg="black")

title = tk.Label(root, text="MediLexi", font=("Helvetica", 20), bg="black", fg="white")
title.pack(pady=10)

symptom_label = tk.Label(root, text="Enter Symptom:", bg="black", fg="white")
symptom_label.pack()
symptom_entry = tk.Entry(root, width=40)
symptom_entry.pack()

symptom_btn = tk.Button(root, text="Check Symptom", command=check_symptoms)
symptom_btn.pack(pady=5)

drug_label = tk.Label(root, text="Enter Drug Name:", bg="black", fg="white")
drug_label.pack()
drug_entry = tk.Entry(root, width=40)
drug_entry.pack()

drug_btn = tk.Button(root, text="Lookup Drug", command=lookup_drug)
drug_btn.pack(pady=5)

result_text = tk.Text(root, height=10, bg="#111", fg="white", wrap="word")
result_text.pack(pady=10)

root.mainloop()
