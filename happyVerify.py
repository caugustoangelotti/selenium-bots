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
    print("Usuario e senha vazio! encerrando....")
    exit()

os.system('color 05')
def animacao():
    chars = ">>>.VERYFING REPORTS.<<< -->BE HAPPY<--"
    a = ""
    os.system('cls')
    for char in chars:
        a += char
        sys.stdout.write('\r'+'Status: '+ a)
        time.sleep(.1)
        sys.stdout.flush()
    a = ""
    os.system('cls')

#ENVIA PEDIDO DE CHECAGEM DOS REPORTS
def checkNow(driver, xpath):
    #number parser
    reportNumber = xpath.split("/")
    reportNumber = reportNumber[8].split("[")
    reportNumber = reportNumber[1].strip("]")
    #check now button open bug bounty site
    checkButton = driver.find_element(By.XPATH,xpath)
    checkButton.click()
    #send report button open bug bounty
    submitButton = driver.find_element(By.XPATH, f"/html/body/div[1]/div[3]/div[1]/table/tbody/tr[{reportNumber}]/td[5]/div/form/table/tbody/tr[2]/td[1]/input")
    submitButton.click()

#NEVEGAO ENTRE AS PAGINAS DE REPORTS
def pageNavigation(driver, page = 1):
    driver.get(f"https://www.openbugbounty.org/researchers/{USER}/onhold/page/{page}/")
    try:
        element = driver.find_element(By.XPATH,'//*[@id="thn"]/img[2]')
        element.click()
    except:
        pass
    driver.get(f"https://www.openbugbounty.org/researchers/{USER}/onhold/page/{page}/")

#RETORNA O NUMERO EXISTENTE DE CHECKS PENDENTES
def checksCount(driver):
    patchList = []
    reports = getNumberOfReports(driver) + 1
    for i in range(1,reports):
        try:
            report = driver.find_element(By.XPATH,f"/html/body/div[1]/div[3]/div[1]/table/tbody/tr[{i}]/td[5]/a")
            patchList.append(f"/html/body/div[1]/div[3]/div[1]/table/tbody/tr[{i}]/td[5]/a")
        except:
            continue
    return patchList

#RETORNA O NUMERO DE REPORTS POR PAGINA
def getNumberOfReports(driver):
    reportsTable = driver.find_elements_by_xpath("//table[@class='wishlist open-bounty']/tbody/tr")
    return len(reportsTable)

#RETORNA O NUMERO DE PAGINAS DE REPORTS
def getNumberOfPages(driver):
    pagesNav = driver.find_elements_by_xpath("//div[@class='pagenav']/a")
    return int(pagesNav[len(pagesNav) - 1].text)

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
total = [0]
def mainThread(): 
    driver = startDriverWithHeadLessConfig()
    driver.get("https://www.openbugbounty.org/report/")
    try:
        element = driver.find_element(By.XPATH,'//*[@id="thn"]/img[2]')
        element.click()
    except:
        pass
    driver.get("https://www.openbugbounty.org/report/")
    if(not isLoged(driver)):
        twitterLogin(driver, USER, PASS)

    pageNavigation(driver)
    pageCount = getNumberOfPages(driver)
    currentPage = 1
    totalChecks = 0

    while (currentPage <= pageCount):
        pageNavigation(driver,currentPage)
        if(currentPage % 15 == 0):
            pageCount = getNumberOfPages(driver)

        toCheck = checksCount(driver)
        totalChecks = totalChecks + len(toCheck)
        for xpath in toCheck:
            checkNow(driver, xpath)

        currentPage += 1
    total[0] = totalChecks
    driver.quit()

mainProcess = threading.Thread(name='happyReport', target=mainThread)
mainProcess.start()
while mainProcess.is_alive():
    animacao()
print(f"Verificacao concluida um total de {total[0]} reports estavam disponiveis para verificação!")
input("Pressione enter para sair!")
exit()