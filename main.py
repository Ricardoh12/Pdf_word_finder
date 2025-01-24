import os
import PySimpleGUI as sg
from PyPDF2 import PdfReader
import threading

word_counter = 0

# Função de procura path dos arquivos
def procurar_palavra_em_pdf(pdf_path, word, window):
    global word_counter

    try:
        reader = PdfReader(pdf_path)
        line = str(pdf_path)
        data = line.split("\\")
        file_name = data[-1]

        for page_num, page in enumerate(reader.pages):
            texto_pagina = page.extract_text().lower()

            if texto_pagina and word in texto_pagina:
                word_counter += 1
                resultado = f"Palavra '{word}' encontrada no arquivo '{file_name}' na página {page_num + 1}"
                window.write_event_value('-PROGRESS-', resultado)
    except Exception as e:
        window.write_event_value('-ERROR-', f"Erro ao processar o arquivo {pdf_path}: {e}")

# Função para processar os PDFS
def processar_pdfs(folder, word, window):
    pdf_files = [arquivo for arquivo in os.listdir(folder) if arquivo.endswith(".pdf")]
    
    if not pdf_files:
        sg.popup_error("Nenhum arquivo PDF encontrado no diretório!")
        return
    
    for i, arquivo in enumerate(pdf_files):
        caminho_pdf = os.path.join(folder, arquivo)
        threading.Thread(target=procurar_palavra_em_pdf, args=(caminho_pdf, word, window), daemon=True).start()
        window['-PROGRESSBAR-'].update((i + 1) * 100 // len(pdf_files))

# Layout da interface
layout = [
    [sg.Text("Caminho do diretório:"), sg.InputText(key="-DIR_PATH-"), sg.FolderBrowse()],
    [sg.Text("Palavra a procurar:"), sg.InputText(key="-WORD-")],
    [sg.Button("Procurar")],
    [sg.Output(size=(80, 20), key="-OUTPUT-")],
    [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESSBAR-')],
]

# Criar a janela
window = sg.Window('PDF FINDER', layout, icon='C:\\Users\\ricar\\Documents\\PyGui\\favicon.ico')


# Loop de eventos
while True:
    event, values = window.read(timeout=100)  
    
    if event == sg.WINDOW_CLOSED:
        break
    
    if event == "Procurar":
        folder = values.get("-DIR_PATH-")
        find_word = values.get("-WORD-", "").lower()  
        
        if not folder or not find_word:
            sg.popup_error("Preencha todos os campos!")
            continue
        
        word_counter = 0
        window['-OUTPUT-'].update("")  
        window['-PROGRESSBAR-'].update(0)
        
        
        processar_pdfs(folder, find_word, window)

        
        window['-OUTPUT-'].update(f"A palavra '{find_word}' foi encontrada em {word_counter} páginas.")


    if event == '-PROGRESS-':
        
        window['-OUTPUT-'].update(values[event] + '\n', append=True)

    if event == '-ERROR-':
        sg.popup_error(values[event])

window.close()
