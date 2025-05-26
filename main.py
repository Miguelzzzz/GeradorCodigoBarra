from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import os
import re
import unicodedata

def limpar_nome_arquivo(nome):
    nome = unicodedata.normalize('NFKD', nome)
    nome_sem_acento = ''.join(c for c in nome if not unicodedata.combining(c))
    nome_sem_acento = re.sub(r'[^a-zA-Z0-9_\- ]', '', nome_sem_acento)
    nome_sem_acento = nome_sem_acento.replace(' ', '_')
    return nome_sem_acento

produtos = [
    {"nome": "Medalha oval dupla Pequena", "codigo": "461234567811"},
    {"nome": "Medalha oval dupla Média", "codigo": "461234567813"},
    {"nome": "Medalha oval dupla Grande", "codigo": "461234567815"},

    {"nome": "Medalha quadrada Pequena", "codigo": "461234567822"},
    {"nome": "Medalha quadrada Média", "codigo": "461234567824"},
    {"nome": "Medalha quadrada Grande", "codigo": "461234567826"},

    {"nome": "Medalha sextavada", "codigo": "461234567833"},
    {"nome": "Medalha sextavada esmaltada", "codigo": "461234567835"},

    {"nome": "Decorativa Pequena", "codigo": "461234567844"},
    {"nome": "Decorativa Grande", "codigo": "461234567846"},
    {"nome": "Decorativa oval", "codigo": "461234567848"},

    {"nome": "Medalha detalhada", "codigo": "461234567855"},

    {"nome": "Medalha oval Pequena", "codigo": "461234567866"},
]

try:
    fonte = ImageFont.truetype("arial.ttf", 20)
except:
    fonte = ImageFont.load_default()

for produto in produtos:
    nome_produto = produto["nome"]
    codigo = produto["codigo"]

    writer_options = {
        'font_size': 7,  
        'text_distance': 3,
    }
    ean = barcode.get('ean13', codigo, writer=ImageWriter())
    temp_file = ean.save(f"codigo_temp_{codigo}", options=writer_options)

    imagem = Image.open(temp_file)
    largura, altura = imagem.size

    nova_altura = altura + 50
    nova_imagem = Image.new("RGB", (largura, nova_altura), "white")
    nova_imagem.paste(imagem, (0, 0))

    desenho = ImageDraw.Draw(nova_imagem)
    largura_texto = desenho.textlength(nome_produto, font=fonte)
    posicao_texto = ((largura - largura_texto) // 2, altura + 6)
    desenho.text(posicao_texto, nome_produto, fill="black", font=fonte)

    nome_arquivo_limpo = limpar_nome_arquivo(nome_produto)

    nome_arquivo = f"{nome_arquivo_limpo}.png"
    nova_imagem.save(nome_arquivo)
    print(f"Imagem salva: {nome_arquivo}")

    try:
        os.remove(temp_file)
    except Exception as e:
        print(f"Erro ao remover arquivo temporário: {e}")

print("Todos os códigos foram gerados com sucesso!")
