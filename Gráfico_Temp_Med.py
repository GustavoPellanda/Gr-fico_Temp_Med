from time import sleep
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

# Guarda os valores referentes a cada cidade no XPATH
cidades_dicionario = {'Belo Horizonte': 5, 'Curitiba': 15, 'Florianópolis': 16, 'Manaus': 28, 'Porto Alegre': 36, 'Rio de Janeiro': 46, 'São Paulo': 52}

# Busca as temperaturas no site
def busca_temperaturas(pagina_temperaturas_ID):
    temperaturas = []
    for i in range(4, 16):
        xpath = f'//*[@id="{pagina_temperaturas_ID}"]/table/tbody[9]/tr[2]/td[{i}]/b'
        busca_temperatura = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        temperatura = float(busca_temperatura.text)
        temperaturas.append(temperatura)
    return temperaturas

# Abre a cidade selecionada:
def abre_cidade(driver, num_escolhido):
    xpath = '//*[@id="ui-id-18"]/a[{}]' # Cidade muda conforme o número de a[ ] no XPATH //*[@id="ui-id-18"]/a[15]
    xpath = xpath.format(num_escolhido)
    cidade_escolhida = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    cidade_escolhida.click()

# Abre o menu para a escolha da cidade e retorna o valor que será inserido no XPATH
def menu():
    
    # Exibe as opções
    print('\nEscolha a cidade:')
    for cidade_index, cidade_nome in enumerate(cidades_dicionario.keys(), start=1):
        print(f'{cidade_index} - {cidade_nome}')
    
    # Recebe a escolha do usuário
    cidade_escolher = int(input('\nDigite o número da cidade: '))
    
    # Caso o número selecionado não exista
    while cidade_escolher not in range(1, len(cidades_dicionario)+1):
        print('Opção inválida. Digite novamente.')
        cidade_escolher = int(input('Digite o número da cidade: '))
    
    # Relaciona o número escolhido com o número do XPATH salvo no dicionário
    cidade_escolhida = list(cidades_dicionario.keys())[cidade_escolher-1]
    cidade_valor = cidades_dicionario[cidade_escolhida]
    
    # Retorna o número do XPATH
    return cidade_valor

# Cidade recebe o número do XPATH da cidade escolhida e Nome Cidade armazena o nome da cidade de acordo com ele
cidade = menu()
nome_cidade = [cidade_nome for cidade_nome, cidade_codigo in cidades_dicionario.items() if cidade_codigo == cidade][0]

# Esse id será usado para obter o XPATH das temperaturas (ele muda para cada página)
# Uma melhoria futura seria incluí-lo no dicionário
if cidade == 5:
    id_cidade = '835870_10'
if cidade == 15:
    id_cidade = '838400_10'
if cidade == 16:
    id_cidade = '838990_10'
if cidade == 28:
    id_cidade = '821110_10'
if cidade == 36:
    id_cidade = '839710_10'
if cidade == 46:
    id_cidade = '837550_10'
if cidade == 52:
    id_cidade = '837800_10'

# Garante que esteja sendo usada a última versão do chrome
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()) )

# Abre o site
driver.get('http://ashrae-meteo.info/v2.0/places.php?continent=Latin%20America')

# Seleciona 2021
escolhe_ano = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="radio"]/label[4]/span[1]')))
escolhe_ano.click()

# Escolhe o Brasil
abre_Brasil = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ui-id-17"]/span')))                                     
abre_Brasil.click()

abre_cidade(driver, cidade)

# Muda para a guia atual
current_window = driver.current_window_handle
for window_handle in driver.window_handles:
    if window_handle != current_window:
        driver.switch_to.window(window_handle)

# Espera o elemento carregar
sleep(3)
driver.execute_script("window.scrollBy(0, 1000)")
sleep(3)

temperaturas = busca_temperaturas(id_cidade)

# Plota o gráfico
meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ,12]
plt.plot(meses, temperaturas)
plt.ylim(0, 35)
plt.xlim(1, 12)
plt.title(f'Temperatura Média em {nome_cidade} ao longo de 2021')
plt.xlabel('Mes')
plt.ylabel('Temperatura Média')
plt.show()
