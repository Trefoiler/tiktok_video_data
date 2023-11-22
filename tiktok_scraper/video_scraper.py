from selenium import webdriver
from bs4 import BeautifulSoup
import time


CLASS = {
    'title' : 'tiktok-1tgwhqp-H1PhotoTitle eqrezik11',
    'description' : 'tiktok-j2a19r-SpanText efbd9f0',
    'like_comment_favorite' : 'tiktok-1l70c6-StrongText edu4zum2'
}

# Scrapes a TikTok video for it's information
def scrape_video(link: str) -> dict:
    video_info = {
        'link' : link,
        'title' : '',
        'description' : '', # cuts off at first tag or hashtag
        'views' : 0, # placeholder; will be aquired in info_organizer.py
        'likes' : 0,
        'comments' : 0,
        'favorites' : 0,
    }
    
    # Set up the browser
    driver = webdriver.Chrome()
    driver.get(link)
    
    # Wait for the page to load
    time.sleep(2)
    
    # Get the HTML content of the full page
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Close the browser
    driver.close()
    
    # Get title and description
    video_info['title'] = soup.find_all('h1', class_=CLASS['title'])[0].text
    description = soup.find_all('span', class_=CLASS['description'])[0].text
    video_info['description'] = description.replace('\xa0', ' ')
    
    # Get likes, comments, and favorites
    likes_comments_favorites = soup.find_all('strong', class_=CLASS['like_comment_favorite'])
    video_info['likes'] = int(likes_comments_favorites[0].text)
    video_info['comments'] = int(likes_comments_favorites[1].text)
    video_info['favorites'] = int(likes_comments_favorites[2].text)
    
    return video_info


if __name__ == '__main__':
    video_info = scrape_video('https://www.tiktok.com/@aimusicpainter/video/7304113946313706783')
    for key in video_info:
        print(f"{key}: {video_info[key]}")
