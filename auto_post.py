from openai import OpenAI
from googleapiclient.discovery import build
import pickle
import os
import urllib.parse

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
# GENERATE VIRAL TOPIC
# ---------------------------------

topic_prompt = """
Generate ONE viral South India news headline.

Requirements:
- Emotional
- Trending
- Click-worthy
- NDTV style
- Short and powerful
- Related to South India
- Make people curious to click
"""

print("Generating viral topic...")

topic_response = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": topic_prompt
        }
    ]
)

topic = topic_response.choices[0].message.content.strip()
topic = topic.replace('"', '')

print("Generated Topic:", topic)

# ---------------------------------
# GENERATE AI THUMBNAIL
# ---------------------------------

image_prompt = f"""
Breaking news style thumbnail for:
{topic}

Cinematic
Realistic
Indian news style
High quality
Emotional
Trending
"""

encoded_prompt = urllib.parse.quote(image_prompt)

image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

print("Generated Thumbnail:", image_url)

# ---------------------------------
# GENERATE NEWS ARTICLE
# ---------------------------------

prompt = f"""
Write a professional Indian news-style article about:

{topic}

Requirements:

- Use NDTV/news portal writing style
- Strong emotional opening
- Add breaking-news feeling
- Use short readable paragraphs
- Add subheadings
- SEO optimized
- Human conversational tone
- Include why this matters
- Add public reaction section
- Add conclusion
- 800 to 1200 words
- Mobile-friendly formatting
- Add FAQs at end

IMPORTANT:
Make article feel REAL and engaging.
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

article_content = response.choices[0].message.content

# ---------------------------------
# FORMAT ARTICLE CONTENT
# ---------------------------------

formatted_content = article_content.replace("\n", "<br><br>")

# ---------------------------------
# NDTV STYLE HTML FORMAT
# ---------------------------------

article = f"""
<div style="
max-width:780px;
margin:auto;
padding:25px;
font-family:Arial, sans-serif;
background:#ffffff;
color:#111111;
line-height:1.9;
font-size:20px;
">

<div style="
font-size:14px;
color:#cc0000;
font-weight:bold;
margin-bottom:15px;
text-transform:uppercase;
">
BREAKING NEWS
</div>

<h1 style="
font-size:42px;
line-height:1.3;
margin-bottom:25px;
font-weight:700;
color:#000000;
">
{topic}
</h1>

<div style="
font-size:15px;
color:#666666;
margin-bottom:30px;
border-bottom:1px solid #e5e5e5;
padding-bottom:15px;
">
Published by SouthSync • Auto AI News System
</div>

<img
src="{image_url}"
style="
width:100%;
border-radius:12px;
margin-bottom:25px;
"
>

<div style="
font-size:20px;
line-height:2;
color:#222222;
">
{formatted_content}
</div>

<hr style="
margin-top:40px;
margin-bottom:20px;
border:none;
border-top:1px solid #dddddd;
">

<div style="
font-size:14px;
color:#888888;
text-align:center;
">
SouthSync AI News • South India Trending Updates
</div>

</div>
"""

# ---------------------------------
# BLOGGER POST
# ---------------------------------

post = {
    "title": topic,
    "content": article,
    "labels": [
        "South India",
        "Trending News",
        "Technology",
        "Breaking News"
    ]
}

print("Publishing to Blogger...")

result = service.posts().insert(
    blogId=BLOG_ID,
    body=post,
    isDraft=False
).execute()

# ---------------------------------
# SUCCESS MESSAGE
# ---------------------------------

print("POST SUCCESSFULLY PUBLISHED!")
print(result["url"])