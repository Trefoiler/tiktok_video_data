from tiktok_scraper.video_info_finalizer import get_info_from_all_videos
from utils.save_video_data import save_data

USER_TAG = '@aimusicpainter'

all_data = get_info_from_all_videos(USER_TAG)
save_data(all_data, USER_TAG)