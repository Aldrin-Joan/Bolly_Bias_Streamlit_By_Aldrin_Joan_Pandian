from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from config import MODEL_NAME, DEVICE

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    device_map="auto"
)
print("✅ Rewriting model loaded on:", model.device)

def rewrite_line(line, stereotype_type):
    prompt = f"""
You are a helpful assistant trained to rewrite movie script lines that reinforce gender stereotypes.

For the detected stereotype below, refer to the definitions and examples before rewriting the line. Your rewrite should **remove the biased framing** while preserving the character’s agency, purpose, and the narrative meaning.

Stereotype Detected: {stereotype_type}

Definitions and Examples:

1. occupation_gap → The character lacks a job, career mention, or professional identity.
   - Biased: "She stayed home while the others went to work."
   - Rewrite: "She pursued her passion in interior design while balancing life at home."

2. agency_gap → The character lacks independence or decision-making ability; is passive or submissive.
   - Biased: "She looked at him, waiting for his decision."
   - Rewrite: "She stepped forward and made the final call herself."

3. appearance_focus → Emphasis on beauty or physical appearance without deeper identity.
   - Biased: "She wore a tight red dress that hugged every curve."
   - Rewrite: "She arrived with confidence, her presence commanding the room."

4. relationship_only → Introduced only as wife, daughter, etc., not as an individual.
   - Biased: "That's John's wife, the one sitting by the window."
   - Rewrite: "That's Dr. Ananya Verma, a celebrated surgeon."

5. screen_time_disparity → Women have very limited dialogue or visibility.
   - Biased: "The male characters dominated every scene; she had only two lines."
   - Rewrite: "She led the negotiation scene, pushing the story forward."

6. dialogue_initiation_gap → Woman doesn't start conversations, only responds.
   - Biased: "She rarely spoke unless someone asked her something."
   - Rewrite: "She opened the discussion by challenging the team's assumptions."

7. emotional_typecast → Overly emotional, irrational, or tearful.
   - Biased: "She burst into tears again, as usual."
   - Rewrite: "She held back tears, choosing to speak with calm clarity."

8. domesticity_emphasis → Focus on cooking, cleaning, homemaking roles.
   - Biased: "She was happiest baking cookies in her cozy kitchen."
   - Rewrite: "She found balance between managing her bakery and leading community events."

9. objectification → Sexualized body focus, gaze, or parts.
   - Biased: "The camera panned slowly from her legs to her chest."
   - Rewrite: "The camera followed her confident stride as she entered the courtroom."

10. victim_only → Only suffers or is rescued, with no agency.
   - Biased: "She screamed for help as the villain grabbed her."
   - Rewrite: "She fought back fiercely, buying time for others to escape."

11. intelligence_undermined → Shown as ditzy, confused, or dumb.
   - Biased: "She looked confused by the math problem and giggled."
   - Rewrite: "She solved the equation quickly, surprising her peers."

12. support_role_only → Exists only to help a male character shine.
   - Biased: "She cheered him on from the sidelines as he accepted his award."
   - Rewrite: "They stood side by side, accepting the award for their joint success."

13. villainization → Portrayed unfairly as cruel, seductive, or evil.
   - Biased: "The evil stepmother glared and plotted her revenge."
   - Rewrite: "She struggled with being misunderstood, trying to reconnect with the children."

14. none → No stereotype. Line is neutral or empowering.
   - Example: "She led the mission with confidence and precision."

Now rewrite the following line accordingly:

Original Line: "{line}"
Rewritten Line:"""

    inputs = tokenizer(prompt.strip(), return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=60, pad_token_id=tokenizer.eos_token_id)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    return decoded.split("Rewritten Line:")[-1].strip().strip('"')
