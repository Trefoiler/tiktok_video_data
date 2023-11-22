from selenium import webdriver
from bs4 import BeautifulSoup
import time


CLASS = {
    'video_section' : 'tiktok-wjuodt-DivVideoFeedV2 ecyq5ls0',
    'entire_video' : 'tiktok-x6y88p-DivItemContainerV2 e19c29qe8',
    'video_image' : 'tiktok-x6f6za-DivContainer-StyledDivContainerV2 eq741c50',
    'video_description' : 'tiktok-vi46v1-DivDesContainer eih2qak4',
    'video_link' : 'tiktok-1wrhn5c-AMetaCaptionLine eih2qak0',
}


# Get the number of videos on the page
def get_num_videos(html: str) -> int:
    soup = BeautifulSoup(html, 'html.parser')
    video_divs = soup.find_all('div', class_=CLASS['entire_video'])
    return len(video_divs)


# Load all videos on the page
def load_all_videos(driver: webdriver.Chrome,
                    initial_wait: int = 7,
                    scroll_wait: int = 3):
    time.sleep(initial_wait)
    
    num_scrolls = 0
    num_videos_pre_scroll = get_num_videos(driver.page_source)
    num_videos_post_scroll = 0
    
    print(f"Found {num_videos_pre_scroll} videos before scrolling")
    
    while num_videos_pre_scroll != num_videos_post_scroll:
        # Scroll to the bottom of the page to lead all videos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        num_scrolls += 1
        
        # Wait for the page to load
        time.sleep(scroll_wait)
        
        # Get the number of videos on the page
        num_videos_pre_scroll = num_videos_post_scroll
        num_videos_post_scroll = get_num_videos(driver.page_source)
        
        print(f"Found {num_videos_post_scroll} videos after {num_scrolls} scrolls")
    
    print(f"Loaded all {num_videos_post_scroll} videos after {num_scrolls} scrolls")


# Scrapes a TikTok profile for all video links
def get_all_video_links(user_tag: str = '@aimusicpainter') -> list:
    # Set up the browser
    driver = webdriver.Chrome()
    driver.get('https://www.tiktok.com/' + user_tag)
    
    # Load all videos
    load_all_videos(driver)
    
    # Get the HTML content of the full page
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get each tag with a video link
    video_link_tags = soup.find_all('a', class_=CLASS['video_link'])
    print(f"Found {len(video_link_tags)} video link tags")
    
    # Get each video link
    video_links = []
    for tag in video_link_tags:
        video_links.append(tag['href'])
    
    # Close the browser
    driver.close()
    
    return video_links


if __name__ == '__main__':
    video_links = get_all_video_links()
    print(video_links)