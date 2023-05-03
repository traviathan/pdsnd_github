import time as time
import pandas as pd
import numpy as np


def getCity():
    """Prompt the user to select a city
    INPUT: None
    DEPENDENCIES: None
    OUTPUT: str. The city name.
    """
    cities = ['Chicago', 'New York City', 'Washington']
    
    print('Cities:')
    for city in cities:
        print('|-', city)

    choice = None
    valid_choice = None

    while valid_choice != True:
        try:
            choice = input("\nEnter the name of the city:\n").title()
            if choice in cities:
                valid_choice = True
                print(f'You chose {choice}.')
            else:
                raise
        except:
            print(f'You chose {choice}.')
            valid_choice = False
            print('Hmm... Try again.')

    return cities.index(choice)


def getMonth():
    """Prompt the user to select a month.
    INPUT: None
    DEPENDENCIES: None
    OUTPUT: int. The index of the month.
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    print('Choose a month from the list:')
    for month in months:
        print('|-', month)

    choice = None
    valid_choice = None

    while valid_choice != True:
        try:
            choice = input("\nEnter the name of the month:\n").title()
            if choice in months:
                valid_choice = True
                print(f'You chose {choice}.')
            else:
                raise
        except:
            valid_choice = False
            print('Hmm... Try again.')

    return months.index(choice)


def getDayOfWeek():
    """Prompt the user to select a day of the week.
    INPUT: None
    DEPENDENCIES: None
    OUTPUT: int. The index of the day of the week.
    """
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    print('Choose a day of the week from the list:')
    for day in days_of_week:
        print('|-', day)

    choice = None
    valid_choice = None

    while valid_choice != True:
        try:
            choice = input("\nEnter the day of the week:\n").title()
            if choice in days_of_week:
                valid_choice = True
                print(f'You chose {choice}.')
            else:
                raise
        except:
            valid_choice = False
            print('Hmm... Try again.')

    return days_of_week.index(choice)


def loadData(city='All'):
    """Load the Bikeshare data from csv.
    INPUT:
    - city: str. The city name.
    DEPENDENCIES:
    -external CSV files
    OUTPUT:
    - dataframe with specified city filter.
    """
    if city == 'Chicago':
        return pd.read_csv("chicago.csv")
    elif city == 'New York City':
        return pd.read_csv("new_york_city.csv")
    elif city == 'Washington':
        df = pd.read_csv("washington.csv")
        df['Gender'] = float("NaN")
        df['Birth Year'] = float('NaN')
        return df
    else:
        df_chicago = pd.read_csv("chicago.csv")
        df_chicago['City'] = 'Chicago'
        df_nyc = pd.read_csv("new_york_city.csv")
        df_nyc['City'] = 'New York City'
        df_washington = pd.read_csv("washington.csv")
        df_washington['City'] = 'Washington'
        return pd.concat([df_chicago, df_nyc, df_washington], sort=False)


def filterCity():
    """Prompts user to filter by city.
    INPUT: None
    DEPENDENCIES:
    - loadData()
    - getCity(): Prompts user to select a city for filtering.
    OUTPUT:
    - dataframe filtered by city
    """
    cityFilter = input('Would you like to see the data filtered by city? (Y/N)\n')
    if cityFilter.upper() == 'N':
        print('Loading data for all cities...')
        df = loadData()
    elif cityFilter.upper() == 'Y':
        print('Let\'s pick our city filter!')
        df = loadData(getCity())
    else:
        print('Invalid choice. Try again...')
        filterCity()
    
    print('-'*40)
    return df

def filterMonth(dataframe):
    """Prompts user to filter by month.
    INPUT: dataframe
    DEPENDENCIES:
    - getMonth(): Prompts user to select a month for filtering.
    OUTPUT:
    - dataframe filtered by month.
    """
    monthFilter = input('Would you like to see the data filtered by month? (Y/N)\n')
    
    dataframe['Start Time'] = pd.to_datetime(dataframe['Start Time'])
    dataframe['month'] = dataframe['Start Time'].dt.month
    dataframe['day of week'] = dataframe['Start Time'].dt.dayofweek
    dataframe['hour'] = dataframe['Start Time'].dt.hour
    
    if monthFilter.upper() == 'N':
        print('Filter not applied.')
        df = dataframe
        print('-'*40)
        return df
    elif monthFilter.upper() == 'Y':
        monthChoice = getMonth()
        df = dataframe.loc[dataframe['month'] == monthChoice + 1]
        print('-'*40)
        return df
    else:
        print('Invalid choice. Try again...')
        filterMonth(dataframe)
    
    print('-'*40)
    return df


def filterDayOfWeek(dataframe):
    """Prompts user to filter by day of the week.
    INPUT: dataframe
    DEPENDENCIES:
    - getDaysOfWeek(): Prompts user to select a day of the week for filtering.
    OUTPUT:
    - dataframe filtered by day of the week.
    """
    dayFilter = input('Would you like to see the data filtered by day of the week? (Y/N)\n')
    
    if dayFilter.upper() == 'N':
        print('Filter not applied.')
        df = dataframe
        return df
    elif dayFilter.upper() == 'Y':
        dayChoice = getDayOfWeek()
        df = dataframe.loc[dataframe['day of week'] == dayChoice]
        return df
    else:
        print('Invalid choice. Try again...')
        filterDayOfWeek(dataframe)
    
    print('-'*40)
    return df


def getDataSet():
    """Initiates all prompts for loading and filtering data.
    INPUT: None
    DEPENDENCIES:
    - filterCity(): Prompts user to filter by city.
    - filterMonth(): Prompts user to filter by month.
    - filterDayofWeek: Prompts user to filter by day of the week.
    OUTPUT:
    - dataframe. Total data based on user's filtering.
    """
    city = filterCity()
    month = filterMonth(city)
    df = filterDayOfWeek(month)

    if df.empty:
        print('-'*40)
        print('There is no data for the period you selected.')
        return
    else:
        return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    print('-'*40)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = int(df.mode()['month'][0])
    print(f'Most common month: {months[most_common_month-1]}')

    # display the most common day of week
    most_common_day = int(df.mode()['day of week'][0])
    print(f'Most common day: {days_of_week[most_common_day]}')

    # display the most common start hour
    most_common_hour = int(df.mode()['hour'][0])
    print(f'Most common hour: {most_common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    print(df.head(20))
    print(df['month'].unique())


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = max(df.groupby(['Start Station']))
    print(f'Most common start station: {most_common_start[0]}')

    # display most commonly used end station
    most_common_end = max(df.groupby(['End Station']))
    print(f'Most common end station: {most_common_end[0]}')

    # display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station'] + '-' + df['End Station']
    most_common_both = df.groupby(['combo']).size().sort_values(ascending=False)
    print(f'Most common both station: {most_common_both.index[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print(f'Total travel time: {total_travel}')

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print(f'Mean travel time: {mean_travel}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_ct = df['User Type'].value_counts()
    print(f'User Type Counts: \n{user_ct}\n')
    
    # Display counts of gender
    try:
        gender_ct = df['Gender'].value_counts()
        print(f'Gender counts: \n{gender_ct}')
    except:
        print('Gender counts: No gender data available.')
    
    # Display earliest, most recent, and most common year of birth
    try:
        min_birth_year = int(min(df['Birth Year']))
        print(f'\nEarliest birth year: {min_birth_year}')
    except:
        print('\nEarliest birth year: No birth year data available.')
        
    try:
        max_birth_year = int(max(df['Birth Year']))
        print(f'Most recent birth year: {max_birth_year}')
    except:
        print('Most recent birth year: No birth year data available.')
    
    try:
        most_common_birth = int(df['Birth Year'].mode())
        print(f'Most common birth year: {most_common_birth}')
    except:
        print('Most common birth year: No birth year data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def getRawData(df):
    df = df.reset_index()
    response = input('Would you like to see some of the raw user data? (Y/N)\n')
    start = 0
    end = 5

    while response.upper() != 'N':
        
        if end <= len(df):
            for index in list(range(start, end)):
                print(df.loc[index], '\n')
            start = end
            end += 5
            response = input('Would you like to see another 5 rows? (Y/N)\n')
        else:
            for index in list(range(start, len(df))):
                print(df.loc[index], '\n')
            print('No more items!')
            break


def main():
    while True:
        df = getDataSet()

        if df.empty:
            print('There is no data for the period you selected.')
            return
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            getRawData(df)

        restart = input('\nWould you like to restart? (Y/N)\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()