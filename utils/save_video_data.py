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


def save_data(dataframe: pd.DataFrame, user_tag: str) -> None:
    print("Saving data...")
    
    # Create the filename using the user tag and the current date and time
    current_time = datetime.now()
    time_str = current_time.strftime("(%Y-%m-%d_%H.%M.%S)")
    file_name = f"reports/{time_str}{user_tag}.csv"
    
    # Save the DataFrame as a CSV file
    dataframe.to_csv(file_name, index=False)
    
    print(f"Finished saving data to {file_name}\n")


