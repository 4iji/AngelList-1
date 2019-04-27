import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_text_from_element(driver, _xpath):
    try:
        content = driver.find_element_by_xpath(_xpath)
        content = content.get_attribute('innerText')
        content = content.replace(',', '')
    except:
        content = None
    return content


def get_text_from_elements(driver, _xpath):
    content = ''
    try:
        elements = driver.find_elements_by_xpath(_xpath)
        for element in elements:
            text = element.get_attribute('innerText')
            text = text.replace(',', '')
            content += text + ' '
    except:
        content = None
    return content


def get_url_from_element(driver, _xpath):
    try:
        url = driver.find_element_by_xpath(_xpath)
        url = url.get_attribute('href')
    except:
        url = None
    return url


def parse_page(page):
    print(page)

    chrome_options = Options()

    # chrome_options.add_argument(f'--proxy-server=socks5://157.230.58.198:80')

    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(executable_path="driver/chromedriver", chrome_options=chrome_options)

    driver.get(page)
    time.sleep(20)

    try:
        driver.find_element_by_xpath('//div[@class="content"]/a[@class="hidden_more"]').click()
    except:
        pass

    website = get_url_from_element(driver, '//span[@class="link s-vgRight0_5"]/a[@class="u-uncoloredLink company_url"]')
    company_name = get_text_from_element(driver, '//h1[@class="u-fontWeight500 s-vgBottom0_5"]')
    location = get_text_from_element(driver, '//span[@class="js-location_tags"]/a')

    description = get_text_from_element(driver,
                                        '//div[@class="product_desc editable_region"]/div/div[@class="content"]')
    if description:
        description = description.replace('\n', ' ').strip()

    joined = get_text_from_element(driver, '//div[@class="date_display"]')
    market = get_text_from_element(driver, '//span[@class="js-market_tags"]/a')
    employees = get_text_from_element(driver, '//span[@class="js-company_size"]')
    stage = get_text_from_element(driver, '//div[@class="type"]')
    total_raised = get_text_from_element(driver, '//div[@class="raised"]')
    twitter_link = get_url_from_element(driver, '//a[@class="fontello-twitter u-uncoloredLink twitter_url"]')
    facebook_link = get_url_from_element(driver, '//a[@class="fontello-facebook u-uncoloredLink facebook_url"]')
    instagram_link = get_url_from_element(driver, '//a[@class="fontello-linkedin u-uncoloredLink linkedin_url"]')
    investors = get_text_from_elements(driver,
                                       '//h4[@data-tips_selector="past_investors_section"]/following-sibling::div[@class="group"][1]//div[@class="name"]')
    advisors = get_text_from_elements(driver,
                                      '//h4[@data-tips_selector="advisors_section"]/following-sibling::div[@class="group"][1]//div[@class="name"]')
    incubators = get_text_from_elements(driver,
                                        '//h4[contains(text(),"Incubator")]/following-sibling::div[@class="group"][1]//div[@class="name"]')

    try:
        founder_1_name = driver.find_elements_by_xpath(driver, '//div[@class="founders section"]//div[@class="name"]')[
            0].text
    except:
        founder_1_name = None

    try:
        founder_2_name = get_text_from_elements(driver, '//div[@class="founders section"]//div[@class="name"]')[1].text
    except:
        founder_2_name = None
    try:
        founder_1_link = get_text_from_elements(driver, '//div[@class="founders section"]//div[@class="name"]')[1]
        founder_1_link = founder_1_link.get_attribute('href')
    except:
        founder_1_link = None

    with open('results.csv', mode='a') as csv_file:
        csv_file.write(f'{company_name},{website}'
                       f', , ,{joined},'
                       f'{location},{market},{employees},{stage}'
                       f',{total_raised},{market},{twitter_link},'
                       f'{facebook_link},{instagram_link},{founder_1_name}'
                       f',{founder_1_link},{founder_2_name},{investors},{incubators},{advisors},{description}\n')

    driver.close()


if __name__ == '__main__':

    company_urls = open('10712-Saudi_Arabia.txt', 'r').readlines()
    company_urls = list(set(company_urls))

    i = 0
    for company_url in company_urls:
        i += 1
        print(i)
        parse_page(company_url)
