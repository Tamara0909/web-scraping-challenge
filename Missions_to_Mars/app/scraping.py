from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser)
    }

    browser.quit()
    return data


def mars_news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    news_title = slide_elem.find('div', class_='content_title').get_text()

    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    return news_title, news_p


def featured_image(browser):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    image_elem = browser.find_by_tag('button')[1]
    image_elem.click()
    img_soup = soup(browser.html, 'html.parser')

    img_url = img_soup.find('img', class_='fancybox-image').get('src')

    featured_image_url  = url + img_url

    return featured_image_url

def mars_facts():
    mars_facts = pd.read_html("https://galaxyfacts-mars.com/")[0]
    mars_facts.columns = ["Description", "Mars", "Earth"]
    mars_facts = mars_facts.set_index("Description")
    return mars_facts.to_html()


def hemispheres(browser):
    url = "https://marshemispheres.com/"
    browser.visit(url + 'index.html')
    hemisphere_image_urls = []

    links = browser.find_by_css('a.product-item img')

    for i in range(len(links)):
        hemi = {}
        
        browser.find_by_css('a.product-item img')[i].click()
        hemi_soup = soup(browser.html, "html.parser")
        
        hemi["title"] = hemi_soup.find("h2", class_="title").get_text()
        hemi["img_url"] = url + hemi_soup.find("a", text="Sample").get("href")

        
        hemisphere_image_urls.append(hemi)
        
        browser.back()

    return hemisphere_image_urls