from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

import sys


def getCoordinates(id):
    '''
    Extracts latitud and longitud from avalanche ID.

    Positional arguments:
    id ---- ID of Avalanche accidents in ACNA's accident database.

    Returns:
    list: list with two elements, the first one corresponds to the latitud
          of the accident and the other one to the longitud.
    '''
    # url
    URL = "https://backoffice.acna.cat/accidents/" + id
    # going to website
    driver = webdriver.Chrome()

    Lat = ""
    Long = ""
    try:

        driver.get(URL)

        # Web Driver Wait used for when it is needed to wait for an element to appear
        wait = WebDriverWait(driver, 10)
        #Scrolling map into view so lat and long are visible
        #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.leaflet-container.leaflet-touch.leaflet-fade-anim.leaflet-grab.leaflet-touch-drag.leaflet-touch-zoom')))
        
        #m = driver.find_element(By.CSS_SELECTOR, '.leaflet-container.leaflet-touch.leaflet-fade-anim.leaflet-grab.leaflet-touch-drag.leaflet-touch-zoom')

        #driver.execute_script("arguments[0].scrollIntoView(true);", m)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/dl/div[6]/dd')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/dl/div[7]/dd')))

            Lat = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/dl/div[6]/dd').text

            Long = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[2]/dl/div[7]/dd').text
        except:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[3]/div[2]/dl/div[6]/dd')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[3]/div[2]/dl/div[7]/dd')))

            Lat = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[3]/div[2]/dl/div[6]/dd').text

            Long = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[3]/div[2]/dl/div[7]/dd').text


    except Exception as e:
        # In case an error happens close the driver
        print("Error ocurred:", e)
        driver.quit()
    
    driver.quit()

    return [Lat, Long]


def GetInformation(season, outputDirectory):
    '''
    Collects accidents from a certain season from ACNA's avalanche database
    avalaible at their oficial website.

    Positional arguments:
    season ---- Season from which you want to gather information.
    outputDirectory ---- Output directory where the output csv file will
                        be created.

    Returns:
    The function creates a csv file in the specified output directory. This
    file will be called: "Accidents_SEASON.csv".
    '''
    # Initialising driver
    print(outputDirectory + "/Accidents_" + season + ".csv")
    File = open(outputDirectory + "/Accidentes_" + season + ".csv", "w+")
    print("ID;Data;Lloc;Grau_Perill;Tipus_Desencadenant;Origen;Mida;Membres;Arrossegats;Ferits;Morts;Activitat;lat;long", file = File)
    driver = webdriver.Chrome()
    
    try:
        # Going to the website of interest
        driver.get("https://backoffice.acna.cat/?season=" + season)
    
        # Web Driver Wait used for when it is needed to wait for an element to appear
        wait = WebDriverWait(driver, 10)
        # Since the page is buggy, the elements of the season are not shown until the next page button
        # is pressed, therefore before extracting any information the button must be pressed.
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@title="Go to next page"]')))

        NextButton = driver.find_element(By.XPATH, '//*[@title="Go to next page"]')

        wait.until(EC.element_to_be_clickable(NextButton))
        
        driver.execute_script("arguments[0].scrollIntoView(true);", NextButton)

        NextButton.click()
        # Wait two seconds before continuing, this is done to avoid put too much preasure to the website
        time.sleep(2)
        # Extract data from table
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiDataGrid-virtualScrollerRenderZone.css-1vouojk")))

        Table = driver.find_element(By.CSS_SELECTOR, ".MuiDataGrid-virtualScrollerRenderZone.css-1vouojk")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiDataGrid-virtualScrollerRenderZone.css-1vouojk")))

        rows = wait.until(lambda Table: Table.find_elements(By.CSS_SELECTOR, ".MuiDataGrid-row"))

        for r in rows:
            Els = r.find_elements(By.CSS_SELECTOR, ".MuiDataGrid-cell")
            ID = r.get_attribute("data-id")
            textToAdd = ID + ";"
            for i in Els:
                textToAdd += i.text + ";"
            time.sleep(1)
            Cordinates = getCoordinates(ID)
            print(textToAdd + Cordinates[0] + ";" + Cordinates[1], end = "\n", file = File)

        File.close()

    except Exception as e:
        # In case an error happens close the driver
        print("Error ocurred:", e)
        driver.quit()
        File.close()

    driver.quit()
    File.close()