import os
from dotenv import load_dotenv,find_dotenv

# Find the .env file
dotenv_path = find_dotenv()
output = load_dotenv(dotenv_path, override=True)

import google.generativeai as genai
for m in genai.list_models():
#   if 'gecko' in m.name:
    print(m)    