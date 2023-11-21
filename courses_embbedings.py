from dotenv import load_dotenv, find_dotenv
import json
import os
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np
import plotly.express as px

_ = load_dotenv('openAI.env')
openai.api_key  = os.environ['openAI_api_key']

with open('output_courses.json', 'r') as file:
    file_content = file.read()
    courses = json.loads(file_content)

#Vamos a crear una nueva llave con el embedding de la descripción de cada película en el archivo .json

for i in range(len(courses)):
  text = courses[i]['labels']['labels']
  text = ' '.join(text)
  emb = get_embedding(text,engine='text-embedding-ada-002')
  courses[i]['embedding'] = emb


#Vamos a almacenar esta información en un nuevo archivo .json
with open('courses_labels_embeddings.json', 'r') as file:
    file_content = file.read()
    courses = json.loads(file_content)