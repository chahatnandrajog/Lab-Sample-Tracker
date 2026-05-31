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

Analyze the following sample and provide:

1. A short summary.
2. Any potential concerns.
3. Data quality observations.

Sample ID: {sample.sample_id}
Type: {sample.sample_type}
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