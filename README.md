## Commands

### Windows CMD command

'''
#create folder for the project
mkdir <project_folder_name>
'''

''' 
#change directory to the project folder
cd  <project_folder_name>
'''

'''
#opens folder in VS code, ensure VS code is installation prior
cd .  
'''

### VS Code CMD environment setup

'''
#create environment of the conda environment
conda create -p <environment name> python=3.10 -y
'''

'''
#activate path of the conda environment
Conda activate <path of environment>

'''

'''
#Clone the git repository
git clone https://github.com/nandhakumarmurugesan/document_portal_project.git
'''

## Requirement of the project
1. LLM Model
Groq (free)
huggingface(free)
ollama(local setup)
gemini(free-limited time)
openai (paid)

2. Embedding Model
open ai
hugging face
gemini

3.Vectordatabase
inmemory
ondisk
cloudbased


#groq API KEY GENERATION
https://console.groq.com/keys
#more on models links -> https://console.groq.com/playground

#Google API KEYS
https://aistudio.google.com/api-keys
#more on models links -> https://ai.google.dev/gemini-api/docs/embeddings