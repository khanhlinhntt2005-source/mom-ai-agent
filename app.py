from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "write a short facebook post about healthy lifestyle"}
    ]
)

print(response.choices[0].message.content)
