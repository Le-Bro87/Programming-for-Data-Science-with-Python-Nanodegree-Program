import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nSelect a city to filter by? New York City, Chicago or Washington?\n").lower().title()
    while city not in ('New York City', 'Chicago', 'Washington'):
     city = input("\nUnable to recognise this city, please try again! New York City, Chicago or Washington.\n")
        
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("\nSelect a month between January and June to filter by. Otherwise select all for all months\n").lower().title()
    while month not in ('January', 'February', 'March', 'April', 'May', 'June', 'all'):
     month = input("\nUnable to recognise this month, please try again!\n")
         
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nEnter a weekday to filter by, or enter all for all days\n").lower().title()
       
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
   	 	# use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    try:
      print('The most common month is: ', df['month'].mode()[0])
    except KeyError:
      print("\nThe most common month is:\nNo data available...")

    # TO DO: display the most common day of week
    try:
     print('The most common day of the week is:', df['day_of_week'].value_counts().idxmax())
    except KeyError:
      print("\nThe most common day of the week is:\nNo data available...")

    # TO DO: display the most common start hour
    try: 
      df['hour'] = df['Start Time'].dt.hour
      popular_hour = df['hour'].mode()[0]
      print('The most common hour is:', popular_hour)
    except KeyError:
      print("\nThe most common hour is:\nNo data available...")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most Commonly used start station:', df['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print('\nMost Commonly used end station:', df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    print("The most frequent combination of start and end stations per trip are")
    most_common_start_and_end_stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(most_common_start_and_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time: ', sum(df['Trip Duration'])/86400, "Days") 
    #86400 seconds in the day

    # TO DO: display mean travel time
    print('Mean travel time: ', df['Trip Duration'].mean()/60, "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    try:
      print(df['Gender'].value_counts())
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")      
    
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
      print("The earliest birth year is: ",int(df['Birth Year'].min()),
          ", \nThe most recent birth year is: \n",int(df['Birth Year'].max()),
           "\nand The most common year of birth is: \n",int(df['Birth Year'].value_counts().idxmax()))
    except KeyError:
      print("\nDisplay earliest, most recent, and most common year of birth:\nNo data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_data(df):
    start_data = 0
    end_data = 2
    df_length = len(df.index)
    
    while start_data < df_length:
        raw_data = input("\nWould you like to see individual trip data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.lower() != 'Yes':
            break

if __name__ == "__main__":
	main()
