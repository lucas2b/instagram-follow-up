import yagmail
import alvo
from datetime import datetime
import json

NOME_ARQUIVO = 'alvos'

def enviar_email(mensagem):
    yag = yagmail.SMTP()
    yagmail.register("email@email.com", "password") #autenticação smtp para utilizar email
    contents = [mensagem]
    yag.send('lucasbonine@live.com', 'Situação do perfil', contents) #email destino
    print("email enviado")
    
def retorna_lista_alvos(nome_arquivo):
    lista = []
    file1 = open(nome_arquivo, 'r')
    for line in file1:
        lista.append(line.rstrip())
    return lista

#lê o arquivo de alvos e monta lista de objetos de alvos
def carregar_lista_objetos_alvos():
    lista_alvos = []
    for item in retorna_lista_alvos(NOME_ARQUIVO):
        array_nome_visibilidade = item.split("#")
        a = alvo.alvo(array_nome_visibilidade[0], True if array_nome_visibilidade[1] == 'privado' else False)
        lista_alvos.append(a)
    
    return lista_alvos

def hora_atual_string():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def login_instagram(loader):
    f = open('usuario_instagram.json')
    dados_json = json.load(f)
    loader.login(dados_json['usuario'], dados_json['senha'])