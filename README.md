# tiktok_video_data

## TODO

- Exponential back-off on shaking. 
- Get all comments for a video?

## Known Bugs

- The description gets cuts off at the first occurence of a hashtag or tagged account.
- If a video has no title or description, the scraping for that video gets stuck in an endless loop since it waits for that info to load before moving on. 
- Automatically setting the width of each column in the report isn't perfect, as the font causes some letters (ex: m) to be much wider that other letters (ex: i or l). 
