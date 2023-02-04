import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
         'new york city': 'new_york_city.csv',
         'washington': 'washington.csv'}
print('Launching.....') 
def check(its_string,its_type):
    """
    Checks if the input is matching the elements in the lists
    its_string: refers to the input
    its_type: refers to the input number
    """
    #A while loop to check validity of the input
    while True:
        read = input(its_string)
        try:
            if read.lower() in CITY_DATA.keys() and its_type == 1:
                break
            elif read.lower() in ['january', 'february', 'march', 'april', 'may', 'june','all'] and its_type == 2:
                break
            elif read.lower() in ['saturday','sunday','monday','tuesday','wednesday','thursday','friday', 'all'] and its_type == 3:
                break
            else:
                if its_type == 1:
                    print('please choose a valid city from the list: chicago, new york city, washington')
                if its_type == 2:
                    print('please choose a valid month, january.....june')
                if its_type == 3:
                    print('please choose a valid day, saturday......friday')
        except ValueError:
            print('Please try again with a valid input!')
    return read.lower()
def filters():
    """
    Collects data from the user and assigns it in the program
    City: City name
    mm: Month
    dd: Day
    """
    #program's welcome.
    print('Hello! Let\'s explore some US bikeshare data!')
    #collects user input for city name.
    city = check('Chicago, New York City, Washington: ',1)
    #collects user input for month.
    mm = check('Choose month, january.....june or all: ',2)
    #collects user input for day.
    dd = check('Choose day, saturday.....friday or all: ',3)
    print('=========================================================================')
    #returns data into it's variables
    return city,mm ,dd
def load(city,mm,dd):
    """
    Loads the data into data frames to analyze it
    """
    print('loading information....')
    #loads data into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    #splits Start Time column into a separated dataframe
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #converts Start Time dataframe into months
    df['month'] = df['Start Time'].dt.month
    #converts Start Time dataframe into days
    df['weekday_name'] = df['Start Time'].dt.weekday_name
    #converts Start Time dataframe into hours
    df['hour'] = df['Start Time'].dt.hour
    #filter months
    if mm != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        mm = months.index(mm) +1
        df = df[df['month']== mm]      
    #filter days
    if dd != 'all':
          df = df[df['weekday_name']== dd.title()]
    print('=========================================================================')
    return df 
def time_stats(df):
    """
    Displays time stats for each month, day, and hour.
    """
    print('Calculating time stats.....')
    #calcualting most popular month with a condition of passing errors
    most_popular_month = df['month'].mode()[0] if len(df['month'].mode()) > 0 else None
    print('Most popular month: ', most_popular_month)
    #calculating most popular day with a condition of passing errors
    most_popular_day = df['weekday_name'].mode()[0] if len(df['weekday_name'].mode()) > 0 else None
    print('Most popular day: ', most_popular_day)
    #calculating most popular hour with a condition of passing errors
    most_popular_hour = df['hour'].mode()[0] if len(df['hour'].mode()) > 0 else None
    print('Most common start hour: ', most_popular_hour)
    print('Time stats calculated successfully.')
    print('=========================================================================')         
def station(df):
    """
    Displays most popular Start and End Stations.
    """
    print('Searching for stations information....')
    #checks if Start Station is in the columns of the dataframe
    if 'Start Station' in df.columns:
        #this is to verify that Start Station contains elements to prevent it from causing an error
        if len(df['Start Station'].mode()) > 0:
            popular_start_station = df['Start Station'].mode()[0]
        else:
            popular_start_station = None
        print('Most popular start station: ', popular_start_station)
    else:
        print('Column First Station not found in dataframe')
    #checks if End Station is in the columns of the dataframe
    if 'End Station' in df.columns:
        #this is to verify that End Station contains elements to prevent it from causing an error
        if len(df['End Station'].mode()) > 0:
            popular_end_station = df['End Station'].mode()[0]
        else:
            popular_end_station = None
        print('Most popular end station: ', popular_end_station)
    else:
        print('Column Last Station not found in dataframe')

    collect_stations = df.groupby(['Start Station', 'End Station'])
    print(collect_stations)
    popular_collected_stations = collect_stations.size().sort_values(ascending=False).head(1) if len(collect_stations) > 0 else None
    print('Most popular Start and End stations combined:\n', popular_collected_stations)
    print('Stations information collected successfully.')
    print('=========================================================================')         

def trip(df):
    """
    Displays trip duration stats.
    """
    print('Computing trip duration....')
    #checks if Trip Duration is in the columns of the dataframe
    if 'Trip Duration' in df.columns:
        #calculates total travelled time
        total_travelled = df['Trip Duration'].sum()
        print("Total travelled: ", total_travelled)
    else:
        print('Column Duration not found in dataframe')
        #calculates mean travel time
    mean_travelled = df['Trip Duration'].mean() if df['Trip Duration'].mean() > 0 else None
    print('Mean travelled : ', mean_travelled)
    print('Trip duration computed successfully.')
    print('=========================================================================')     
def user_stats(df,city):
    """
    Displays user stats: Gender, Birth Years, User Types.
    """
    print('Collecting user stats.....')
    print('User Type Stats:')
    print(df['User Type'].value_counts())
    #collcets user data
    if city != 'washington':
        print('Gender Stats:')
        #collects gender stats from the dataframe
        print(df['Gender'].value_counts())
        print('Birth Stats:')
        #collects the most common birth year from the dataframe
        common_year = df['Birth Year'].mode()[0]
        print('Common Year:',common_year)
        #collects the most recent birth year from the dataframe
        recent_year = df['Birth Year'].max()
        print('Recent Year:',recent_year)
        #collects the earliest birth year from the dataframe
        earliest_year = df['Birth Year'].min()
        print('Earliest Year:',earliest_year)
    print('User stats collected successfully.')     
    print('=========================================================================')
    print('Operations completed.')
def main():
    """
    Arranging operations.
    """
    while True:
        city,mm,dd = filters()
        
        time_stats(df)
        station(df)
        trip(df)
        user_stats(df,city)
        display_five = input('\n do you want to show five lines of raw data? yes, no\n')
        if display_five.lower() == 'yes':
            print(df.iloc[0:5])
        display = input('\ndo you want to see all details? yes, no\n')
        #displays five lines of raw data for each iteration
        if display.lower() == 'yes':
            for line in df:
                print(df.iloc[0:5])
        #restarts the program
        restart = input('\nrestart the program? yes, no\n')
        if restart.lower() != 'yes':
            break           
if __name__ == "__main__":
    main()