# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TOKEN:
    raise ValueError("[ERROR] TELEGRAM_TOKEN not found in environment variables. Please check your .env file.")

if ':' not in TOKEN or len(TOKEN) < 20:
    raise ValueError("[ERROR] TELEGRAM_TOKEN has invalid format. Please check your token.")

print(f"[OK] Token loaded: {TOKEN[:10]}...", flush=True)

