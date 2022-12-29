import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = ''
    day = ''
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: ask user input for city (chicago, new york city, washington).
    several_cities = ['chicago', 'new york city', 'washington']
    city = str(input("Would you like to see data for Chicago, New York City, or Washington ? ")).lower().strip()
    while city not in several_cities:
        city = str(input("Would you like to see data for Chicago, New York City, or Washington ?")).lower().strip()

        print("You chose {} city to filter results by ".format(city))
    # TO DO: ask user input for month (all, january, ... , june)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    while month not in months:
        month = str(input("Which month - January, February, March, April, May, or June? ")).title().strip()
        if month in months:
            print("You chose month of {} to filter results by".format(month))
            break

    # TO DO: ask user input for day of week (all, monday, ... sunday)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
    while day not in days:
        day = str(
            input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?")).title().strip()
        if day in days:
            print("You chose {} to filter results by ".format(day))
            break

    print('-' * 40)
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

    # load file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is: {} '.format(most_common_month))
    # TO DO: display the most common day of week
    most_common_day = df['day'].mode()[0]
    print('The most common day is: {} '.format(most_common_day))

    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour is: {} '.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: {} '.format(start_station))
    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: {} '.format(end_station))
    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(
        'The most commonly used combination of start and end stations are:{} and {}'.format(most_common_combination[0],
                                                                                            most_common_combination[1]))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: {}, second'.format(total_travel_time))

    # TO DO: display mean travel time
    total_mean_time = df['Trip Duration'].mean()
    print('The mean travel time is: {}, second'.format(total_mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    for key, value in df['User Type'].value_counts().items():
        print('{} of the users are {}'.format(value, key))
    print('\n')
    # TO DO: Display counts of gender
    if 'Gender' in df:
        for key, value in df['Gender'].value_counts().items():
            print('{} of the users are {}'.format(value, key))
    print('\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        early_birth = 'Earliest birth year is ', int(df['Birth Year'].min())
        print(early_birth)
        latest_birth = 'Latest birth year is ', int(df['Birth Year'].max())
        print(latest_birth)
        print('Most common birth year is {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def get_raw_data(df):
    count = 0
    while True:
        repeat = input("Do you want to see some of the raw data? Enter yes or no as an answer.").lower().strip()
        if repeat == 'yes':
            print(df[count: count + 5])
            count += 5
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
        get_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
    