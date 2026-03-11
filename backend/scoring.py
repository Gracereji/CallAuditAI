from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY")

def analyze_transcript(transcript):

    prompt = f"""
Analyze this customer service call.

Return ONLY JSON in this format:

{{
"satisfaction_score": number,
"agent_efficiency": number,
"language_quality": number,
"time_efficiency": number,
"bias_reduction": number,
"customer_emotion": number,
"overall_quality": number,
"f1_score": number,
"summary": "text summary"
}}

Transcript:
{transcript}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content