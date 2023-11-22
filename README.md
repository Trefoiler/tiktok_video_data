# tiktok_video_data

## Possible Improvements

- Make a config file for things such as profile tag, wait times, etc.
- Format the output file better
    - bold titles
    - change width of columns
    - make percents appear as percents
    - add conditional formatting to numerical values

### `tiktok_scraper/profile_scraper.py`

- Get rid of the initial wait for `load_all_videos` and make it start scrolling once videos have initially loaded. 
- Add a way to increase the wait times in `load_all_videos` from `get_all_video_links`.

### `tiktok_scraper/video_scraper.py`

- Get rid of the wait time and make it just get the data once it's available. 
- Make it get the full description. 
- Only count comments that aren't the creator. 
