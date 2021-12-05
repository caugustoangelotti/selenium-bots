from selenium import webdriver
from selenium.webdriver.common.by import By
import os, time, threading, sys

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"

#=========CONTA DO TWITTER \/ =========
USER = ""
PASS = ""
#=========CONTA DO TWITTER /\ =========

HEADLESS_MODE = True

if(USER == "" or PASS == ""):
    print("Usuario e senha vazios! Encerrando...")
    exit()

caminhoLista = input("Arraste a lista com os links para serem reportados")
if(caminhoLista):
    nomelista = caminhoLista.split("\\")
else:
    print("Lista não encontrada. encerrando!...")
    exit()
payload = input("Insira o payload do xss:")
start = input(f'Reportar links da lista |{nomelista[3]}| com o payload | {payload} | ?(S):')

if(not start.lower() == 's'):
    print('i´m a joke to you ? ;(. encerrando!...')
    exit()

os.system('color 05')
def animacao():
    chars = ">>>.WORKING.<<< -->BE HAPPY<--"
    a = ""
    os.system('cls')
    for char in chars:
        a += char
        sys.stdout.write('\r'+'Status: '+a)
        time.sleep(.1)
        sys.stdout.flush()
    a = ""
    os.system('cls')

#=================LOGIN-FUNCTIONS======================

#VERIFICA SE USUARIO JA ESTA LOGADO
def isLoged(driver):
    try:                                       
        logout = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div/div[2]/ul[1]/li[1]/a")
        return True
    except:
        return False

#FUNCAO QUE VERIFICA O TIPO DE LOGIN, AUTORIZAR OU ATRAVES DOS DADOS DE LOGIN
def userAndPassLoginMethod(driver):
    try:
        esqueceusenha = driver.find_element(By.XPATH,'//*[@id="oauth_form"]/fieldset[1]/p/a')
        return True
    except:
        return False

#FAZ LOGIN NO SITE PELO TWITTER
def twitterLogin(driver,user, senha):
    loginWithTwitterButton(driver)
    if(userAndPassLoginMethod(driver)):
        #LOGIN COM USUARIO E SENHA
        #label user twitter
        lblUser = driver.find_element(By.XPATH,'//*[@id="username_or_email"]')
        #label senha twitter
        lblSenha = driver.find_element(By.XPATH,'//*[@id="password"]')
        lblUser.send_keys(user)
        lblSenha.send_keys(senha)
        #login button twitter
        btn_login = driver.find_element(By.XPATH,'//*[@id="allow"]')
        btn_login.click()
        driver.get("https://www.openbugbounty.org/report/")
    else:
        #LOGIN COM TWITTER JA LOGADO
        btn_appAuth = driver.find_element(By.XPATH,'//*[@id="allow"]')
        btn_appAuth.click()
        driver.get("https://www.openbugbounty.org/report/")

#CLICA NO BOTAO SIGN WITH TWITTER
def loginWithTwitterButton(driver):                    
    twitterSignButton = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div/form/input[2]')
    twitterSignButton.click()
#======================================================

def startDriverWithHeadLessConfig():
    options = webdriver.ChromeOptions()
    options.headless = HEADLESS_MODE
    path = os.path.abspath("default")
    options.add_argument(f'user-agent={USER_AGENT}')
    options.add_argument("--window-size=1600,900")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("user-data-dir=" + path)
    options.add_argument('log-level=3')
    return webdriver.Chrome(executable_path="chromedriver.exe", options=options)

def countReports(driver):
    try:
        element = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/table[1]/tbody/tr/td')
        if(not element.text == "Thank you! Public vulnerability submission will be verified soon."):
            return 0
        return 1
    except:
        return 0

def waitFullLoad(driver):
    try:
        element = driver.find_element(By.XPATH,'//*[@id="url1"]')
        return
    except:
        waitFullLoad(driver)

def doReport(driver, url, postdata):
    waitFullLoad(driver)
    driver.find_element(By.XPATH,'//*[@id="agreeethics"]').click()
    urlElemnt = driver.find_element(By.XPATH,'//*[@id="url1"]')
    postDataElement = driver.find_element(By.XPATH,'//*[@id="postparams"]')
    driver.execute_script(f"arguments[0].value='';", urlElemnt)
    driver.execute_script(f"arguments[0].value='';", postDataElement)
    driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[1]/table/tbody/tr/td/table/tbody/tr/td/form/table[4]/tbody/tr[17]/td/p/label/span[1]').click()
    postDataElement.send_keys(postdata)
    urlElemnt.send_keys(url)


with open(caminhoLista,'r') as arqv:
    urls = arqv.readlines()
total = [0]
def mainThread(): 
    apvTotal = 0
    driver = startDriverWithHeadLessConfig()
    driver.get("https://www.openbugbounty.org/report/")
    try:
        driver.find_element(By.XPATH,'//*[@id="thn"]/img[2]').click()
    except:
        pass
    driver.get("https://www.openbugbounty.org/report/")
    if(not isLoged(driver)):
        twitterLogin(driver, USER, PASS)

    for url in urls:
        doReport(driver, url, payload)
        apvTotal = apvTotal + countReports(driver)
        driver.get("https://www.openbugbounty.org/report/")
    total[0] = apvTotal

mainProcess = threading.Thread(name='happyReport', target=mainThread)
mainProcess.start()

while mainProcess.is_alive():
    animacao()
print(f"{total[0]} sites foram reportados com sucesso!")
input("Pressione enter para sair!")
exit()