import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_sample_summary(sample):

    prompt = f"""
You are a laboratory workflow assistant.

Review this lab sample and provide:

1. Summary
2. Data Validation Review
3. Potential Risks
4. Recommended Next Step

Keep the response under 150 words.

Consider these validation rules:
- Temperature should be between -200 and 100.
- Required fields should not be missing.
- Storage and status should make sense for the sample.

Sample ID: {sample.sample_id}
Type: {sample.sample_type}
Collection Date: {sample.collection_date}
Status: {sample.status}
Storage Location: {sample.storage_location}
Owner: {sample.owner}
Temperature: {sample.temperature}
Notes: {sample.notes}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content