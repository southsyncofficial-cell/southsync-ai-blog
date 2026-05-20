from openai import OpenAI
from googleapiclient.discovery import build
import pickle
import os
on
# ---------------------------------
# OPENROUTER API
# ---------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# ---------------------------------
# BLOGGER AUTH
# ---------------------------------

with open("token.pkl", "rb") as token:
    creds = pickle.load(token)

service = build("blogger", "v3", credentials=creds)

BLOG_ID = "9088517857362996956"

# ---------------------------------
# TOPIC
# ---------------------------------

topic = "Top Trending Technology News in South India Today"

# ---------------------------------
# AI ARTICLE
# ---------------------------------

prompt = f"""
Write a detailed SEO optimized blog article about:

{topic}

Requirements:
- 1000+ words
- SEO optimized
- Headings
- FAQs
- Human tone
- Beginner friendly
"""

print("Generating article...")

response = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

article = response.choices[0].message.content

# ---------------------------------
# BLOGGER POST
# ---------------------------------

post = {
    "title": topic,
    "content": article
}

result = service.posts().insert(
    blogId=BLOG_ID,
    body=post,
    isDraft=False
).execute()

print("POST SUCCESSFULLY PUBLISHED!")
print(result["url"])