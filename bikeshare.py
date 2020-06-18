import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_choices = ('chicago', 'new york city', 'washington')
time_choices = ('month', 'day', 'both', 'none')
month_choices = ('january', 'february', 'march', 'april', 'may', 'june', 'all')
dow_choices = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')

# Ask user to input city
def city_input():
    print('Hello. Let\'s explore bikeshare data in US!')
    while True:
        try:
            city = input('Please pick a city Chicago, New York City, or Washington: ').lower().strip()
            if city in city_choices:
                break
        except:
            print('System Error!')
        print('Invalid input. Please input again!')
    return city

# Ask user if time filter needed
def time_filter_check():
    while True:
        try:
            time_filter = input('Would you like to filter the data by month, day, both, or none: ').lower().strip()
            if time_filter in time_choices:
                break
        except:
            print('System Error!')
        print('Invalid input. Please input again!')
    return time_filter

# Ask user to input month(if applicable)
def month_input():
    while True:
        try:
            month = input('Which month January, February, March, April, May, June, or all?').lower().strip()
            if month in month_choices:
                break
        except:
            print('System Error!')
        print('Invalid Input. Please input again!')
    return month

#Ask user to input dow(if applicable)
def dow_input():
    while True:
        try:
            dow = input('Which day of week Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?').lower().strip()
            if dow in dow_choices:
                break
        except:
            print('System Error!')
        print('Invalid Input. Please enter again in the format DDD!')
    return dow

#Load data with user inputs
def load_data(city, month, dow, time_filter):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] =  pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['dow'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + ' and return to ' + df['End Station']

#The question sets will be adjusted based on the user input
    if time_filter == 'both':
        if month != 'all':
            month = month_choices.index(month) + 1
            df = df[df['month'] == month]
            if dow != 'all':
                df = df[df['dow'] == dow.title()]
    elif time_filter == 'month':
        if month != 'all':
            month = month_choices.index(month) + 1
            df = df[df['month'] == month]
    elif time_filter == 'day':
        if dow != 'all':
            df = df[df['dow'] == dow.title()]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

#Most common month. If month filter is used, the asnwer will be the month that user input.
    df['Start Time'] =  pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    print('Most common month is:', most_common_month)

#Most common day of week. If day of week filter is used, the asnwer will be the day of week that user input.
    df['dow'] = df['Start Time'].dt.weekday_name
    most_common_dow = df['dow'].mode()[0]
    print('Most common day of week:', most_common_dow)

#Most common hour.
    most_common_start_hour = df['hour'].mode()[0]
    print('Most common start hour (24-hour format):', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

#Most Popular Start Station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', most_common_start_station)

#Most Popular End Station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', most_common_end_station)

#Most Popular Trip
    most_frequent_trip = df['trip'].mode()[0]
    print('Most frequent trip:', most_frequent_trip)
    print('The Start Station is', most_frequent_trip.split(' and return to ')[0],'and End Station is', most_frequent_trip.split(' and return to ')[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

# TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    hour = total_time//3600
    minute = (total_time%3600)//60
    sec = (total_time%3600)%60
    print('Total travel time in seconds:', total_time)
    print('In another word, total travel time is:', hour,'hour(s)', minute,'minute(s)', sec,'second(s)')

# TO DO: display mean travel time
    mean_time = (df['Trip Duration'].mean())
    mean_hour = mean_time//3600
    mean_minute = (mean_time%3600)//60
    mean_sec = (mean_time%3600)%60
    print('Total mean travel time in seconds:', mean_time)
    print('In another word, mean travel time is:', mean_hour,'hour(s)', mean_minute,'minute(s)', mean_sec,'second(s)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of user type without NaN entries:')
    print(df['User Type'].value_counts())

    #The code below is to show the same data with NaN entries
    #print('\nCounts of user type with NaN entries:')
    #print(df['User Type'].value_counts(dropna=False))

    # TO DO: Display counts of gender
    # Since Washington does not have column for Gender and Birth Year, we will skip this data when user input Washington
    if city != 'washington':
        print('\nCounts of gender without NaN entries:')
        print(df['Gender'].value_counts())

        #The code below is to show the same data with NaN entries
        #print('\nCounts of gender with NaN entries:')
        #print(df['Gender'].value_counts(dropna=False))

        # TO DO: Display earliest year of birth aka the birth year of the first customer
        first_tran = df[df['Start Time'] == df['Start Time'].min()]['Birth Year'].values
        print('\nThe customer who made the first transaction was born in:', first_tran[0])

        # TO DO: Display most recent, and most common year of birth
        recent_birth_year = df[df['Start Time'] == df['Start Time'].max()]['Birth Year'].values
        print('The most recent customer was born in:', recent_birth_year[0])

        # TO DO: Display most common year of birth
        common_birth_year = df['Birth Year'].mode()[0]
        print('The most common customer year of birth:', common_birth_year)
    else:
        print('\n***Washington does not have data for Gender and Birth Year***')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def ind_data(df):
    print('\nCalculating User Stats...\n')
    ind_df = df.drop(['month','dow','trip', 'hour'], axis =1)
    next_page = 'yes'
    i = 0
    while next_page == 'yes':
        try: #to prevent the loop crash when it reach to the end of the list!
            for i in range(i, i+5):
                 print(ind_df.iloc[i], '\n')
        except:
            print('This is the end of the list!')
            break
        i += 1
        next_page = input('Would you like to continue to next page? Input yes to continue or anything else to stop: ')

    print('-'*40)

def main():
    while True:
        city = city_input()
        time_filter = time_filter_check()
        if time_filter == 'both':
            month = month_input()
            dow = dow_input()
        elif time_filter == 'month':
            month = month_input()
            dow = ''
        elif time_filter == 'day':
            month = ''
            dow = dow_input()
        else:
            month = ''
            dow = ''

        df = load_data(city, month, dow, time_filter)

        answer_time = input('\nWould you like to see the most frequent Times of Travel? Input yes to continue or anything else to skip: ').lower().strip()
        if answer_time == 'yes':
            time_stats(df)

        answer_station = input('\nWould you like to see the most popular Stations and Trip? Input yes to continue or anything else to skip: ').lower().strip()
        if answer_station == 'yes':
            station_stats(df)

        answer_duration = input('\nWould you like to see Trip Duration? Input yes to continue or anything else to skip: ').lower().strip()
        if answer_duration == 'yes':
            trip_duration_stats(df)

        answer_user = input('\nWould you like to see User Stats? Input yes to continue or anything else to skip: ').lower().strip()
        if answer_user == 'yes':
            user_stats(df, city)

        answer_ind = input('\nWould you like to see Individual Data (group of 5)? Input yes to continue or anything else to skip: ').lower().strip()
        if answer_ind == 'yes':
            ind_data(df)

        restart = input('\nWould you like to restart? Enter \'yes\' to restart or antyhing else to stop.\n')
        if restart.lower().strip()!= 'yes':
            break

if __name__ == "__main__":
	main()

print('Thank you for stopping by. Good bye!')
