from selenium import webdriver
from bs4 import BeautifulSoup


class Video:
    # HTML classes for scraping
    _HTML_CLASS = {
    'title' : 'tiktok-1tgwhqp-H1PhotoTitle eqrezik11',
    'description' : 'tiktok-j2a19r-SpanText efbd9f0',
    'like_comment_favorite' : 'tiktok-1l70c6-StrongText edu4zum2'
    }
    
    def __init__(self, link: str, views: int = 0):
        '''
        Creates a Video object with a link and number of views,
        both of which are gotton from the profile page (they're not on the video page).
        '''
        
        self.data: dict = {
            'link' : link,
            'title' : '',
            'description' : '',
            'num views' : views,
            'num likes' : 0,
            'num comments' : 0,
            'num favorites' : 0,
        }
    
    
    def scrape_info(self, do_log: bool = False) -> None:
        '''
        Scrapes the video page for it's info.
        '''
        
        if do_log: print(f"Scraping video: {self.data['link']}")
        
        # Set up the browser
        driver = webdriver.Chrome()
        driver.get(self.data['link'])
        
        # Wait for the page to load
        # Detected by the presence of each of the info sections
        if do_log: print("Waiting for page to load...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        section_title = soup.find('h1', class_=self._HTML_CLASS['title'])
        section_description = soup.find('span', class_=self._HTML_CLASS['description'])
        section_likes_comments_favorites = soup.find_all('strong', class_=self._HTML_CLASS['like_comment_favorite'])
        while section_title is None or section_description is None or section_likes_comments_favorites is None:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            section_title = soup.find('h1', class_=self._HTML_CLASS['title'])
            section_description = soup.find('span', class_=self._HTML_CLASS['description'])
            section_likes_comments_favorites = soup.find_all('strong', class_=self._HTML_CLASS['like_comment_favorite'])
        
        if do_log: print("Page loaded.")
        
        self.data['title'] = section_title.text
        self.data['description'] = section_description.text.replace('\xa0', ' ')
        self.data['num likes'] = int(section_likes_comments_favorites[0].text)
        self.data['num comments'] = int(section_likes_comments_favorites[1].text)
        self.data['num favorites'] = int(section_likes_comments_favorites[2].text)
        
        if do_log:
            print("Scraped video info:")
            for key in self.data:
                print(f"{key}: {self.data[key]}")
        
        if do_log: print("Finished scraping video.\n")
        
        # Close the browser
        driver.close()