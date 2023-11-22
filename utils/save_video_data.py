import pandas as pd
from datetime import datetime


def save_data(list_of_dicts, user_tag):
    # Turn the data into a pandas DataFrame
    df = pd.DataFrame(list_of_dicts)
    
    # Create the filename using the user tag and the current date and time
    current_time = datetime.now()
    time_str = current_time.strftime("(%Y-%m-%d_%H.%M.%S)")
    file_name = f"reports/{time_str}{user_tag}.csv"
    
    # Save the DataFrame as a CSV file
    df.to_csv(file_name, index=False)


