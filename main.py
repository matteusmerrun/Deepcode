
from colorama import Fore, Style, init
import ollama

init(autoreset=True)

# Your banner goes here
DEEPCODE_BANNER = r"""
________                                        .___      
\______ \   ____   ____ ______   ____  ____   __| _/____  
 |    |  \_/ __ \_/ __ \\____ \_/ ___\/  _ \ / __ |/ __ \ 
 |    `   \  ___/\  ___/|  |_> >  \__(  <_> ) /_/ \  ___/ 
/_______  /\___  >\___  >   __/ \___  >____/\____ |\___  >
        \/     \/     \/|__|        \/           \/    \/ 
"""


prompt = input(Fore.CYAN + "\nDeepcode > ")

response = ollama.chat(
    model="deepseek-coder:6.7b",
    messages=[{"role": "user", "content": prompt}],
)

print(response["message"]["content"])
