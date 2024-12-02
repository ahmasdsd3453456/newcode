import requests
import json
from bs4 import BeautifulSoup
import time
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import asyncio
import os

cookies_file_path = "cookie.json"




headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Not=A?Brand\";v=\"99\", \"Chromium\";v=\"118\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "Referer": "https://seo-fast.ru/work_youtube",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}




def load_cookies(cookies_file_path):
    with open(cookies_file_path, 'r') as f:
        cookies_data = json.load(f)
    cookies = {cookie['name']: cookie['value'] for cookie in cookies_data}
    return cookies





def check_cookies_working(cookies_file_path, username, password):
    # Load cookies
    cookies = load_cookies(cookies_file_path)
    
    url = "https://seo-fast.ru/payment_user"
    
    # Check the page with cookies
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    balance_element = soup.find('span', {'style': 'color: #ffffff; font-weight: bold; text-shadow: 0 0 2px rgba(158,157,157,0.4);'})
    if balance_element:
        balance = balance_element.get_text(strip=True)
        print(f"Balance: {balance}")
    else:
        print("Cookies expired. Logging in again...")
        
        # Set up Selenium with Chrome options and webdriver manager
        options = Options()
        options.headless = True  # Running in headless mode
        options.add_argument("--no-sandbox")  # Disables the sandbox, necessary for some environments
        options.add_argument("--disable-dev-shm-usage")  # Fixes issues with shared memory in Docker environments
        options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
        options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration (useful in headless mode)
        options.add_argument("--headless")  # Ensure Chrome is in headless mode
        options.add_argument("--disable-software-rasterizer")  # Disables software rasterizer
        service = Service(ChromeDriverManager().install())  # Automatically downloads the correct ChromeDriver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Go to login page
        login_url = "https://seo-fast.ru/login"
        driver.get(login_url)
        
        # Fill in the login form
        driver.find_element(By.ID, 'logusername').send_keys(username)
        driver.find_element(By.ID, 'logpassword').send_keys(password)
        
        # Click the login button
        login_button = driver.find_element(By.CSS_SELECTOR, 'a.sf_button:has-text("Вход")')
        login_button.click()
        
        # Wait for login to complete (you can adjust the time depending on the website speed)
        time.sleep(10)
        
        # Get cookies after login
        cookies = driver.get_cookies()
        
        # Save cookies to file
        with open(cookies_file_path, "w") as f:
            json.dump(cookies, f, indent=4)
        
        print(f"Cookies have been saved to {cookies_file_path}.")
        
        # Close the browser
        driver.quit()




