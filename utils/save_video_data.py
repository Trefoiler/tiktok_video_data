import pandas as pd
from datetime import datetime


def analyze_data(list_of_dicts: list) -> pd.DataFrame:
    print("Analyzing data...")
    
    video_data = pd.DataFrame(list_of_dicts)
    
    # Create a new column for percent viewed that liked
    video_data['percent viewed that liked'] = video_data['likes'] / video_data['views']
    
    # Create a new column for percent liked that favorited
    video_data['percent liked that favorited'] = video_data['favorites'] / video_data['likes']
    
    print("Finished analyzing data\n")
    
    return video_data


def save_data_to_csv(dataframe: pd.DataFrame, user_tag: str) -> None:
    print("Saving data...")
    
    # Create the filename using the user tag and the current date and time
    current_time = datetime.now()
    time_str = current_time.strftime("(%Y-%m-%d_%H.%M.%S)")
    file_name = f"reports/{time_str}{user_tag}.csv"
    
    # Save the DataFrame as a CSV file
    dataframe.to_csv(file_name, index=False)
    
    print(f"Finished saving data to {file_name}\n")


if __name__ == '__main__':
    # Create a very list of dictionaries to use as a sample DataFrame
    # Has a link, title, description, views, likes, comments, favorites, 
    # percent viewed that liked, and percent liked that favorited
    sample_data = [
        {
            'link': 'https://www.tiktok.com/@aimusicpainter/video/7303004908452728095',
            'title': 'Can You Hear the Moon',
            'description': 'AI generated images of Can You Hear the Moon by Grady ',
            'views': 654,
            'likes': 32,
            'comments': 5,
            'favorites': 2
        },
        {
            'link': 'https://www.tiktok.com/@aimusicpainter/video/7303010234757418270',
            'title': 'Ashes',
            'description': 'AI generated images of Ashes by Stellar ',
            'views': 679,
            'likes': 32,
            'comments': 2,
            'favorites': 1
        },
        {
            'link': 'https://www.tiktok.com/@aimusicpainter/video/7303045128086637855',
            'title': 'Walking On A Dream',
            'description': 'AI generated images of Walking On A Dream by Empire of the Sun ',
            'views': 1638,
            'likes': 106,
            'comments': 3,
            'favorites': 6
        }
    ]
    
    sample_data = analyze_data(sample_data)
    save_data_to_csv(sample_data, 'sample_data')