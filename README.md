# tiktok_video_data

## Possible Improvements

- Add a max videos to grab variable to the config file

### `tiktok_scraper/profile.py`

- Make it get the full description. 
- Only count comments that aren't the creator. 

## Known Bugs

- The description gets cuts off at the first occurence of a hashtag or tagged account.
- If a video has no title or description, the scraping for that video gets stuck in an endless loop since it waits for that info to load before moving on. 
