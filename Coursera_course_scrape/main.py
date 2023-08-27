from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import json

def get_courses(path):

    # data dictionary
    data = {}
    # Time of Start of Code
    start = time.time()


    data['courses'] = list()

    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")

    page = 1
    url = f'https://www.coursera.org/search?query=python&page={page}&index=prod_all_products_term_optimization'

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # Open the website in the chromedriver
        driver.get(url)
        time.sleep(10)

        try:
            course_class = driver.find_elements(By.XPATH,'//ul[@class="cds-9 css-18msmec cds-10"]/li')
            # print("hello")
            # print("class",course_class)
        except Exception as e:
            print(f'course_class error: {e}')

        num = len(course_class)
        count = 0

        for item in course_class:


            try:
                course_name = item.find_element(By.XPATH ,'./div//a').text
                full_data = course_name.split("\n")
                print(course_name)
            except Exception as e:
                print(f'course_name error: {e}')
            

            try:
                data['courses'].append(
                    {
                        'Name': full_data[1],
                        'Provider' : full_data[0],
                        'Skills':full_data[2],
                        'Time_to_complete' : full_data[5],
                        'Rating': full_data[3],
                        'Reviews' : full_data[4]

                        
                    }
                )
            except:
                pass

            count += 1
            print(f'{count}/{num} scraped')

            seconds = time.time() - start
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            print("\t%d:%02d:%02d" % (h, m, s))
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    except Exception as e:
        print(f'driver.get error:\n {e} , {full_data[1]}')

    try:
        with open('data.json', 'w' , encoding='utf-8') as f:
            json.dump(data, f , indent=4)
    except Exception as e:
        print(f'Data Dumping Error: {e}')

    driver.quit()

get_courses('../chromedriver_linux/chromedriver')