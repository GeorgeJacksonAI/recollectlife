# 🎙️ Life Story Game – Chatbot (AI Interviewer) Flow  
**Product Specification – Version 1.0**

## 🎯 Purpose
Enable subscribed users to easily and emotionally engage with their life story through a conversational AI experience, resulting in a structured narrative that can be automatically transformed into a personalized board game.

This path is ideal for users who:
- Feel they “don’t have a story”
- Prefer talking over writing
- Are unsure where to begin

---

## 🔄 User Journey Overview

1. **User logs in** (subscription verified)  
2. **Selects “AI Interviewer”** from story-start options  
3. **Engages in a guided chat** with an AI persona  
4. **Reviews & refines** AI-suggested story name and chapters  
5. **Edits or expands** chapters in a simple editor  
6. **Generates game assets** (cards, board, PDF)  

---

## 💬 AI Interviewer Experience

### Personality & Tone
- **Warm, curious, and compassionate**  
- Feels like a wise friend or documentary interviewer  
- Never judgmental; always encouraging  
- Uses open-ended, reflective questions

### Conversation Flow (Approx. 5–7 Questions)

| Step | AI Prompt (Example) | Purpose |
|------|---------------------|--------|
| 1 | “What’s a story from your life that you hope never gets forgotten?” | Elicit core motivation |
| 2 | “Who would you most want to hear this story—and why?” | Identify audience & emotional stakes |
| 3 | “Was there a moment when everything changed for you?” | Find turning points |
| 4 | “What’s something you’ve never told anyone—but might want to share through this game?” | Unlock vulnerable, meaningful content |
| 5 | “If your life had a theme song or motto, what would it be?” | Capture tone & spirit |
| 6 *(optional)* | “Let’s go deeper: tell me more about [moment they mentioned].” | Expand key scenes |

> 💡 The AI **remembers** prior answers and **builds context** (e.g., if user mentions “raising kids alone,” later questions explore resilience, support, joy).

---

## 🧠 AI Backend Logic

### What Happens Behind the Scenes
1. User message is sent to your backend server.
2. Your server formats a **system prompt** like this:

```text
You are a compassionate life story coach helping someone create a meaningful board game for their loved ones.
Ask gentle, open-ended questions that uncover emotional truth, pivotal moments, and legacy.
After 5–7 thoughtful exchanges, summarize their story with:
- A poetic but clear TITLE (max 5 words)
- A 1-sentence REASON why they’re telling it
- 3–5 CHAPTER TITLES that form a narrative arc

Keep responses concise (1–2 sentences max during interview).