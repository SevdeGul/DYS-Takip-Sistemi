from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import argparse
from win10toast import ToastNotifier

def komut_alma():
    parser = argparse.ArgumentParser(description="DYS Uygulaması")
    parser.add_argument('-u', '--user', help="User_eposta")
    parser.add_argument('-p', '--passwd', help="Password")
    args = parser.parse_args()

    user_eposta = args.user
    password = args.passwd

    return [user_eposta,password]

def giris():
    path = 'geckodriver.exe'
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=options, executable_path=path)
    browser.get("https://dys.mu.edu.tr/login/index_auth.php")
    time.sleep(5)
    kullanici = browser.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/section/div/div[2]/form[2]/div[1]/input")
    sifre = browser.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/section/div/div[2]/form[2]/div[2]/input")
    giris_bilgileri = komut_alma()
    kullanici.send_keys(giris_bilgileri[0])
    sifre.send_keys(giris_bilgileri[1])
    browser.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/section/div/div[2]/form[2]/button").click()
    time.sleep(5)

    return browser

def ders_secimi():
    while True:
        browser = giris()
        time.sleep(2)
        ders_kutucugu = browser.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/section/div/div[2]/div")
        dersler = ders_kutucugu.find_elements(By.CLASS_NAME, "coursebox")

        ders_bilgileri = []
        for ders in dersler:
            ders_a_tag = ders.find_element(By.CLASS_NAME, "aalink")

            ders_adi = ders_a_tag.text
            ders_kodu = ders_adi.split(":")[0]
            #dosya(ders_kodu)

            ders_link = ders_a_tag.get_attribute("href")
            ders_bilgileri.append((ders_kodu,ders_link))

        for ders in ders_bilgileri:
            fark = karsilastir(browser,ders[0],ders[1])
            if fark == False:
                ders_icerigi = ders_icerigi_cek(browser, ders[1])
                dosya_yazma(ders[0], ders_icerigi)
                print("%s güncellendi! - URL: %s" % (ders[0],ders[1]))
                toast = ToastNotifier()
                toast.show_toast(
                    "DYS'de Yeni bir güncelleme var!",
                    "%s güncellendi! - URL: %s" % (ders[0],ders[1]),
                    duration = 20,
                    threaded = True,
                )

        #for element in ders_bilgileri:
        #    ders_icerigi = ders_icerigi_cek(browser,element[1])
        #    dosya_yazma(element[0],ders_icerigi)

        browser.close()
        time.sleep(3600)

def karsilastir(browser,ders_kodu,ders_link):
    ders_icerigi = ders_icerigi_cek(browser, ders_link)
    dosya = open(ders_kodu + ".txt", 'r', encoding="utf-8")
    dosya_icerigi = dosya.read()
    dosya.close()
    if ders_icerigi == dosya_icerigi:
        return True
    return False

def ders_icerigi_cek(browser, ders_link):
    browser.get(ders_link)
    sayfa = browser.find_element(By.ID, "region-main").text
    return sayfa

def dosya(ders_kodu):
    dosya = open(ders_kodu + ".txt" , "w", encoding="utf-8")
    dosya.close()

def dosya_yazma(ders_kodu,sayfa):
    dosya = open(ders_kodu + ".txt", "w", encoding="utf-8")
    dosya.write(sayfa)
    dosya.close()

ders_secimi()