def delete_already_watching_videos():
    cookies = load_cookies(cookies_file_path) 
    url = "https://seo-fast.ru/infoall.php"
    payload = {
    "i_see_y": "ok"
        }
    response = requests.post(url, headers=headers, data=payload, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_divs = soup.find_all('div', id=True)
    for div in video_divs:
        div_id = div.get('id', '')
        video_id = div_id.replace('id_i_see_y', '') 
        print(video_id) 
        url2 = "https://seo-fast.ru/ajax/ajax_rest_sf.php"
        data1 = {
        "sf": "del_i_see_y",
        "id": video_id
        }
        response = requests.post(url2, headers=headers, data=data1, cookies=cookies)
    print("successfully deleted already watching videos...")






def get_bonus(cookies_file_path):
    cookies = load_cookies(cookies_file_path) 
    work_youtube_url = "https://seo-fast.ru/work_youtube"
    response = requests.get(work_youtube_url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    actions_bonus = soup.find(id="actions_bonus").get_text()
    first_digit = ''.join(filter(str.isdigit, actions_bonus.split()[0]))
    print(f"Today Your views are: {first_digit}")
    if int(first_digit) > 300:
        url = "https://seo-fast.ru/ajax/ajax_rest_sf.php"
        data = {
            'sf': 'actions_bonus'
                }
        response = requests.post(url, headers=headers, data=data, cookies=cookies)
        print(response.text)




def get_links_1():
    cookies = load_cookies(cookies_file_path) 
    work_youtube_url = "https://seo-fast.ru/work_youtube?all"
    response = requests.get(work_youtube_url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', onclick=lambda value: value and "start_youtube_view" in value)
    ids = []
    for link in links:
        onclick_value = link['onclick']
        start = onclick_value.find("start_youtube_view('") + len("start_youtube_view('")
        end = onclick_value.find("')", start)
        extracted_id = onclick_value[start:end]
        ids.append(extracted_id)
    print("Extracted IDs:", ids)
    all_data = []
    count = 0
    for extracted_id in ids:
        if count >= 10:  # Process only 10 ids
            break
        payload = {
            "sf": "start_youtube_view_y",
            "id": extracted_id
        }
        time.sleep(0.2)
        url2 = "https://seo-fast.ru/site_youtube/ajax/ajax_youtube_nobd.php"
        response = requests.post(url2, headers=headers, data=payload, cookies=cookies)
        response_data = json.loads(response.text)
        url1 = response_data.get("url")
        if url1 and url1.startswith("https://noref.site/#"):
            url1 = url1[len("https://noref.site/#"):]
            print(url1)
            data_to_save = {"url": url1}
            all_data.append(data_to_save)
        count += 1    
    with open("urls.txt", "w") as f:
        json.dump(all_data, f, indent=4)
    print("All Urls saved to urls.txt... now watching started....")



def get_links_2():
    cookies = load_cookies(cookies_file_path) 
    work_youtube_url = "https://seo-fast.ru/work_youtube?youtube_time"
    response = requests.get(work_youtube_url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', onclick=lambda value: value and "start_youtube_view" in value)
    ids = []
    for link in links:
        onclick_value = link['onclick']
        start = onclick_value.find("start_youtube_view('") + len("start_youtube_view('")
        end = onclick_value.find("')", start)
        extracted_id = onclick_value[start:end]
        ids.append(extracted_id)
    print("Extracted IDs:", ids)
    all_data = []
    count = 0
    for extracted_id in ids:
        if count >= 10:  # Process only 10 ids
            break
        payload = {
            "sf": "start_youtube_view_y",
            "id": extracted_id
        }
        time.sleep(0.2)
        url2 = "https://seo-fast.ru/site_youtube/ajax/ajax_youtube_nobd.php"
        response = requests.post(url2, headers=headers, data=payload, cookies=cookies)
        response_data = json.loads(response.text)
        url1 = response_data.get("url")
        if url1 and url1.startswith("https://noref.site/#"):
            url1 = url1[len("https://noref.site/#"):]
            print(url1)
            data_to_save = {"url": url1}
            all_data.append(data_to_save)
        count += 1    
    with open("urls.txt", "w") as f:
        json.dump(all_data, f, indent=4)
    print("All Urls saved to urls.txt... now watching started....")



def get_links_3():
    cookies = load_cookies(cookies_file_path) 
    work_youtube_url = "https://seo-fast.ru/work_youtube?youtube_exclusiv_2"
    response = requests.get(work_youtube_url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', onclick=lambda value: value and "start_youtube_view" in value)
    ids = []
    for link in links:
        onclick_value = link['onclick']
        start = onclick_value.find("start_youtube_view('") + len("start_youtube_view('")
        end = onclick_value.find("')", start)
        extracted_id = onclick_value[start:end]
        ids.append(extracted_id)
    print("Extracted IDs:", ids)
    all_data = []
    count = 0
    for extracted_id in ids:
        if count >= 10:  # Process only 10 ids
            break
        payload = {
            "sf": "start_youtube_view_y",
            "id": extracted_id
        }
        time.sleep(0.2)
        url2 = "https://seo-fast.ru/site_youtube/ajax/ajax_youtube_nobd.php"
        response = requests.post(url2, headers=headers, data=payload, cookies=cookies)
        response_data = json.loads(response.text)
        url1 = response_data.get("url")
        if url1 and url1.startswith("https://noref.site/#"):
            url1 = url1[len("https://noref.site/#"):]
            print(url1)
            data_to_save = {"url": url1}
            all_data.append(data_to_save)
        count += 1    
    with open("urls.txt", "w") as f:
        json.dump(all_data, f, indent=4)
    print("All Urls saved to urls.txt... now watching started....")




def get_links_4():
    cookies = load_cookies(cookies_file_path) 
    work_youtube_url = "https://seo-fast.ru/work_youtube?youtube_video_simple"
    response = requests.get(work_youtube_url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', onclick=lambda value: value and "start_youtube_view" in value)
    ids = []
    for link in links:
        onclick_value = link['onclick']
        start = onclick_value.find("start_youtube_view('") + len("start_youtube_view('")
        end = onclick_value.find("')", start)
        extracted_id = onclick_value[start:end]
        ids.append(extracted_id)
    print("Extracted IDs:", ids)
    all_data = []
    count = 0
    for extracted_id in ids:
        if count >= 10:  # Process only 10 ids
            break
        payload = {
            "sf": "start_youtube_view_y",
            "id": extracted_id
        }
        time.sleep(0.2)
        url2 = "https://seo-fast.ru/site_youtube/ajax/ajax_youtube_nobd.php"
        response = requests.post(url2, headers=headers, data=payload, cookies=cookies)
        response_data = json.loads(response.text)
        url1 = response_data.get("url")
        if url1 and url1.startswith("https://noref.site/#"):
            url1 = url1[len("https://noref.site/#"):]
            print(url1)
            data_to_save = {"url": url1}
            all_data.append(data_to_save)
        count += 1    
    with open("urls.txt", "w") as f:
        json.dump(all_data, f, indent=4)
    print("All Urls saved to urls.txt... now watching started....")




def get_links_5():
    cookies = load_cookies(cookies_file_path) 
    work_youtube_url = "https://seo-fast.ru/work_youtube"
    response = requests.get(work_youtube_url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', onclick=lambda value: value and "start_youtube_view" in value)
    ids = []
    for link in links:
        onclick_value = link['onclick']
        start = onclick_value.find("start_youtube_view('") + len("start_youtube_view('")
        end = onclick_value.find("')", start)
        extracted_id = onclick_value[start:end]
        ids.append(extracted_id)
    print("Extracted IDs:", ids)
    all_data = []
    count = 0
    for extracted_id in ids:
        if count >= 10:  # Process only 10 ids
            break
        payload = {
            "sf": "start_youtube_view_y",
            "id": extracted_id
        }
        time.sleep(0.2)
        url2 = "https://seo-fast.ru/site_youtube/ajax/ajax_youtube_nobd.php"
        response = requests.post(url2, headers=headers, data=payload, cookies=cookies)
        response_data = json.loads(response.text)
        url1 = response_data.get("url")
        if url1 and url1.startswith("https://noref.site/#"):
            url1 = url1[len("https://noref.site/#"):]
            print(url1)
            data_to_save = {"url": url1}
            all_data.append(data_to_save)
        count += 1    
    with open("urls.txt", "w") as f:
        json.dump(all_data, f, indent=4)
    print("All Urls saved to urls.txt... now watching started....")







#without login
def get_links_6():
    cookies = load_cookies(cookies_file_path) 
    work_youtube_url = "https://seo-fast.ru/work_youtube"
    response = requests.get(work_youtube_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    youtube_rows = soup.find_all('tr', id=lambda x: x and x.startswith('youtube'))
    ids = []
    for row in youtube_rows:
        link = row.find('a', onclick=lambda value: value and "go_login" in value)
        if link:
            onclick_value = link['onclick']
            start = onclick_value.find("go_login('") + len("go_login('")
            end = onclick_value.find("')", start)
            extracted_id = onclick_value[start:end]
            ids.append(extracted_id)
    print("Extracted IDs:", ids)
    all_data = []
    count = 0
    for extracted_id in ids[10:]:
        if count >= 20:  # Process only 10 ids
            break
        payload = {
            "sf": "start_youtube_view_y",
            "id": extracted_id
        }
        time.sleep(0.2)
        url2 = "https://seo-fast.ru/site_youtube/ajax/ajax_youtube_nobd.php"
        response = requests.post(url2, headers=headers, data=payload, cookies=cookies)
        response_data = json.loads(response.text)
        url1 = response_data.get("url")
        if url1 and url1.startswith("https://noref.site/#"):
            url1 = url1[len("https://noref.site/#"):]
            timer = int(url1.split("timer=")[1].split("&")[0])
            if int(timer > 1):
                print(url1)
                data_to_save = {"url": url1}
                all_data.append(data_to_save)
                count += 1    
    with open("urls.txt", "w") as f:
        json.dump(all_data, f, indent=4)
    print("All Urls saved to urls.txt... now watching started....")


















# Function to handle a single video with improved error handling using Selenium
async def play_video(driver, url, timer):
    print(f"Watching video: {url}")
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe#video-start')))  # Wait for iframe to load
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe#video-start')
        
        # Switch to the iframe to interact with it
        driver.switch_to.frame(iframe)
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ytp-large-play-button')))
        play_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-large-play-button')
        play_button.click()
        
        time.sleep(timer)  # Simulate watching the video for the given time
    except TimeoutException as e:
        print(f"Timeout error handling URL {url}: {e}")
    except Exception as e:
        print(f"Error handling URL {url}: {e}")
    finally:
        driver.switch_to.default_content()  # Return to the default content (main page)

# Function to handle multiple videos dynamically using Selenium
async def handle_videos(urls):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver_path = "/usr/local/bin/chromedriver"  # Change this if necessary
# Make sure the ChromeDriver is compatible with your version of Chrome
    service = Service(driver_path)  # This should automatically download the correct version of ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        tasks = []
        for url_data in urls:
            url = url_data["url"]
            timer = int(url.split("timer=")[1].split("&")[0]) + 5  # Extract timer value
            if timer > 300:
                print(f"Ignoring URL {url} as timer is greater than 300.")
                continue
            tasks.append(play_video(driver, url, timer))
            
            if len(tasks) >= 6:
                await asyncio.gather(*tasks)
                print(f"Completed 6 tasks. Remaining tasks: {len(tasks)}")
                tasks.clear()

        if tasks:
            await asyncio.gather(*tasks)

    except Exception as e:
        print(f"Error handling multiple videos: {e}")
    finally:
        driver.quit()

# Function to start video playback
async def start_watching_videos():
    try:
        with open("urls.txt", "r") as file:
            urls = json.load(file)
        print("Starting video playback for URLs...")
        await handle_videos(urls)
        print("Completed video playback for all URLs.")
    except Exception as e:
        print(f"Error starting video playback: {e}")
    finally:
        if os.path.exists("./urls.txt"):
            os.remove("./urls.txt")











while True:
    try:
        # Your existing code to execute the tasks
        check_cookies_working(cookies_file_path, "ahmad374.4755@gmail.com", "a516a87cfc")
        delete_already_watching_videos()

        get_bonus(cookies_file_path)

        get_links_1()
        asyncio.run(start_watching_videos())

        get_links_2()
        asyncio.run(start_watching_videos())

        get_links_3()
        asyncio.run(start_watching_videos())

        get_links_4()
        asyncio.run(start_watching_videos())

        get_links_5()
        asyncio.run(start_watching_videos())

        delete_already_watching_videos()
        get_links_6()
        asyncio.run(start_watching_videos())

    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C to stop the loop
        print("\nProgram interrupted by user. Exiting...")
        break  # Exit the loop
    except Exception as e:
        # Handle any other exceptions (optional)
        print(f"An error occurred: {e}")






