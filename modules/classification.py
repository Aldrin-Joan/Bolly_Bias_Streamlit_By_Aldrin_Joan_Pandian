from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
from config import MODEL_NAME, DEVICE

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    device_map="auto"
)
print("✅ Classification model loaded on:", model.device)

def classify_stereotype(line):
    prompt = f"""
You are a language model trained to detect gender stereotypes in lines from movie scripts.
   Your task is to classify each line into exactly one of the following 14 categories, based on the presence of stereotypical portrayals—especially of women.
   Assign only **one** label per line. Be careful to read subtle biases. Return only the **label** (not the line, not any explanation).
   Here are the 14 valid categories:
    1. occupation_gap → The character lacks a job, career mention, or professional identity.
      - Ex: "She stayed home while the others went to work."

    2. agency_gap → The character lacks independence or decision-making ability; is passive or submissive.
      - Ex: "She looked at him, waiting for his decision."

    3. appearance_focus → Emphasis on physical appearance, beauty, clothing, or body—but not sexual objectification.
      - Ex: "She walked in wearing a tight red dress that hugged every curve."

    4. relationship_only → Introduced only as a relation to another (wife, daughter, etc.).
      - Ex: "That's John's wife, the one sitting by the window."

    5. screen_time_disparity→ Line shows that women have very limited screen/dialog presence.
      - Ex: "The male characters dominated every major scene, while she had only two lines."

    6. dialogue_initiation_gap → The woman doesn't start conversations or only speaks when spoken to.
      - Ex: "She rarely spoke unless someone asked her a question first."

    7. emotional_typecast → The woman is only shown as overly emotional, irrational, or tearful.
      - Ex: "She burst into tears again, as usual."

    8. domesticity_emphasis → Emphasis on domestic roles (cooking, cleaning, homemaking).
      - Ex: "She was happiest baking cookies in her cozy kitchen."

    9. objectification → The body is sexualized visually or narratively. Often includes gaze, zoom-ins, or body parts.
      - Ex: "The camera panned slowly from her legs to her chest."

    10. victim_only → The woman appears only to suffer harm or be rescued, with no further agency.
      - Ex: "She screamed for help as the villain grabbed her."

    11. intelligence_undermined → The woman is portrayed as dumb, ditzy, or confused—especially in academic/intellectual areas.
      - Ex: "She looked confused by the math problem and giggled nervously."

    12. support_role_only → Exists only to encourage, cheer for, or help a man without her own arc.
      - Ex: "She cheered him on from the sidelines as he accepted his award."

    13. villainization → Woman is unfairly portrayed as evil, manipulative, or cruel (e.g. stepmother, seductress).
      - Ex: "The evil stepmother glared with contempt and plotted her revenge."

    14. none → The line is empowering or neutral. No stereotype or bias.
      - Ex: "She led the mission with confidence and precision."

    ---

    Read the line carefully. Choose the **most accurate single category** from the above list.
    If the line contains no bias, use `none`.

    Line: "{line}"
    Label:"""

    inputs = tokenizer(prompt.strip(), return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=10, pad_token_id=tokenizer.eos_token_id)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    label_matches = re.findall(r"Label:\s*(\w+)", decoded.lower())

    valid_labels = {
        "occupation_gap", "agency_gap", "appearance_focus", "relationship_only",
        "screen_time_disparity", "dialogue_initiation_gap", "emotional_typecast",
        "domesticity_emphasis", "objectification", "victim_only",
        "intelligence_undermined", "support_role_only", "villainization", "none"
    }

    return next((lbl for lbl in reversed(label_matches) if lbl in valid_labels), "none")
