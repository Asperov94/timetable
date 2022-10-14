from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import requests
import yaml
# import os


def telegram_image(group_id: dict, send_image: str, text='')-> int:
  with open(send_image, 'rb') as image_fd:
    url = 'https://api.telegram.org/' + config['telegram']["bot"]+ '/' + 'sendPhoto'
    data = { 'chat_id' : group_id,  "caption": text, "parse_mode": 'Markdown',  "disable_web_page_preview": 'true'}
    response=requests.post(
    url,
    data=data,
    files={'photo': image_fd})
    return response.status_code


class Mti_bot():
  def __init__(self):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage') 
    self.driver = webdriver.Chrome(chrome_options=options)
  

  def timetable(self, config):
    self.driver.set_window_size(1800, 1400)
    self.driver.get("https://lms.mti.edu.ru/")
    time.sleep(10) # Sleep for 3 seconds
    self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/form/input[1]').send_keys(config["mti"]["login"])
    time.sleep(1)
    self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/form/input[3]').send_keys(config["mti"]["password"])
    time.sleep(1)
    self.driver.find_element(By.XPATH, '//*[@id="popupLoginBtn"]').click()
    time.sleep(10)
    self.driver.get("https://lms.mti.edu.ru/schedule/academ?print=1")
    self.driver.save_screenshot("screenshot.png")
    time.sleep(1)
    self.driver.quit()
    

if __name__ == "__main__":
  with open("config.yml", "r") as ymlfile:
    config = yaml.safe_load(ymlfile)
  # config = {}
  # config['mti']['login'] = os.environ.get('login')
  # config['mti']['password'] = os.environ.get('password')
  # config['telegram']['bot'] = os.environ.get('bot')
  # config['telegram']['id_group'] = os.environ.get('group')
  s = Mti_bot()
  s.timetable(config)
  telegram_image(config['telegram']['id_group'],"screenshot.png", "")
