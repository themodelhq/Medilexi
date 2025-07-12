# export_tinybert_to_onnx.py

from transformers import AutoTokenizer, AutoModel
import torch
import os

# 1. Model name from Hugging Face
model_name = "huawei-noah/TinyBERT_General_4L_312D"

# 2. Load the tokenizer and model
print("[INFO] Loading TinyBERT model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()

# 3. Dummy input for export
print("[INFO] Creating dummy input...")
dummy_text = "fever and chills"
inputs = tokenizer(dummy_text, return_tensors="pt")
dummy_inputs = (inputs["input_ids"], inputs["attention_mask"])

# 4. Export path
output_path = "tinybert.onnx"

# 5. Export to ONNX using opset_version=14
print(f"[INFO] Exporting to ONNX format at: {output_path}...")
torch.onnx.export(
    model,
    dummy_inputs,
    output_path,
    input_names=["input_ids", "attention_mask"],
    output_names=["last_hidden_state", "pooler_output"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence"},
        "attention_mask": {0: "batch_size", 1: "sequence"},
        "last_hidden_state": {0: "batch_size", 1: "sequence"},
        "pooler_output": {0: "batch_size"}
    },
    opset_version=14,  # ✅ Fix: using supported ONNX opset
    do_constant_folding=True
)

print(f"[✅ SUCCESS] tinybert.onnx saved at: {os.path.abspath(output_path)}")
