# ui/gui.py

import tkinter as tk
from tkinter import messagebox, scrolledtext
from core.symptom_checker import get_possible_conditions
from core.drug_lookup import lookup_drug
from core.voice_output import speak

class MediLexiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MediLexi - Offline AI Assistant")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="🩺 MediLexi – AI Symptom & Drug Checker", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack(pady=5)

        self.symptom_btn = tk.Button(self.mode_frame, text="Check Symptoms", command=self.check_symptoms)
        self.symptom_btn.grid(row=0, column=0, padx=10)

        self.drug_btn = tk.Button(self.mode_frame, text="Look up Drug", command=self.lookup_drug)
        self.drug_btn.grid(row=0, column=1, padx=10)

        self.input_label = tk.Label(self.root, text="Enter text below:")
        self.input_label.pack()

        self.text_input = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=5)
        self.text_input.pack(pady=5)

        self.submit_btn = tk.Button(self.root, text="Submit", command=self.process_input)
        self.submit_btn.pack(pady=5)

        self.output_label = tk.Label(self.root, text="Results:")
        self.output_label.pack()

        self.output_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=10, state='disabled')
        self.output_box.pack(pady=5)

        self.mode = None

    def check_symptoms(self):
        self.mode = "symptom"
        self.clear_text()
        self.text_input.insert(tk.END, "e.g., fever, headache, cough")

    def lookup_drug(self):
        self.mode = "drug"
        self.clear_text()
        self.text_input.insert(tk.END, "e.g., Amoxicillin, Paracetamol")

    def process_input(self):
        query = self.text_input.get("1.0", tk.END).strip()
        self.output_box.config(state='normal')
        self.output_box.delete("1.0", tk.END)

        if not query:
            messagebox.showwarning("Input Required", "Please enter symptoms or a drug name.")
            return

        if self.mode == "symptom":
            results = get_possible_conditions(query)
            output_text = "\n".join(f"• {r}" for r in results)
            speak_text = "The possible conditions are: " + ", ".join(results)
            speak(speak_text)

        elif self.mode == "drug":
            result = lookup_drug(query)
            if "error" in result:
                output_text = f"❌ {result['error']}"
                speak(result["error"])
            else:
                output_text = f"""💊 Drug Info:

Adult Dosage: {result['dosage']['adult']}
Child Dosage: {result['dosage']['child']}
Indications: {", ".join(result['indications'])}
Interactions: {", ".join(result['interactions'])}
Contraindications: {", ".join(result['contraindications'])}
"""
                voice_text = result.get("language_text", {}).get("en", "")
                if voice_text:
                    speak(voice_text)

        else:
            output_text = "❗ Please select a mode first (Symptom or Drug Lookup)."

        self.output_box.insert(tk.END, output_text)
        self.output_box.config(state='disabled')

    def clear_text(self):
        self.text_input.delete("1.0", tk.END)
        self.output_box.config(state='normal')
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = MediLexiApp(root)
    root.mainloop()
