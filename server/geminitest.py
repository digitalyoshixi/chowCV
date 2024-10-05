import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
geminikey = os.getenv("GEMINI")

genai.configure(api_key=geminikey)

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Respond in a line by-line format with answers only as integer values seperated by a space. The average price in CAD and expiry in days of: bread, beans, milk, ")
print(response.text)
#response = model.generate_content("Respond in only the answer as a single integer value. The average expiry in days of bread is:")
#print(int(response.text))