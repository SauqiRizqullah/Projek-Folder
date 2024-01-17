from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options as chrome_opts
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
import os


def get_browser(launch_on='local'):
    """
    launch: launch selenium driver in 'local' environment or 'server' environtment. Default is 'local'
    """
    co = chrome_opts()    
    if launch_on == 'local':
        co.add_experimental_option("detach", True)
        driver = Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=co)
    else:
        pass
        co.add_argument("--headless")
        co.add_argument("--disable-dev-shm-usage")
        co.add_argument("--no-sandbox")
        driver = Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=co)

    return driver


def extract_data(index, driver):
    try:
        # extract data
        kode_xpath = f'//*[@id="tbllelang"]/tbody/tr[{index}]/td[1]'
        kode = driver.find_element(By.XPATH, kode_xpath).text

        # extract nama paket
        paket_xpath = f'//*[@id="tbllelang"]/tbody/tr[{index}]/td[2]/p[1]/a'
        paket = driver.find_element(By.XPATH, paket_xpath).text

        if " Tender Gagal Tender Ulang" in paket:
            judul = paket.replace(" Tender Gagal Tender Ulang", "")
        elif " Tender Gagal" in paket:
            judul = paket.replace(" Tender Gagal", "")
        elif " Tender Batal" in paket:
            judul = paket.replace(" Tender Batal", "")       
        elif " Tender Ulang" in paket:
            judul = paket.replace(" Tender Ulang", "")
        elif " Seleksi Gagal Seleksi Ulang" in paket:
            judul = paket.replace(" Seleksi Gagal Seleksi Ulang", "")
        elif " Seleksi Gagal" in paket:
            judul = paket.replace(" Seleksi Gagal", "")
        elif " Seleksi Ulang" in paket:
            judul = paket.replace(" Seleksi Ulang", "")
        elif " Seleksi Batal" in paket:
            judul = paket.replace(" Seleksi Batal", "")
        else:
            judul = paket
        
        # extract tender/seleksi
        # extract using reverse slicing on the string
        if " Tender Gagal Tender Ulang" in paket:
            status_tender = paket[-1:-26:-1]
            reversed_status = status_tender[-1::-1]
        elif " Tender Ulang" in paket:
            status_tender = paket[-1:-13:-1]
            reversed_status = status_tender[-1::-1]
        elif " Tender Gagal" in paket:
            status_tender = paket[-1:-13:-1]
            reversed_status = status_tender[-1::-1]
        elif " Tender Batal" in paket:
            status_tender = paket[-1:-13:-1]
            reversed_status = status_tender[-1::-1]
        elif " Seleksi Gagal Seleksi Ulang" in paket:
            status_tender = paket[-1:-30:-1]
            reversed_status = status_tender[-1::-1]
        elif " Seleksi Gagal" in paket:
            status_tender = paket[-1:-15:-1]
            reversed_status = status_tender[-1::-1]
        elif " Seleksi Ulang" in paket:
            status_tender = paket[-1:-15:-1]
            reversed_status = status_tender[-1::-1]
        elif " Seleksi Batal" in paket:
            status_tender = paket[-1:-15:-1]
            reversed_status = status_tender[-1::-1]
        else:
            reversed_status = 'NONE'

        # extract link paket
        link = driver.find_element(By.XPATH, paket_xpath).get_attribute('href')

        # extract deskripsi paket
        deskripsi_paket_xpath = f'//*[@id="tbllelang"]/tbody/tr[{index}]/td[2]/p[2]'
        deskripsi_paket = driver.find_element(By.XPATH, deskripsi_paket_xpath).text

        # extract nilai kontrak
        nilai_kontrak_xpath = f'//*[@id="tbllelang"]/tbody/tr[{index}]/td[2]/p[3]'
        nilai_kontrak = driver.find_element(By.XPATH, nilai_kontrak_xpath).text
        kontrak = nilai_kontrak.replace("Nilai Kontrak : ", "")

        # extract nama klpd
        klpd_xpath = f'//*[@id="tbllelang"]/tbody/tr[{index}]/td[3]'
        klpd = driver.find_element(By.XPATH, klpd_xpath).text
                
        # extract tahapan lelang
        tahapan_xpath = f'//*[@id="tbllelang"]/tbody/tr[{index}]/td[4]/a'
        tahapan = driver.find_element(By.XPATH, tahapan_xpath).text

        # extract link tahapan lelang
        link_tahapan = driver.find_element(By.XPATH, tahapan_xpath).get_attribute('href')
                
        # extract nilai HPS
        hps_xpath = f'//*[@id="tbllelang"]/tbody/tr[{index}]/td[5]'
        hps = driver.find_element(By.XPATH, hps_xpath).text

    except StaleElementReferenceException:
        pass

    except NoSuchElementException:
        pass
            
    # simpan hasil ke list extracted data
    data = [kode, judul, reversed_status, link, deskripsi_paket, kontrak, klpd, tahapan, link_tahapan, hps]

    return data

    

if __name__ == '__main__':
    try:
        driver = get_browser()
        main_url = 'https://lpse.bmkg.go.id/eproc4/lelang?kategoriId=&tahun=&instansiId=&rekanan=&kontrak_status=&kontrak_tipe='
        driver.get(main_url)
        driver.maximize_window()
        sleep(10)
        
        # get maximum page
        last_page = driver.find_element(By.XPATH, '//*[@id="tbllelang_paginate"]/ul/li[9]/a').text
        last_page = int(last_page)

        extracted_data = []
        limit = 133
        end = limit - 1
        for z in range(1, limit):
            # get data from table
            print('Page ' + str(z))
            sleep(31)
            table_row_xpath = '//*[@id="tbllelang"]/tbody/tr'
            sleep(3)
            results = driver.find_elements(By.XPATH, table_row_xpath)
            finale = len(results) + 1

            for i in range(1, finale):
                sleep(5)
                data = extract_data(i, driver)
                extracted_data.append(data)

            if (z == end):
                break
            else:
                next_page = driver.find_element(By.XPATH, '//*[@id="tbllelang_next"]')
                sleep(3)
                driver.execute_script("arguments[0].click();", next_page)
            
        # save list to dataframe
        df_lpse = pd.DataFrame(extracted_data, columns = ['Kode', 'Nama Paket', 'Status Tender', 'Link', 'Deskripsi Paket', 'Nilai Kontrak', 'K/L/PD', 'Tahapan', 'Link Tahapan', 'HPS'])

        # save dataframe to csv
        df_lpse.to_csv('LPSE All Pages Complete.csv', index=False)
        print('Completed')

    
    except KeyboardInterrupt:
        driver.close()
        print('Closed')
