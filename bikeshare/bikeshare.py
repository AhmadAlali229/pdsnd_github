import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def input_check(input_String,input_Sort):
    """
    makes sure that the input entered by user is correct
    
    InputSort: is what kind of input
    InputString: is what the user entered C for city , M for month , D for Day
    """
    while True:
        input_read=input(input_String).lower()
        try:
            if input_read in ['chicago','new york city','washington'] and input_Sort == 'C':
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_Sort == 'M':
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_Sort == 'D':
                break
            else:
                if input_Sort == 'C':
                    print("The city You have Enetered is not listed, Please choose : chicago,  new york , washington")
                if input_Sort == 'M':
                    print("The month You have Enetered is not listed, Please choose january ,february ,march ,april ,may ,june, all")
                if input_Sort == 'D':
                    print("The day You have Enetered is not listed, Please choose friday, saturay, sunday, monday, tuesday , wednesday, thrusday, all")
        except ValueError:
            print("Wrong Entry")
    return input_read

def get_filters():
    """
    get_filters asks the user to enter the city, month and day
    
    Returns:
          (str) city - name of the city to get data from
          (str) month - name of the month to be filterd
          (str) day - name of the day of week be filterd
    """
    city = input_check("choose the prefered city : chicago,  new york , washington ",'C')
    month = input_check("What month ", 'M')
    day = input_check("What day ", 'D')
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
    # Load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extracting month and day of week and hour from start time to make columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filtering by month.
    if month != 'all':
        # Using index of months to get corresponding int.
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Create new dataframe.
        df = df[df['month'] == month]
    
    # Filtering by day of week.
    if day != 'all':
         # Create new dataframe.
        df = df[df['day_of_week'] == day.title()]

    return df
    
def popular_times(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()
    popular_month = df['month'].mode()[0]
    popular_week = df['day_of_week'].mode()[0]
    popular_hour = df['hour'].mode()[0]
    # Display the most common month.
    print('most common month of the year', popular_month)
    # Display the most common day of week.
    print('most common day of week', popular_week)
    # Display the most common start hour.
    print('most common hour of day', popular_hour)
    
    print("time spent cauclating %s seconds" % (time.time() - start_time))
    print('-'*40)
def popular_trips(df):
    """Displays statistics on the most popular stations and trip."""
    start_time = time.time()
    start_station = df['Start Station'].mode()[0]
    end_station = df['End Station'].mode()[0]
    group_field=df.groupby(['Start Station','End Station'])
    start_to_end = group_field.size().sort_values(ascending=False).head(1)
    # Display most commonly used start station.
    print('most common start station', start_station)
    # Display most commonly used end station.
    print('most common end station', end_station)
    # Display most frequent combination of start station and end station trip.
    print('most common trip from start to end \n', start_to_end )
    
    print("time spent cauclating %s seconds" % (time.time() - start_time))
    print('-'*40)
def trip_duration(df):
    """Displays statistics on the total and average trip duration."""
    
    start_time = time.time()
    total = df['Trip Duration'].sum()
    total = total /60 # Total to minutes.
    average = df['Trip Duration'].mean()
    average = average / 60 # Average in minutes.
    # Display total travel time.
    print('total travel time in minutues is', total)
    # Display mean travel time.
    print('average travel time in minutues is', average)
    print("time spent cauclating %s seconds" % (time.time() - start_time))
    print('-'*40)
def user_info(df,city):
    """Displays statistics on bikeshare users."""
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    # Display counts of user types.
    print('counts of each user type \n',user_types)
    if city != 'washington':
        gender = df['Gender'].value_counts()
        # Display counts of gender.
        print('counts of each gender \n',gender)
        # Display earliest, most recent, and most common year of birth.
        print('most recent year of birth',df['Birth Year'].max())
        print('most common year of birth',df['Birth Year'].mode()[0])
        print('most earliest year of birth',df['Birth Year'].min())
         
    print("time spent cauclating %s seconds" % (time.time() - start_time))
    print('-'*40)
def main():
    while True:
        city, month, day = get_filters()
        df= load_data (city,month,day)
        popular_times(df)
        popular_trips(df)
        trip_duration(df)
        user_info(df,city)
        count = 5 
        # Asks the user if they want to print raw data.
        raw_data = input('Would you like to see the first five lines raw data  ? yes or no ')
        while raw_data  == 'yes':
             print(df.iloc[count:count+5]) 
             count += 5
             raw_data = input('Would you like to see the next five lines of raw data  ? yes or no ') 
             # Asking the user if they wanted to print the next five lines.   
          
        restart = input('Would you like to try again ? yes or no ')
        if restart != 'yes':
            break
        
        
if __name__=="__main__":
    main()