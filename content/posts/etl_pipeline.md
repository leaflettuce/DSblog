Title: Automating an ETL Pipeline w/ Python and MySQL
Slug: auto_etl_pipeline
Date: 2019-05-26 08:30
Category: Exploratory Data Analysis
Tags: pandas, Python, cleaning, etl, sql, manipulation
author: Andrew Trick
Summary: I find myself often working with data that is updated on a regular basis. Rather than manually run through the etl process every time I wish to update my locally stored data, I thought it would be beneficial to work out a system to update the data through an automated script. I use python and MySQL to automate this etl process using the city of Chicago's crime data.

GitHub Repo: [leaflettuce/chicago_crime](https://github.com/leaflettuce/chicago_crime)<br>

# Automating an ETL Pipeline w/ Python and MySQL
NOTE: These are only highlights of the full code, please go to above repo and clone for full version.
<br>
### Background 
The city of Chicago has a wonderful data portal that constantly updates data on different aspects of the city. I've been interesting in exploring and analyzing the crime data set available in this portal for quite some time now. While extracts of the data can be pulled directly into csv format off the site, I wanted to find a way to create a pipeline which is able to automatically update the local version of this data on a daily basis. Rather than manually re-pull the csv each day, they have an option to connect to an API which I use. This process also allows for the cleaning and feature generation to be conducted during data import rather than manually run after updating the csv file.
<br>

### Connecting to the Data
The first step is to connect to the data. Chicago uses Saleforce to provide API connectivity to their data. Once obtaining credentials through their portal we can use requests in Python to connect to and query this data.
```
URL = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?"

API_TOKEN = os.environ.get("CHI_API_TOKEN")
if not API_TOKEN:
    print("You need to get an City of Chicago API token! Exiting..")
    sys.exit(1)

for year in range(2001, 2020):    
    # set parameters
    print('querying year: ' + str(year))
    param = {'$$app_token' : API_TOKEN,
             #'$select' : 'date, COUNT(date)',   #example query
             #'$group' : 'date',    # example query
             '$limit' : '1000000',
             '$where' : 'year = ' +  str(year)}
      
    # API call 
    response = requests.get(URL, params = param)
    data = json.loads(response.text)
    
    # set to df
    df = json_normalize(data)
    
    # write out
    upload_dir = 'E:/projects/chi_crime/data/raw/'
    upload_file = 'raw_' + str(year)
df.to_csv(upload_dir + upload_file + '.csv', index = False)
```
Notice the loop iterating through each year and querying off this. While the full data set could be requests at once, running in smaller queries like this greatly speeds up the process.
<br>
### Processing the Data 
Chicago keeps the data sets relatively complete and clean. There was little to do here in ways of data cleaning and imputation- any missing data was due to early versions not tracking all the variables later versions have. As such, I focus more on feature generation in this step.
<br><br>The analysis I'd like to complete on this data is focused on exploring trends in chi crime rates over temporal elements. So, I focus mostly on splitting up the datetime var into specific elements which will be beneficial later on when visualizing the data.
```
# AGGREGATE DATA
df_agg = pd.DataFrame()
for year in range(2001, 2020): # iterate through each year, pulling in raw data and adding to final aggregate df
    temp_df = pd.read_csv('../../data/raw/raw_' + str(year) + '.csv')
    if year == 2001:
        df_agg = temp_df
    else:
        df_agg = pd.concat([df_agg, temp_df])
        
df_agg = df_agg.reset_index(drop=True) 


# FEATURE GENERATION
# set time
df['time'] = ''
df.time = df.date.str[11:-7]

# set date
df['full_date'] = df.date
df.date = df.date.str[0:10]

# set hours
df['hour'] = 0
df.hour = df.time.str[0:2].astype(int)

# set month
df['month'] = df.date.str[5:7].astype(int) 

# set day of month
df['day'] = df.date.str[8:10].astype(int) 

# set hour bins
conditions = [
    (df['hour'] >= 0) & (df['hour'] < 8),
    (df['hour'] >= 8) & (df['hour'] < 16),
    (df['hour'] >= 16)]
choices = ['0 - 8', '8 - 16', '16 - 24']
df['hour_bin'] = np.select(conditions, choices, default='0')

# add day of week
df['datetime'] = pd.to_datetime(df.date) # helper col
df['day_of_week'] = df['datetime'].dt.day_name()

# add week number
df['week_number'] = df['datetime'].dt.week

# Prune features
df = df.drop(['datetime', 'full_date'], axis = 1) # drop helper
```
<br>
### Loading into MySQL
While SQL Server or any other number of storage environments would be suitable for this data, I opted for MySQL as I already had to running on my localhost. I use the mysql.connector module for this process.
<br><br>Pretty standard loading process. I had error with some of the data types so did a broad strokes varchar and int rather than fine-tune.. While not the best decision its a trade off with time and my analysis needs are simple so this should not result in any difficulties down the road.
<br><br>This creates the DB, table, and then loads the data in 10,000 rows at a time. I initially tried to load all 7m at once and my computer decided it didn't like this.. :/  Splitting it like this just smooths the loading process for the CPU a bit.
```
MYSQL_PASS = os.environ.get("MYSQL_PASS")

# import data
df = pd.read_csv('../../data/processed/crime.csv')

# connect to db
cnx = mysql.connector.connect(user='root', password=MYSQL_PASS,  # set pass to API envi
                              host='localhost')
cursor = cnx.cursor()

# create new DB for storage
cursor.execute("CREATE DATABASE chicago_crime")  
cursor.execute('USE chicago_crime;')

# create table for crime data
cursor.execute("CREATE TABLE crime (arrest VARCHAR(255), beat VARCHAR(64), block VARCHAR(255), \
                                    case_number VARCHAR(255), community VARCHAR(255), \
                                    date VARCHAR(255), description VARCHAR(255), \
                                    district VARCHAR(255), domestic VARCHAR(255), fbi_code VARCHAR(255), \
                                    id INT(64) PRIMARY KEY, iucr VARCHAR(255), latitude VARCHAR(255), \
                                    address VARCHAR(255), latitude_2 VARCHAR(255), longitude_2 VARCHAR(255), \
                                    loc_description VARCHAR(255), longitude VARCHAR(255), primary_type VARCHAR(255), \
                                    updated_on VARCHAR(255), ward VARCHAR(255), x_coord VARCHAR(255), y_coord VARCHAR(255), \
                                    year INT(64), time TIME, hour INT(64), month INT(64), day INT(64), \
                                    hour_bin VARCHAR(255), day_of_week VARCHAR(255), week_number INT(64))")

# helper function to insert data rows into table
def insert_crime(crime):
    query = "INSERT INTO crime (arrest, beat, block, case_number, community, date, description, district, domestic, fbi_code,\
                                id, iucr, latitude, address, latitude_2, longitude_2, loc_description, longitude, primary_type, \
                                updated_on, ward, x_coord, y_coord, year, time, hour, month, day, hour_bin, day_of_week, week_number) \
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            
    try:
        cursor.executemany(query, crime)
 
    except Error as e:
		print('Error:', e)

# set pandas df to list 
crimes_list = df_null.values.tolist()
# crimes_list = crimes_list[:100]   # for testing

# insert list into table with helper function
print('loading into SQL 10,000 rows at a time.')
for i in range(0, len(crimes_list), 10000):
    print(i + '/' + len(crimes_list))
    insert_crime(crimes_list[i : i + 10000])
    
# commit additions
cnx.commit()
```
<br>
### Bringing the System Together
With the initial data import query, aggregation, and processing complete, I then move on to combining each of them into a batch script to make this easy to run. Not only can I run this from the console and collect the entire dataset, but I can now simply git pull this repo and be able to load the entire data set (cleaned and processed) onto any machine I want. 
<br><br>Similarly, anyone else who would like this same processed data set should be able to do the same as long as they acquire an API key. 
<br>NOTE: I added in a requirements.txt check in the batch file to make sure no errors occur when running py files. The get_requs.py file also checks for data directories and creates them if needed.
```
REM pip install -r requirements.txt

python get_requs.py

echo Querying crime data (2001 to current) from City of Chicago by year...
python pull_raw_data.py

echo Raw data imported successfully! 
echo Aggregating data into complete data set...
python aggregate_data.py

echo Aggregation complete! 
echo Cleaning data and processing model requirements...
python clean.py
 
echo Data processing complete! :)
echo Creating MySQL Storage and uploading...
python load_into_sql.py

echo SQL storage successful!
echo ALL DONE! Have a good day :)
```
<br>
### Updating the System
While data is able to be loaded fine, it's a bit redundant and wasteful to load all 7 million rows of data in every time we want to update the new crimes. To deal with this problem, we need to create a method of storing the last crime datetime included in our most recent data pull (either in inital load or in an update).
<br><br>A simple way of dealing with this is to create a txt file which stores the last datetime within the dataset whenever querying the API. This is the route I took, and you can see in both the initial loading and the updating files that I call for the MAX(datetime) in the pandas df and print it to the txt file.
```
# in initial pull
with open('last_update.txt', 'w') as f:
f.write(max(df.iloc[:, 5]))

# and to pull it in for updating
txt_file = open("last_update.txt", "r")
last_update_datetime = txt_file.read()
```
<br>
As stated, a rather simple solution. Once this is done, we can use this tracked datetime when querying for updates to ensure we pull only data that has been uploaded to Chi's system since our last import.
<br><br>The most significant change is the API query off the stored datetime:
```
param = {'$$app_token' : API_TOKEN,
         '$limit' : '1000000',
		 '$where' : 'date > \'' + last_update_datetime + '\''}
```
<br>
This extract, aggregate, clean, and loading process for the updater is very similar to the initial loading and a lot of copy-paste is used. The main difference is in the filenames and store process locally.
<br><br> I thought it also important to keep the last version of the data in a backup on local as well in case of any loading or processing errors. This is taken care of by simply writing out the old csv before concating the new data to it:
```
# store old data in backup
upload_dir = 'E:/projects/chi_crime/data/interim/'
upload_file = 'BACKUP-previous_version'
df_old.to_csv(upload_dir + upload_file + '.csv', index = False)

# update working df
df = pd.concat([df_old, df])     
df = df.reset_index(drop=True) 
```
<br>Once all the necessary files were complete, I formed a second batch file which runs all the code to import, process, and load the new data into the MySQL table.
```
echo Updating crime data based on last import or update.
echo Please wait ;)
python updater.py

echo Data Successfully updated!
echo Cleaning new version of data and processing model requirements...
python clean.py
python clean_new_data.py

echo Data processing complete! :)
echo Inserting new files into MySQL storage...
python update_sql.py

echo SQL storage successful!
echo ALL DONE! Have a good day :)
```
<br>
### Final Considerations
As it stands now, I can import the cleaned and processed data onto any machine by pulling this repo and running the batch file. Similarly, I can keep the data up to date by running the updater batch script every day or so.
<br><br>The only step after this to full automate the process would be to set up an event scheduler to run the updater batch script on a regular schedule. While rather simple to do, I plan to skip this step as I work primarily off a laptop and will not have the constant uptime best suited for such scheduler. 
<br><br>It's a simple system (running a bat from console) and I'm quite happy just running the script right before running analysis or visualization- Which will be my next post here! 
