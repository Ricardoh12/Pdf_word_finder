import os
from PyPDF2 import PdfReader
import json

file_name = 'data_files.json'
with open(file_name, 'r') as file:
    data = json.load(file)

path = data['entry_value']




def procurar_palavra_em_pdf(pdf_path, word):
    
    global word_counter
    word_counter = 0

    reader = PdfReader(pdf_path)
    line = str(pdf_path)
    data = line.split("\\")
    file_name = data[-1]

    for page_num, page in enumerate(reader.pages):
        texto_pagina = page.extract_text().lower()

       
        palavras = texto_pagina.split()
        
        if word in palavras:
            word_counter += 1
            print(f"Palavra encontrada no arquivo '{file_name}' na página {page_num + 1}")
        


folder = path

print(folder)

find_word = input("Palavra a procurar: ").lower()  

for arquivo in os.listdir(folder):
    if arquivo.endswith(".pdf"):
        caminho_pdf = os.path.join(folder, arquivo)
        procurar_palavra_em_pdf(caminho_pdf, find_word)
    

print(f"A palavra {find_word} foi encontrada em {word_counter} páginas")
