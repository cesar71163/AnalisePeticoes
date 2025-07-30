import gradio as gr
import pdfplumber

# Campos PT e EN (sem regex, pois faremos busca direta por linha)
CAMPOS_MULTILINGUE = {
    "pt": {
        "NÚMERO E DATA DA ÚLTIMA RESOLUÇÃO DE CERTIFICAÇÃO": "NUMBER AND DATE OF LAST CERTIFICATION RESOLUTION",
        "NÚMERO DO EXPEDIENTE ou do PROCESSO": "PROCESS OR CASE NUMBER",
        "IDENTIFICAÇÃO DA EMPRESA SOLICITANTE": "IDENTIFICATION OF THE APPLICANT COMPANY",
        "RESPONSÁVEL(IS) NO BRASIL PELO AGENDAMENTO DE INSPEÇÕES": "PERSON RESPONSIBLE IN BRAZIL FOR SCHEDULING INSPECTIONS",
        "IDENTIFICAÇÃO DA EMPRESA ESTRANGEIRA A SER CERTIFICADA": "IDENTIFICATION OF THE FOREIGN COMPANY TO BE CERTIFIED",
        "INSUMOS OBJETOS DA CERTIFICAÇÃO": "INPUTS SUBJECT TO CERTIFICATION"
    },
    "en": {
        "NUMBER AND DATE OF LAST CERTIFICATION RESOLUTION": "NÚMERO E DATA DA ÚLTIMA RESOLUÇÃO DE CERTIFICAÇÃO",
        "PROCESS OR CASE NUMBER": "NÚMERO DO EXPEDIENTE ou do PROCESSO",
        "IDENTIFICATION OF THE APPLICANT COMPANY": "IDENTIFICAÇÃO DA EMPRESA SOLICITANTE",
        "PERSON RESPONSIBLE IN BRAZIL FOR SCHEDULING INSPECTIONS": "RESPONSÁVEL(IS) NO BRASIL PELO AGENDAMENTO DE INSPEÇÕES",
        "IDENTIFICATION OF THE FOREIGN COMPANY TO BE CERTIFIED": "IDENTIFICAÇÃO DA EMPRESA ESTRANGEIRA A SER CERTIFICADA",
        "INPUTS SUBJECT TO CERTIFICATION": "INSUMOS OBJETOS DA CERTIFICAÇÃO"
    }
}

def extrair_multilingue_por_linhas(pdf_file, idioma, linhas_pos_titulo):
    if idioma not in CAMPOS_MULTILINGUE:
        return "Idioma não suportado.", None

    campos = CAMPOS_MULTILINGUE[idioma]
    with pdfplumber.open(pdf_file.name) as pdf:
        texto = "\n".join(page.extract_text() or "" for page in pdf.pages)

    linhas = texto.split('\n')
    resultado = ""

    for campo, campo_traduzido in campos.items():
        for i, linha in enumerate(linhas):
            if campo.lower() in linha.lower() or campo_traduzido.lower() in linha.lower():
                trecho = linhas[i+1 : i+1+linhas_pos_titulo]
                conteudo = "\n".join(trecho).strip()
                resultado += f"{campo} / {campo_traduzido}:\n{conteudo}\n\n"
                break
        else:
            resultado += f"{campo} / {campo_traduzido}:\n⚠️ Campo não encontrado\n\n"

    with open("resultado_extracao_multilingue.txt", "w", encoding="utf-8") as f:
        f.write(resultado)

    return resultado, "resultado_extracao_multilingue.txt"

# Interface Gradio com controle de idioma e número de linhas
gr.Interface(
    fn=extrair_multilingue_por_linhas,
    inputs=[
        gr.File(label="📤 Envie o PDF"),
        gr.Dropdown(label="🌐 Idioma do documento", choices=["pt", "en"], value="pt"),
        gr.Slider(label="📏 Número de linhas após o título", minimum=1, maximum=15, value=5, step=1)
    ],
    outputs=[
        gr.Text(label="📄 Resultado extraído"),
        gr.File(label="📥 Baixar resultado_extracao_multilingue.txt")
    ],
    title="🌐 Extrator CADIFA Multilíngue por Linhas",
    description="Detecta campos em português ou inglês e extrai linhas subsequentes conforme sua escolha.",
).launch()