import os
from dotenv import load_dotenv
# Módulo do zabbix para manipulação de objetos: 
# https://github.com/zabbix/python-zabbix-utils
from zabbix_utils import ZabbixAPI
# Zabbix -> 192.168.2.36/zabbix -> Via DHCP no meu caso
# Função que autentica e retorna esse status para futuro uso em outras funções de ação ou consulta Zabbix
#api = autenticator_zabbix()
def autenticator_zabbix():
    autentication_status = False
    while autentication_status == False:
        load_dotenv("projeto_zabbix_1.0\\secrets\\zabbix_token.env")
        zabbix_api_auth = os.getenv("zabbix_token_api")
        if zabbix_api_auth is not None:
            print("Chave de API carregada com sucesso. Informe o endereço do seu servidor Zabbix.")
        else:
            print('Chave de API não encontrada, verifique o arquivo "projeto_zabbix_1.0\\tokens\\zabbix_token.env".')
        try:
            zabbix_server_address = str(input("Informe o endereço do servidor Zabbix: "))
            api = ZabbixAPI(url=zabbix_server_address)
            api.login(token=zabbix_api_auth)
            # Trazendo usuários para testar conexão
            users = api.user.get(
                output=['name']
            )
            if users:
                print("Conexão com o servidor realizada com sucesso.")
                autentication_status = True
                return api
        except:
            print("A autenticação falhou, verifique o token e o endereço informados.")
# Função para listar os usuários
def listar_usuarios(api):
    zabbix_users = api.user.get(
        output = ['userid', 'username', 'surname']
    )
    print("Usuários:")
    for user in zabbix_users:
        if user['username'] == 'guest':
            user['surname'] = 'Convidado'
        print(f'Usuário: {user['username']} -> Função: {user['surname']}')
# Função para listar hosts
def listar_hosts(api):
    zabbix_hosts = api.host.get(
        output = ['host', 'name']
    )
    for host_item in zabbix_hosts:
        print(f"Host: {host_item['host']}\n\tNome: {host_item['name']}")
# Função para listar grupo de host's
def listar_host_group(api):
    zabbix_host_group = api.hostgroup.get(
        output = ['name', 'groupid']
    )
    for group in zabbix_host_group:
        print(f"Grupo: {group['name']}\n\tId: {group['groupid']}")
# Função relatório de host's
def relatorio_hosts(api):
    eventos = []
    zabbix_relatorios_eventos = api.event.get(
        output = ['name']
    )
    for incidente in zabbix_relatorios_eventos:  
        if incidente['name'] not in eventos:
            eventos.append(incidente['name'])
    for problema in eventos:
        print('Incidentes:')
        print(problema)
# Função menu
def menu_zabbix(api):
    opcao_menu_status = 1
    opcoes = list(range(0,6))
    mensagem_layout = r""" ____                         _           _                               
    | __ )  ___ _ __ ___   __   _(_)_ __   __| | ___     __ _  ___            
    |  _ \ / _ \ '_ ` _ \  \ \ / / | '_ \ / _` |/ _ \   / _` |/ _ \           
    | |_) |  __/ | | | | |  \ V /| | | | | (_| | (_) | | (_| | (_) |          
    |____/ \___|_| |_| |_|   \_/ |_|_| |_|\__,_|\___/   \__,_|\___/           
    _____     _     _     _         ____ _     ___   __  __                  
    |__  /__ _| |__ | |__ (_)_  __  / ___| |   |_ _| |  \/  | ___ _ __  _   _ 
    / // _` | '_ \| '_ \| \ \/ / | |   | |    | |  | |\/| |/ _ \ '_ \| | | |
    / /| (_| | |_) | |_) | |>  <  | |___| |___ | |  | |  | |  __/ | | | |_| |
    /____\__,_|_.__/|_.__/|_/_/\_\  \____|_____|___| |_|  |_|\___|_| |_|\__,_|"""
    print(mensagem_layout)
    print("")
    while opcao_menu_status == 1:
        print("(1) Listar usuários")
        print("(2) Listar Host's")
        print("(3) Listar Grupo de Host's")
        print("(4) Relatório de Host's")
        print("(5) Açoes")
        print("(0) Sair do Programa")
        opcao_menu = int(input("Opção: "))
        if opcao_menu == 1:
            print("")
            listar_usuarios(api)
            print("")
        elif opcao_menu == 2:
            print("")
            listar_hosts(api)
            print("")
            # Função listar hosts
        elif opcao_menu == 3:
            print("")
            listar_host_group(api)
            print("")
            # Função listar grupo de hosts
        elif opcao_menu == 4:
            print("")
            relatorio_hosts(api)
            print("")
            # Função relatório de hosts
        elif opcao_menu == 5:
            print("")
            print("Em desenvolvimento")
            print("")
            # Função tomar ações
        elif opcao_menu == 0:
            print("Obrigado por usar. Finalizando programa.")
            opcao_menu_status = 0
        elif opcao_menu not in opcoes:
            print("Opção inválida")
            continue
# Programa principal
def main():
    api = autenticator_zabbix()
    menu_zabbix(api)

main()