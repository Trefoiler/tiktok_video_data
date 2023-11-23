from typing import List
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import xlsxwriter.utility
import config
from utils.load_bar import load_bar
from tiktok_scraper.video import Video


class Profile:
    # HTML classes for scraping
    _HTML_CLASS = {
    'video_section' : 'tiktok-wjuodt-DivVideoFeedV2 ecyq5ls0',
    
    'entire_video' : 'tiktok-x6y88p-DivItemContainerV2 e19c29qe8',
    'video_image' : 'tiktok-x6f6za-DivContainer-StyledDivContainerV2 eq741c50',
    'video_description' : 'tiktok-vi46v1-DivDesContainer eih2qak4',
    
    'video_link' : 'tiktok-1wrhn5c-AMetaCaptionLine eih2qak0',
    'views' : 'video-count tiktok-dirst9-StrongVideoCount e148ts222'
    }
    
    
    def __init__(self, scrape_videos: bool = True):
        # tag of the user to scrape; set in config.py
        self.user_tag: str = config.USER_TAG
        # set up video list
        self.videos: list[Video] = self._set_up_videos()
        self.num_videos = len(self.videos)
        if scrape_videos:
            self._scrape_video_info()
    
    
    def _set_up_videos(self) -> list[Video]:
        '''
        Scrapes a TikTok profile,
        returning list of Video objects, each with the links and views.
        '''
        
        # Set up the browser
        driver = webdriver.Chrome()
        driver.get('https://www.tiktok.com/' + self.user_tag)
        
        # Wait for the page to load
        # Detected by the presence of the video section
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        while soup.find('div', class_=self._HTML_CLASS['video_section']) is None:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Load all videos
        Profile._load_all_videos(driver)
        
        # Get the final updated page source and close the browser
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        
        print("Scraping for video links and views...")
        
        # Get each tag with a video link
        print("Finding video link tags...")
        video_link_tags = soup.find_all('a', class_=Profile._HTML_CLASS['video_link'])
        print(f"Found {len(video_link_tags)} video link tags.")
        
        # Get the view count for each video
        print("Finding view counts...")
        video_view_tags = soup.find_all('strong', class_=Profile._HTML_CLASS['views'])
        print(f"Found {len(video_view_tags)} view count tags.")
        
        # Ensure the number of video links and view counts are the same
        if len(video_link_tags) != len(video_view_tags):
            raise Exception("Number of video links and view counts are not the same.")
        num_videos = len(video_link_tags)
        
        # Ensure the number of videos is not greater than the max
        if num_videos > config.MAX_VIDEOS:
            print(f"Number of videos ({num_videos}) is greater than the max ({config.MAX_VIDEOS}).")
            print(f"Only using the first {config.MAX_VIDEOS} videos.")
            num_videos = config.MAX_VIDEOS
            video_link_tags = video_link_tags[:config.MAX_VIDEOS]
            video_view_tags = video_view_tags[:config.MAX_VIDEOS]
        
        print("Finished scraping for video links and views.\n")
        
        # Create the list of videos using the links and view counts
        print("Creating list of Video objects...")
        videos: List[Video] = []
        for link_tag, view_tag in zip(video_link_tags, video_view_tags):
            videos.append(Video(link_tag['href'], int(view_tag.text)))
        
        print("Finished creating list of Video objects.\n")
        
        return videos
    
    
    @staticmethod
    def _get_num_videos(html: str) -> int:
        '''
        Gets the number of videos on a page.
        '''
        soup = BeautifulSoup(html, 'html.parser')
        video_divs = soup.find_all('div', class_=Profile._HTML_CLASS['entire_video'])
        return len(video_divs)
    
    
    @classmethod
    def _load_all_videos(cls, driver: webdriver.Chrome):
        '''
        Loads all videos on the page.        
        '''
        print("Loading all videos...")
        
        # Stores the time when the last new video was found
        last_time_of_increase_in_videos = time.time()
        
        # Get the initial number of videos on the page
        last_num_videos = cls._get_num_videos(driver.page_source)
        num_videos = last_num_videos
        print(f"Found {num_videos} videos before scrolling.")
        
        # Scroll to the bottom of the page, constnatly checking for new videos. 
        # Stops scrolling when no new videos are found for MAX_SCROLL_WAIT_TIME seconds. 
        while (time.time() - last_time_of_increase_in_videos) < config.MAX_SCROLL_WAIT_TIME:
            # Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Scroll back up a tiny bit because sometimes it doesn't detect you're at the bottom
            driver.execute_script("window.scrollBy(0, -10);")
            
            # Get the number of videos on the page
            last_num_videos = num_videos
            num_videos = cls._get_num_videos(driver.page_source)
            
            # If the number of videos is already the max, stop scrolling
            if num_videos == config.MAX_VIDEOS:
                print('Stopped scrolling because the max number of videos was reached.')
                break
            
            # If new videos were found, reset the timer
            if num_videos > last_num_videos:
                last_time_of_increase_in_videos = time.time()
        
        print(f"Found {num_videos} videos total.\n")
    
    
    def _scrape_video_info(self) -> None:
        '''
        Scrapes the info for each video in self.videos.
        '''
        print("Scraping each video's info...")
        
        for vid_index in range(self.num_videos):
            print(load_bar(vid_index, self.num_videos, 50))
            self.videos[vid_index].scrape_info()
            
        print(load_bar(self.num_videos, self.num_videos, 50))
        print("Finished scraping each video's info.\n")
    
    
    def _video_data_to_df(self) -> pd.DataFrame:
        '''
        Converts the video data to a DataFrame.
        '''
        
        data_from_all_videos: list[dict] = []
        for video in self.videos:
            data_from_all_videos.append(video.data)
        
        return pd.DataFrame(data_from_all_videos)
    
    
    def _get_output_file_name(self) -> str:
        '''
        Gets the file name for the report.
        '''
        
        # Create the filename using the user tag and the current date and time
        current_time = datetime.now()
        time_str = current_time.strftime("(%Y-%m-%d_%H.%M.%S)")
        file_name = f"reports/{time_str}{self.user_tag}.xlsx"
        
        return file_name
    
    
    @staticmethod
    def _get_col_widths(df: pd.DataFrame) -> list[int]:
        '''
        Gets the column widths for the report.
        '''
        
        widths = []
        for col in df.columns:
            # Check if the column has a custom width
            if col in config.CUSTOM_COLUMN_WIDTHS:
                if config.CUSTOM_COLUMN_WIDTHS[col] is not None:
                    # Use the custom width
                    widths.append(config.CUSTOM_COLUMN_WIDTHS[col])
                    continue
            
            # Length of the column header
            col_len = len(str(col))
            # Maximum length of data in the column
            max_data_len = max([len(str(val)) for val in df[col]])
            # Choose the max between header length and data length
            max_len = max(col_len, max_data_len)
            # Append the maximum length
            widths.append(max_len)
        
        return widths

    
    
    def save_data_to_xlsx(self) -> None:
        '''
        Saves the video data to an Excel file.
        '''
        print("Saving data...")
        
        # Save the video data to a dataframe
        video_data: pd.DataFrame = self._video_data_to_df()
        
        # Analyze the data
        print("Analyzing data...")        
        video_data['percent viewed that liked'] = round(video_data['num likes'] / video_data['num views'], 4)
        video_data['percent liked that favorited'] = round(video_data['num favorites'] / video_data['num likes'], 4)
        print("Finished analyzing data")
        
        # Remove the sections specified in the config file
        print("Removing excluded sections...")
        for section in config.EXCLUDED_VIDEO_DATA:
            print(f"Removing section: {section}")
            video_data = video_data.drop(section, axis=1)
        print("Finished removing excluded sections.")
        
        
        # Get the file name and sheet name
        output_file: str = self._get_output_file_name()
        sheet_name = 'Video Data'
        
        # Create a Pandas Excel writer using XlsxWriter as the engine
        writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
        # Convert the DataFrame to an XlsxWriter Excel object
        video_data.to_excel(writer, sheet_name=sheet_name, index=False)
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        
        # Set the column widths
        print("Setting column widths...")
        column_widths = Profile._get_col_widths(video_data)
        for i, width in enumerate(column_widths):
            worksheet.set_column(i, i, width)
        print("Finished setting column widths.")
        
        # Apply conditional formatting to columns with numerical content
        print("Applying conditional formatting...")
        for i, col in enumerate(video_data.columns):
            if pd.api.types.is_numeric_dtype(video_data[col]):
                # Excel column letter (A, B, C, ...)
                col_letter = xlsxwriter.utility.xl_col_to_name(i)
                
                # Define the Excel range to apply the formatting
                excel_range = f'{col_letter}2:{col_letter}{len(video_data) + 1}'  # +1 for header row

                # Apply the conditional formatting
                worksheet.conditional_format(excel_range, {'type': '3_color_scale',
                                                        'min_color': "#e67c73",  # Red
                                                        'mid_color': "#ffd666",  # Yellow
                                                        'max_color': "#57bb8a"}) # Green
                
                # Apply the percent formatting to columns with 'percent' in the name
                if 'percent' in col.lower():
                    # Apply the percent formatting
                    worksheet.set_column(i, i, column_widths[i], workbook.add_format({'num_format': '0.00%'})) # type: ignore
        print("Finished applying conditional formatting.")
        
        # Close the Pandas Excel writer and output the Excel file
        writer.close()
        
        print(f"Finished saving data to {output_file}\n")
