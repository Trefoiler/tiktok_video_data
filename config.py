'''
CONFIGURATION FILE
'''


'''
User tag for the TikTok profile to scrape.
Format: '@username' (example: '@aimusicpainter') 
'''
USER_TAG: str = '@aimusicpainter'

'''
The maximum number of videos to scrape from the profile.
'''
MAX_VIDEOS: int = 50

'''
When scrolling to load videos on a profile,
the max allowble time to wait for videos to load after scrolling.
'''
MAX_SCROLL_WAIT_TIME: int = 3 # seconds

'''
A list of what video data exclude from the final report.
Leave empty to include all data.
Possible choices:
- 'link'
- 'title'
- 'description'
- 'num views'
- 'num likes'
- 'num comments'
- 'num favorites'
- 'percent viewed that liked'
- 'percent liked that favorited'
'''
EXCLUDED_VIDEO_DATA: list = ['description']

'''
Dictionary of what video data columns to give a custom width in the final report.
'''
CUSTOM_COLUMN_WIDTHS: dict = {
    'link': 5,
    'title': None,
    'description': None,
    'num views': None,
    'num likes': None,
    'num comments': None,
    'num favorites': None,
    'percent viewed that liked': None,
    'percent liked that favorited': None
}
