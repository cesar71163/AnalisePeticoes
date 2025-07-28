import gradio as gr
import pdfplumber
import spacy

# Carrega o modelo de NLP
nlp = spacy.load("pt_core_news_md")


def processar_pdf(pdf_file, pergunta):
    # Extrai texto
    with pdfplumber.open(pdf_file.name) as pdf:
        texto = "\n".join(page.extract_text() or "" for page in pdf.pages)

    # NLP no texto
    doc = nlp(texto)

    # Simples mecanismo de busca: verifica se a pergunta tem uma entidade
    respostas = []
    for ent in doc.ents:
        if pergunta.lower() in ent.text.lower():
            respostas.append(f"{ent.text} -> {ent.label_}")

    if respostas:
        return "\n".join(respostas)
    else:
        return "Desculpe, não encontrei informações relacionadas à sua pergunta."


# Interface Gradio
gr.Interface(
    fn=processar_pdf,
    inputs=[
        gr.File(label="Envie seu PDF "),
        gr.Textbox(label="Pergunte algo sobre o documento"),
    ],
    outputs="text",
    title="Chatbot Leitor de PDF",
    description="Interaja com documentos PDF e obtenha informações relevantes.",
).launch()
