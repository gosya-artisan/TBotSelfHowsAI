import requests
from openai import OpenAI
import os
import re
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from collections import Counter 

last_message = "" 
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Send name here!!!')

#API = "https://api.github.com"

#def gh(path: str, params=None):
    #r = requests.get(
    #    API + path,
    #    params=params,
    #    headers={"Accept": "application/vnd.github+json", "User-Agent":"recap-bot"},
    #    timeout=20,
    #)
    #if r.status_code == 404:
    #    return None
    #if r.status_code == 403:
    #    raise RuntimeError("GitHub rate limit(403). Try later or add a tocen")
    #.raise_for_status()
    #return r.json()

#def build_prompt(username: str)-> str:
    #user = gh(f"/users/{username}") 
    #if not user:
    #    return ""

    #repos = gh(f"/users/{username}/repos", params={"per_page": 100, "sort": "updated"}) or []

    #langs = Counter()
    #for r in repos:
    #    if r.get("language"):
    #        langs[r["language"]] +=1
    
    #top_langs = ", ".join([f"{l} ({c})" for l,c in langs.most_common(5) or "unknown"]) 
    #if langs:
    #    top_langs = ", ".join([f"{l} ({c})" for l, c in langs.most_common(5)])
    #else:
    #    top_langs = "unknown"
    #return("prompt")

#llm activation command:
#env __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia vllm serve Qwen/Qwen3-0.6B \--host 127.0.0.1 --port 8000 \--dtype float16 \--gpu-memory-utilization 0.85 \--max-model-len 2048

def build_prompt():
    return last_message

def ask_llm(text: str) -> str:
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key = "yoass",
    )
    resp = client.chat.completions.create(
        model = "Qwen/Qwen3-0.6B",
        messages = [{"role": "user", "content": text}],
        max_tokens = 800,
        temperature =0.7,
    )

    return resp.choices[0].message.content

def recap():#(username: str) -> str:
    prompt = build_prompt()#username
    print(prompt)
    if not prompt:
        return "Something went wrong"
    return ask_llm(prompt)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #username = (update.message.text or " ").strip()
    #if not username:
    #    return
    
    #await update.message.reply_text("Working...")

    global last_message
    last_message = (update.message.text or "").strip()
    try: 
        out = await asyncio.to_thread(recap)#username
        print(out)
        await update.message.reply_text(re.sub(r'<think>.*?</think>', '', out, flags=re.DOTALL | re.IGNORECASE))
    except Exception as e:
        await update.message.reply_text(f"Error {e}")
    #await update.message.reply_text(out)

def main():
    app = ApplicationBuilder().token("8509234367:AAFvQAU84ltcUkmqzVr9zp5x3CYB8AkqYq4").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
