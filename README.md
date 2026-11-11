
# Deepcode

---

Deepcode is a deepseek plugin to use to vibe code in your own terminal with the deepseek model of your choice locally. Its very close to some very famous applications like claude code or qwen code but this is completley human written with no ai whatsoever, and im not planning to have AI work on this project and it is not a moddification of any kind. 

## Installation

It works on evrey opperatting system beacouse it is an aplication that you connect with ollama so ollama supports evrey OS us to in the future right now its macOS and linux only. Ensure that you have Node js installed if not you can install it at: [Node-js](https://nodejs.org) Install (v18+) but there is an option which i personally use which is: [Python](https://python.org).

### 1. Then clone the github repo with this following command:
```bash
git clone https://github.com/matteusmerrun/Deepcode.git 
cd deepcode
```
Now what this does is that it installs my project from github and it uses the terminal to open the folder in the terminal thats what c


### 2. Then Install some programs needed to run the terminal application:
```bash
pip install -r requirements.txt
```
This installs some librarys you need to run the project like when i built it i used import requests and import ollama and import rich and import collorama you do not need to type that whats just what i used to build this.

### 3. Install ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 4. Set up your local deepseek model:
```bash
curl -fsSL https://ollama.com/install.sh | sh && ollama pull deepseek-coder:6.7b && ollama run deepseek-coder:6.7b
```
This installs and runs deepseek-coder:6.7b.

## Setting it up & and running it

 ### Running the Application

Open your terminal or command prompt and run the single command for your operating system:
* **MacOS:**
  just double click the deepseek.command in finder
   
* **Linux:**
  ```bash
  cd deepseek && python3 main.py
  ```

* **Windows:**
  ```cmd
  cd deepseek && python main.py
  ```
  
## Licence

Copyright (c) 2026 Matteus Merrun. All Rights Reserved.

Deepcode is proprietary software.

Permission is granted to view and inspect the source code for personal, educational, and evaluation purposes, including portfolio and résumé review.

Without prior written permission from the copyright holder, no person may:
- Copy or redistribute this software.
- Modify or create derivative works.
- Use this software commercially.
- Publish or distribute modified versions.
- Claim ownership of any part of this project.

All rights not expressly granted are reserved by the copyright holder.

For permissions beyond those explicitly granted above, contact the copyright holder. 
