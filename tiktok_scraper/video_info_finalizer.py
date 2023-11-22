from selenium import webdriver
from bs4 import BeautifulSoup
import time

from profile_scraper import get_all_video_links_with_views
from video_scraper import scrape_video


def load_bar(current: int, total: int, bar_length: int = 50) -> str:
    percent = current / total
    num_filled = int(percent * bar_length)
    num_empty = bar_length - num_filled
    return f"[{'#' * num_filled}{' ' * num_empty}] {int(percent * 100)}% ({current}/{total})"


def get_info_from_all_videos(user_tag: str = '@aimusicpainter') -> list:
    all_info_from_all_videos: list = []
    
    # Process each video from the profile
    print(f"Processing videos from {user_tag}")
    video_links_and_views = get_all_video_links_with_views(user_tag)
    video_links = [link_and_views[0] for link_and_views in video_links_and_views]
    num_videos = len(video_links)
    print("Beginning individual video scraping process")
    for link, i in zip(video_links, range(num_videos)):
        print(load_bar(i, num_videos))
        all_info_from_all_videos.append(scrape_video(link))
    print(load_bar(num_videos, num_videos))
    print("Finished primary scraping process")
    
    # Get views
    print("Getting views")
    video_views = [link_and_views[1] for link_and_views in video_links_and_views]
    for i in range(num_videos):
        all_info_from_all_videos[i]['views'] = video_views[i]
    print("Finished getting views")
    
    print(f"Finished processing videos from {user_tag}\n")
    return all_info_from_all_videos

if __name__ == '__main__':
    all_data = get_info_from_all_videos()
    for video_info in all_data:
        print(video_info)