from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os,time,sys,re,threading

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
HEADLESS_MODE = True
IPREGEX = '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
DEV = False

if(DEV):
    fileDir = "input.txt"
else:
    try:
        fileDir = sys.argv[1]
    except IndexError:
        print("Forneca o nome do arquivo ou caminho ex:py verifyip.py C:\\Users\\...")
        exit()

ipArray = []
with open(fileDir, 'r', encoding='utf-8') as file:
    ipArray = file.readlines()

os.system('color 0a')
def animacao():
    chars = ">>>.WORKING.<<< -->be Happy.<--"
    a = ""
    os.system('cls')
    for char in chars:
        a += char
        sys.stdout.write('\r'+'Status: '+a)
        time.sleep(.1)
        sys.stdout.flush()
    a = ""
    os.system('cls')

def startDriverWithHeadLessConfig():
    options = webdriver.ChromeOptions()
    options.headless = HEADLESS_MODE
    path = os.path.abspath("default")
    options.add_argument(f'user-agent={USER_AGENT}')
    options.add_argument("--window-size=1440,900")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument("--mute-audio")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("user-data-dir=" + path)
    options.add_argument('log-level=3')
    return webdriver.Chrome(executable_path="chromedriver.exe", options=options)

def searchNextIp(driver, ip):
    driver.get(f'https://www.abuseipdb.com/check/{ip}')

def buildData(driver,ip):
    return f'{ip.rstrip()},{getIsp(driver)},{getDomain(driver)},{getCountry(driver)},{ipIsFoundInDb(driver)}'

def getIsp(driver):
    try:
        isp = driver.find_element(By.XPATH, "//*[@id='report-wrapper']/div/div[1]/div/table/tbody/tr[1]/td")
        return isp.text
    except:
        return 'ISP Not Found'

def getDomain(driver):
    try:
        domain = driver.find_element(By.XPATH, "//*[@id='report-wrapper']/div/div[1]/div/table/tbody/tr[4]/td")
        return domain.text
    except:
        return 'Domain Not Found'

def getCountry(driver):
    try:
        country = driver.find_element(By.XPATH, "//*[@id='report-wrapper']/div/div[1]/div/table/tbody/tr[5]/td")
        return country.text
    except:
        return 'Country Not Found'

def checkToManyRequest(driver):
    try:
        toManyLabel = driver.find_element(By.XPATH, '//*[@id="content"]/div/h1/b')
        return 'not found' if toManyLabel.text == '404 Page Not Found' else 'to many'
    except:
        return False

def makeOutputFile(data, filename = 'output.txt'):
    with open(filename, 'a') as file:
        for line in data:
            file.write(f'{line}\n')

def ipIsFoundInDb(driver):
    try:
        dbStatus = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='report-wrapper']/div/div[1]/div/h3")))
        status = re.split(IPREGEX, dbStatus.text)
        status = status[1].strip()
        return False if status == 'was not found in our database' else True
    except TimeoutError as err:
        print(err)
        exit()

def mainThread():
    driver = startDriverWithHeadLessConfig()

    ipIndex = 0
    dataArr = []

    try:
        while ipIndex < len(ipArray):
            searchNextIp(driver,ipArray[ipIndex])
            check = checkToManyRequest(driver)
            if check:
                if check == 'not found':
                    ipIndex += 1
                    continue
                else:
                    time.sleep(0.4)
                    continue
            dataArr.append(buildData(driver,ipArray[ipIndex]))
            ipIndex += 1

    except KeyboardInterrupt:
        makeOutputFile(dataArr)
        exit()
    except Exception:
        makeOutputFile(dataArr)
        exit()
    else:
        makeOutputFile(dataArr)
        exit()

try:
    mainProcess = threading.Thread(name='process', target=mainThread)
    mainProcess.start()
    while mainProcess.is_alive():
        animacao()
except KeyboardInterrupt:
    mainProcess.join()
    print('\nInterrupcao do usuario salvando arquivo...')
    exit()
except Exception:
    mainProcess.join()
    print('\nErro desconhecido, salvando trabalho realizado e encerrando...')
    exit()
else:
    print('\nTrabalho concluido, salvando arquivo de saida....')
    exit()