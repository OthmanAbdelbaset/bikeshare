import time
import pandas as pd
import numpy as np
import calendar as clndr


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = clndr.month_name[1:]
MONTHS.append('all'.title())
DAYS = clndr.day_name[1:]
DAYS.append('all'.title())


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
    city = ''
    month = ''
    day = ''

    while True:
        try:
            city = input('Which city would you like to discover {}:'.format(list(CITY_DATA.keys())))
            if not city:
                city = 'chicago'
                break
            elif city.lower() not in list(CITY_DATA.keys()):
                raise ValueError
        except ValueError:
            print('sorry this is not a valid city, please try again!')
        else:
            city = city
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Which month would you like to check {} - \'all\' is the defualt if nothing selected:\n'.format(MONTHS)))
            if not month:
                month = 'all'
                break
            elif month.title() not in MONTHS:
                raise ValueError
        except ValueError:
            print('sorry this is not a valid month, please try again!')
        else:
            if month == 'all':
                month = 'all'
            else:
                month = str(MONTHS.index(month.title())+1)
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('Which day would you like to check {} - \'all\' is the defualt if nothing selected:\n'.format(DAYS)))
            if not day:
                day = 'all'
                break
            elif day.title() not in DAYS:
                raise ValueError
        except ValueError:
            print('sorry this is not a valid day, please try again!')
        else:
            if day == 'all':
                day = 'all'
            else:
                day = day
            break

    print('-'*40)
    print('Running parameters are:\nCity\t=', city, '\nMonth\t=', month, '\nDay\t=', day)
    return city.lower(), month, day.lower()


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
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    df['hour'] = df['Start Time'].dt.hour

    if month.lower() != 'all':
        df = df[df['month'] == int(month)]

    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # print(df.head())
    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common month is: {}'.format(MONTHS[most_common_month-1]))

    # TO DO: display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('Most common day is: {}'.format(most_common_day_of_week))

    # TO DO: display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('Most common hour is: {}'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df.groupby('Start Station').size().to_frame(name='size')
    popular_start_station_name = popular_start_station.idxmax()[0]
    popular_start_station_count = popular_start_station.max()[0]
    print('Most common start station is: {} with count of {}'.format(popular_start_station_name,popular_start_station_count))

    # TO DO: display most commonly used end station
    popular_end_station = df.groupby('End Station').size().to_frame(name='size')
    popular_end_station_name = popular_end_station.idxmax()[0]
    popular_end_station_count = popular_end_station.max()[0]
    print('Most common end station is: {} with count of {}'.format(popular_end_station_name,popular_end_station_count))

    # TO DO: display most frequent combination of start station and end station trip
    popular_start_end_station = df.groupby(['Start Station', 'End Station']).size().to_frame(name='size')
    popular_start_end_station_name = popular_start_end_station.idxmax()[0]
    popular_start_end_station_count = popular_start_end_station.max()[0]
    print('Most common Start & End station are: {} with count of {}'.format(popular_start_end_station_name,popular_start_end_station_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = round(df['Trip Duration'].sum()/3600.0/24, 2)
    print('Total travel time is: {} days'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean()/60.0, 2)
    print('Average travel time is: {} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User trypes are:\n{}\n'.format(pd.DataFrame(user_types)))
    print('-'*40)

    if 'Gender' in df:
        # TO DO: Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('Gender distribution is as follows:\n{}\n'.format(pd.DataFrame(gender_count)))
    else:
        print('No gender data available.')
    print('-'*40)

    if 'Birth Year' in df:
        # TO DO: Display earliest, most recent, and most common year of birth
        lowest_dob = int(df['Birth Year'].min())
        largst_dob = int(df['Birth Year'].max())
        common_dob = int(df['Birth Year'].mode())

        print('Earliest year of birth is: {}'.format(lowest_dob))
        print('Most recent year of birth is: {}'.format(largst_dob))
        print('Most common year of birth is: {}'.format(common_dob))

    else:
        print('No birth year data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            x = 0
            while True:
                try:
                    raw_data_check = input('Do you want to check a sample of the raw data (Yes/No)?')
                    if raw_data_check.lower() != 'yes':
                        raise ValueError
                    elif raw_data_check.lower() == 'yes':
                        for i in range(x, x+5):
                            print(df.iloc[i, 1:-3].to_frame())
                            print('*'*50)
                except ValueError:
                    break
                else:
                    x += 5
                    continue

        else:
            print('!'*40,' \nSorry, No data were found for the selected parameters.')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
