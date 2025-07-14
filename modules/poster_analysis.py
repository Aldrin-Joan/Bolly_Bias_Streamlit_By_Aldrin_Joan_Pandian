# modules/poster_analysis.py

import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.units import inch
import tempfile
from io import BytesIO

# 📦 Load model + processor once
model_id = "llava-hf/llava-1.5-7b-hf"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForVision2Seq.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)
device = model.device

# 🔍 Inference function
def detect_poster_bias(image: Image.Image) -> str:
    prompt = (
        "<|user|>\n<image>\n"
        "Analyze the movie poster for signs of gender bias. "
        "Classify the bias into one of these **exact** categories (respond using the text label only):\n"
        "- occupation_gap\n"
        "- agency_gap\n"
        "- appearance_focus\n"
        "- relationship_only\n"
        "- screen_time_disparity\n"
        "- dialogue_initiation_gap\n"
        "- emotional_typecast\n"
        "- domesticity_emphasis\n"
        "- objectification\n"
        "- victim_only\n"
        "- intelligence_undermined\n"
        "- support_role_only\n"
        "- villainization\n"
        "- none\n\n"
        "Respond strictly in this format:\n"
        "Bias Category: <one category from above>\n"
        "Severity: <low / medium / high>\n"
        "Suggested Tweak: <specific change to reduce bias>\n"
        "<|assistant|>\n"
    )

    inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=200)
    decoded = processor.batch_decode(output, skip_special_tokens=True)[0].strip()
    if "<|assistant|>" in decoded:
        decoded = decoded.split("<|assistant|>")[-1].strip()
    return decoded

# 🧾 PDF Generator (returns in-memory PDF)
def generate_poster_pdf(result_text: str, image: Image.Image) -> BytesIO:
    lines = result_text.splitlines()
    bias_category = lines[0].split(":", 1)[1].strip() if len(lines) > 0 else "N/A"
    severity = lines[1].split(":", 1)[1].strip() if len(lines) > 1 else "N/A"
    tweak = lines[2].split(":", 1)[1].strip() if len(lines) > 2 else "N/A"

    # Save image to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img_file:
        image.save(temp_img_file.name)
        img_path = temp_img_file.name

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(RLImage(img_path, width=4.5 * inch, height=6 * inch))
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("🎬 <b>Poster Bias Detection Report</b>", styles["Title"]))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(f"<b>Bias Category:</b> {bias_category}", styles["Normal"]))
        story.append(Paragraph(f"<b>Severity:</b> {severity}", styles["Normal"]))
        story.append(Paragraph(f"<b>Suggested Tweak:</b> {tweak}", styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("<i>This report was generated using LLaVA-1.5</i>", styles["Normal"]))

        doc.build(story)

    return buffer
