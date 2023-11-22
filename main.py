import time
from tiktok_scraper.video_info_finalizer import get_info_from_all_videos
from utils.save_video_data import analyze_data, save_data


USER_TAG = '@aimusicpainter'


start_time = time.time()

video_data = get_info_from_all_videos(USER_TAG)
video_data = analyze_data(video_data)
save_data(video_data, USER_TAG)

print(f"Finished in {time.time() - start_time} seconds")
