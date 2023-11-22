import pandas as pd
import xlsxwriter.utility
from datetime import datetime


def analyze_data(list_of_dicts: list) -> pd.DataFrame:
    print("Analyzing data...")
    
    video_data = pd.DataFrame(list_of_dicts)
    
    # Create a new column for percent viewed that liked (round to 2 decimal places)
    video_data['percent viewed that liked'] = round(video_data['likes'] / video_data['views'], 4)
    
    # Create a new column for percent liked that favorited
    video_data['percent liked that favorited'] = round(video_data['favorites'] / video_data['likes'], 4)
    
    print("Finished analyzing data\n")
    
    return video_data


def get_file_name(user_tag: str) -> str:
    # Create the filename using the user tag and the current date and time
    current_time = datetime.now()
    time_str = current_time.strftime("(%Y-%m-%d_%H.%M.%S)")
    file_name = f"reports/{time_str}{user_tag}."
    
    return file_name


def save_data_to_csv(df: pd.DataFrame, user_tag: str) -> None:
    print("Saving data...")
    
    file_name = get_file_name(user_tag) + 'csv'
    
    # Save the DataFrame as a CSV file
    df.to_csv(file_name, index=False)
    
    print(f"Finished saving data to {file_name}\n")


def get_col_widths(dataframe):
    widths = []
    for col in dataframe.columns:
        # Length of the column header
        col_len = len(str(col))
        # Maximum length of data in the column
        max_data_len = max([len(str(val)) for val in dataframe[col]])
        # Choose the max between header length and data length
        max_len = max(col_len, max_data_len)
        # Append the maximum length
        widths.append(max_len)
    return widths


def save_data_to_xlsx(df: pd.DataFrame, user_tag: str,
                      remove_description: bool = True) -> None:
    print("Saving data...")
    
    file_name = get_file_name(user_tag) + 'xlsx'
    sheet_name = 'TikTok Video Data'
    links_column_width = 5
    
    
    # Remove the description column if specified
    if remove_description:
        df = df.drop(columns=['description'])
    
    
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    # Convert the DataFrame to an XlsxWriter Excel object
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    
    
    # Set the column widths
    column_widths = get_col_widths(df)
    for i, width in enumerate(column_widths):
        worksheet.set_column(i, i, width)
        if i == 0:
            # Manually set the width of the links column
            worksheet.set_column(i, i, links_column_width)
    
    
    # Apply conditional formatting to columns with numerical content
    for i, col in enumerate(df.columns):
        if pd.api.types.is_numeric_dtype(df[col]):
            # Excel column letter (A, B, C, ...)
            col_letter = xlsxwriter.utility.xl_col_to_name(i)
            
            # Define the Excel range to apply the formatting
            excel_range = f'{col_letter}2:{col_letter}{len(df) + 1}'  # +1 for header row

            # Apply the conditional formatting
            worksheet.conditional_format(excel_range, {'type': '3_color_scale',
                                                    'min_color': "#e67c73",  # Red
                                                    'mid_color': "#ffd666",  # Yellow
                                                    'max_color': "#57bb8a"}) # Green
            
            if 'percent' in col:
                # Apply the percent formatting
                worksheet.set_column(i, i, column_widths[i], workbook.add_format({'num_format': '0.00%'})) # type: ignore
    
    
    
    
    
    # # Set number format for percent columns
    # percent_format = workbook.add_format({'num_format': '0.00%'})

    # # Apply the format to the percent columns
    # for column in df.columns:
    #     if 'percent' in column:
    #         col_idx = df.columns.get_loc(column) + 1 # Adjusting for Excel indexing
    #         worksheet.set_column(col_idx, col_idx, 12, percent_format) # 12 is a sample column width, adjust as needed

    
    
    
    
    # Close the Pandas Excel writer and output the Excel file
    writer.close()
    
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
    save_data_to_xlsx(sample_data, 'sample_data')
