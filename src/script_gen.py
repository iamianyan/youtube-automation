import anthropic
from src.config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_script(topic: str) -> str:
    print(f"Generating script for: {topic}")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""Write a faceless YouTube video script on this topic: "{topic}"

Structure it exactly like this:

[HOOK]
An attention-grabbing opening question or surprising stat. 2-3 sentences. No fluff.

[INTRO]
Tell the viewer exactly what they will learn. 2-3 sentences.

[SECTION: Section Title]
Main content. Write in short sentences, conversational tone. 60-90 seconds when read at 150 words per minute.

[SECTION: Section Title]
Repeat for 4-6 sections total.

[CTA]
Ask viewers to like and subscribe. Tell them what video to watch next. 2-3 sentences.

Rules:
- Write for voiceover — short sentences, no jargon, no bullet points
- No stage directions or camera notes
- Total script should be 700-900 words
- Use "you" to address the viewer directly
- Make it genuinely useful, not just filler"""
        }]
    )

    script = response.content[0].text
    print(f"Script generated ({len(script.split())} words)")
    return script


def extract_sections(script: str) -> list[dict]:
    sections = []
    current_tag = None
    current_lines = []

    for line in script.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            if current_tag and current_lines:
                sections.append({
                    "tag": current_tag,
                    "content": " ".join(current_lines)
                })
            current_tag = line[1:-1]
            current_lines = []
        else:
            current_lines.append(line)

    if current_tag and current_lines:
        sections.append({
            "tag": current_tag,
            "content": " ".join(current_lines)
        })

    return sections


def extract_keywords(script: str) -> list[str]:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""Extract 6 short visual search keywords from this script.
Each keyword should describe a scene or image that would work as background footage.
Return only the keywords, one per line, no numbering, no explanation.

Script:
{script[:1000]}"""
        }]
    )

    keywords = [
        line.strip()
        for line in response.content[0].text.splitlines()
        if line.strip()
    ]
    print(f"Keywords extracted: {keywords}")
    return keywords[:6]
