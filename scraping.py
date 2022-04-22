import selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

def scrape_season_team(num_pages, season='2021-22'):
    #define starting URL, and open file for writing
    driver = webdriver.Chrome('chromedriver')
    begin_url = f'https://www.nba.com/stats/teams/boxscores/?Season={season}&SeasonType=Regular%20Season'
    f = open('team_data.txt', 'a')
    
    driver.get(begin_url)

    page_count = 0
    while page_count < num_pages:
        try:
            table = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]')
            f.write(table.text)
            next_page = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[3]/div/div/a[2]')
            next_page.click()
            page_count += 1
            sleep(.25)
        except:
            print(f"completed scraping {page_count + 1} pages")

    print("page_count = ", page_count)
    f.close()
    driver.quit()




#similar function as above, but for individual players
def scrape_season_player(num_pages, season='2021-22'):
   
    #define starting URL, and open file for writing
    driver = webdriver.Chrome('chromedriver')
    begin_url = f'https://www.nba.com/stats/players/boxscores/?Season={season}&SeasonType=Regular%20Season'
    f = open('player_data.txt', 'a')
    
    driver.get(begin_url)

    page_count = 0
    while page_count < num_pages:
        try:
            table = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]')
            next_page = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[3]/div/div/a[2]')
            f.write(table.text)
            next_page.click()
            page_count += 1
            sleep(1)
        except:
            print(f"completed scraping {page_count + 1} pages")

    print("page_count = ", page_count)
    f.close()
    driver.quit()
