#realiza leitura de arquivo de alvos
#carrega lista de objetos contendo alvos
#percorre lista de objetos e verifica se situação de privacidade mudou

import minhas_libs as libs

#libs externas
import instaloader as instaloader
import time as time
import sys

TEMPO_INTERVALO_CONSULTA = 3600

#recuperando argumento para utilizar login no instagram
try:
    logarInstagram = sys.argv[1:][0]
except:
    logarInstagram = False

#------------- início programa -------------

lista_objetos_alvos = libs.carregar_lista_objetos_alvos()
loader = instaloader.Instaloader()

if logarInstagram == 'logar':
    print("Utilizará login no instagram...")
    libs.login_instagram(loader)
else:
    print("Não utilizará login no instagram...")

while True:
    for alvo in lista_objetos_alvos:
        
        #recupera atributos do objeto
        nome_perfil = alvo.nome
        isPerfilPrivado = alvo.isPrivado
        
        try:
            #realizando consulta instaloader
            profile = instaloader.Profile.from_username(loader.context, nome_perfil)
            isPrivateReturnInstaloader = profile.is_private
            
            #comparando e descobrindo perfis que não são mais privados
            situacao_string = "PRIVADO" if isPrivateReturnInstaloader else "PÚBLICO"  # recupera situação atual do instaloader
            if isPrivateReturnInstaloader == isPerfilPrivado:
                #privacidade do perfil não mudou
                mensagem_nao_mudou = f"Situação do Perfil do(a) {nome_perfil.upper()} não mudou. Situação: {situacao_string}"
                print(mensagem_nao_mudou)
            else:
                #privacidade do perfil mudou
                mensagem_mudou = f"\n--->>> Atenção!!!! Situação do Perfil do(a) {nome_perfil.upper()} MUDOU!!!. Situação: {situacao_string}.\n"
                print(mensagem_mudou)

                #se perfil se tornou público, baixar o mesmo
                if not isPrivateReturnInstaloader:
                    print(f"Baixando perfil do(a) {nome_perfil}...")
                    loader.download_profile(nome_perfil)
                    print(f"Baixou o perfil do(a) {nome_perfil}...")
                    
                #libs.enviar_email(mensagem_mudou)

        except instaloader.LoginRequiredException:
            print(f"Ocorreu uma exceção de login necessário... aguardando {TEMPO_INTERVALO_CONSULTA/60}min... - {libs.hora_atual_string()}\n")
            time.sleep(TEMPO_INTERVALO_CONSULTA)
    
    print(f"\nAdormecendo por {TEMPO_INTERVALO_CONSULTA/60} minutos.... - {libs.hora_atual_string()}\n")
    time.sleep(TEMPO_INTERVALO_CONSULTA)
