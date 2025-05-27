
import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def safe_parse_json(content):
    """Safely parse JSON returned by GPT."""
    try:
        return json.loads(content)
    except Exception as e:
        raise ValueError(f"❌ Failed to parse JSON: {e}\nGPT Output:\n{content}")

def call_gpt(system_prompt, user_prompt, temperature=0):
    """Generic GPT-4 wrapper."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()

def chatbot_response(query, demand_df, processing_df, transportation_df):
    """Descriptive query handler: answers strictly from data."""

    demand_data = demand_df.to_string(index=False)
    processing_data = processing_df.to_string(index=False)
    transportation_data = transportation_df.to_string(index=False)

    system_prompt = f"""
You are a highly accurate supply chain chatbot. You MUST base your answer strictly on the provided datasets below.

🔹 **Demands Dataset** — required amount of light/dark roast for each café.
🔹 **Processing Dataset** — suppliers, roasteries, capacity, and cost.
🔹 **Transportation Dataset** — routes, costs, and capacities.

### Rules:
- Do NOT guess.
- Do NOT invent numbers.
- Do NOT answer from general knowledge.
- If you cannot determine an answer from the dataset, say: 
  👉 "I could not determine the correct answer from the dataset."

---

#### Demands Dataset:
{demand_data}

#### Processing Dataset:
{processing_data}

#### Transportation Dataset:
{transportation_data}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    return response["choices"][0]["message"]["content"].strip()
