from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import pandas as pd
import re
import json


def scrape(category, id_category):
    chrome_service = Service("/usr/bin/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=chrome_service, options=options)

    url = f"https://bwf.tournamentsoftware.com/ranking/category.aspx?id=35416&category={id_category}"
    driver.get(url)
    table = driver.find_element(By.CLASS_NAME, "ruler")
    time.sleep(3)
    bwf_rank = []



    page = 1
    while page <= 1:
        # Get all the rows in the table
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Iterate over each row and extract the desired data
        for row in rows:
            # Get the cells in each row
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 1:
                if category in ["ms", "ws"]:
                    rank = cells[0].text
                    prev_rank_str = cells[1].get_attribute("title")
                    prev_rank = 0
                    match = re.search(r"\d+", prev_rank_str)
                    if match:
                        prev_rank = match.group()
                    country_id = cells[3].text
                    player = cells[4].text
                    player_profile_url = (
                        cells[4].find_element(By.TAG_NAME, "a").get_attribute("href")
                    )
                    country_flag_img_url = (
                        cells[4].find_element(By.TAG_NAME, "img").get_attribute("src")
                    )
                    member_id = cells[6].text
                    points = cells[7].text
                    tournaments = cells[8].text
                    confedaration = cells[9].text

                    current_rank_data = {
                        "rank": rank,
                        "previous_rank": prev_rank,
                        "country_id": country_id,
                        "country_flag_img_url": country_flag_img_url,
                        "player_name": player,
                        "player_profile_url": player_profile_url,
                        "member_id": member_id,
                        "points": points,
                        "tournaments": tournaments,
                        "confederation": confedaration,
                    }

                    bwf_rank.append(current_rank_data)
                else:
                    rank = cells[0].text
                    prev_rank_str = cells[1].get_attribute("title")
                    prev_rank = 0
                    match = re.search(r"\d+", prev_rank_str)
                    if match:
                        prev_rank = match.group()
                    country_ids = cells[3].find_elements(By.TAG_NAME, "p")
                    country_id_1 = country_ids[0].text
                    country_id_2 = country_ids[1].text
                    players = cells[4].find_elements(By.TAG_NAME, "p")
                    player_name_1 = players[0].text
                    player_name_2 = players[1].text
                    player_profile_url_1 = (
                        players[0].find_element(By.TAG_NAME, "a").get_attribute("href")
                    )
                    player_profile_url_2 = (
                        players[1].find_element(By.TAG_NAME, "a").get_attribute("href")
                    )
                    country_flag_img_url_1 = (
                        players[0].find_element(By.TAG_NAME, "img").get_attribute("src")
                    )
                    country_flag_img_url_2 = (
                        players[1].find_element(By.TAG_NAME, "img").get_attribute("src")
                    )
                    member_ids = cells[6].text.split("\n")
                    member_id_1 = member_ids[0]
                    member_id_2 = member_ids[1]
                    points = cells[7].text
                    tournaments = cells[8].text
                    confedaration = cells[9].find_elements(By.TAG_NAME, "a")
                    
                    confedaration_1 = False
                    confedaration_2 = False
                    if len(confedaration) == 1:
                        confedaration_1 = confedaration[0].text
                        confedaration_2 = confedaration[0].text
                    else:
                        confedaration_1 = confedaration[0].text
                        confedaration_2 = confedaration[1].text

                    current_rank_data = {
                        "rank": rank,
                        "previous_rank": prev_rank,
                        "country_id_1": country_id_1,
                        "country_id_2": country_id_2,
                        "country_flag_img_url_1": country_flag_img_url_1,
                        "country_flag_img_url_2": country_flag_img_url_2,
                        "player_name_1": player_name_1,
                        "player_name_2": player_name_2,
                        "player_profile_url_1": player_profile_url_1,
                        "player_profile_url_2": player_profile_url_2,
                        "member_id_1": member_id_1,
                        "member_id_2": member_id_2,
                        "points": points,
                        "tournaments": tournaments,
                        "confederation_1": confedaration_1,
                        "confederation_2": confedaration_2,
                    }

                    bwf_rank.append(current_rank_data)
        page += 1
        time.sleep(3)

        try:
            # Check if there is a next page button
            next_button = driver.find_element(By.CLASS_NAME, "page_next")
            # Click on the pagination link
            next_button.click()
            # Wait for the table to reload after clicking the link
            WebDriverWait(driver, 10).until(EC.staleness_of(table))
            # Find the table element again after the page reloads
            table = driver.find_element(By.CLASS_NAME, "ruler")
        except NoSuchElementException:
            break

    driver.quit()

    with open(f"./data/bwf-rank-{category}.json", "w") as json_file:
        json.dump(bwf_rank, json_file)

if __name__ == "__main__":
    scrape("ms", 472)
    # scrape("ws", 473)
    # scrape("md", 474)
    # scrape("wd", 475)
    # scrape("xd", 476)