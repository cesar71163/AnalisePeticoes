import gradio as gr
import pdfplumber
import re

# Lista dos campos-título que queremos buscar
CAMPOS_CADIFA = [
    "NÚMERO E DATA DA ÚLTIMA RESOLUÇÃO DE CERTIFICAÇÃO",
    "NÚMERO DO EXPEDIENTE ou do PROCESSO",
    "IDENTIFICAÇÃO DA EMPRESA SOLICITANTE",
    "RESPONSÁVEL(IS) NO BRASIL PELO AGENDAMENTO DE INSPEÇÕES",
    "IDENTIFICAÇÃO DA EMPRESA ESTRANGEIRA A SER CERTIFICADA",
    "INSUMOS OBJETOS DA CERTIFICAÇÃO"
]

def extrair_por_linhas(pdf_file, linhas_pos_titulo):
    with pdfplumber.open(pdf_file.name) as pdf:
        texto = "\n".join(page.extract_text() or "" for page in pdf.pages)

    linhas = texto.split('\n')
    resultado = ""

    for campo in CAMPOS_CADIFA:
        for i, linha in enumerate(linhas):
            # Normaliza espaços e verifica se o campo aparece na linha
            if campo.lower() in linha.lower():
                trecho = linhas[i+1 : i+1+linhas_pos_titulo]
                conteudo = "\n".join(trecho).strip()
                resultado += f"{campo}:\n{conteudo}\n\n"
                break  # para evitar múltiplas ocorrências

    # Salva em .txt
    with open("resultado_extracao.txt", "w", encoding="utf-8") as f:
        f.write(resultado)

    return resultado, "resultado_extracao.txt"

# Interface Gradio com escolha do número de linhas
gr.Interface(
    fn=extrair_por_linhas,
    inputs=[
        gr.File(label="📤 Envie o PDF"),
        gr.Slider(label="📏 Número de linhas após o título", minimum=1, maximum=15, value=5, step=1),
    ],
    outputs=[
        gr.Text(label="📄 Conteúdo extraído"),
        gr.File(label="📥 Baixar resultado_extracao.txt"),
    ],
    title="🔍 Extrator CADIFA por Linhas",
    description="Escolha quantas linhas capturar após os campos CADIFA e salve o resultado em .txt.",
).launch()