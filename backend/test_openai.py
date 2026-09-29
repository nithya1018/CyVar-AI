import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env")
    raise SystemExit

print("✅ API key found")

client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-5.6-luna",
        input="Reply with exactly: CyVar AI connected successfully"
    )

    print("AI Response:")
    print(response.output_text)

except Exception as error:
    print("❌ OpenAI connection failed")
    print(error)