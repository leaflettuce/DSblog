Date: 2018-10-13 08:53 
Author: Andrew Trick 
Title: Merchandise Analysis Project (Part I)
Name: Merchandise Analysis Project (Part I)
Category: exploratory data analysis
Tags: sourcing, cleaning, python, pandas, collection,
Summary: Project to aggregate and analyze merchandise sales data for my band, TDWP. Overall goals are to develop a forecasting model to predict future sales volumes and to identify patterns with which to facilitate future design decisions. This post is a description of the first steps taken of this project- reolving primarily around: sourcing and collecting the data, methods of aggregating and combining the disparate dataset, and cleaning of the data into a relation format. This depicts the process from first steps to DB uploading.

# Merchandise Analysis Project (Part I)
Project to aggregate and analyze merchandise sales data for my band, TDWP. Overall goals are to develop
a forecasting model to predict future sales volumes and to identify patterns with which to facilitate 
future design decisions. This post is a description of the first steps taken of this project- reolving 
primarily around: sourcing and collecting the data, methods of aggregating and combining the disparate 
dataset, and cleaning of the data into a relation format. This depicts the process from first steps to DB 
uploading.
 <br>

## Goals

```
1 - Collect and aggregate unit sales of tour merchandise into a mySQL database.
2 - Analyze historic sales trends to forecast sales and enhance stock mgmt.
3 - More accurately predict merchandise sales for tour budgeting.
```
<br>
First steps- even before data collection- was to explore what this project might be able to achieve and the
reasons for conducting one such as this. As listed above, three specific and distinct benefits could be seen
from organizing and analyzing our historic merchandise sales. Brainstorming the goals like this provided not 
only an idea why this project should be attempted, but also pointed to the overall process of how the project 
should run, allowing for a vague outline of the project life-cycle.

<br>
## Overall Process
 
```
1 - Collect data (internal, scrapers, etc.)
2 - Generate features 
3 - store processed data into mySQL
4 - EDA FTW
5 - Explore models
6 - Report findings and methods of implementation
```
<br>
The process taken for this project is the typical expected for most data science work-flows. It begins with collecting
the data and ends with a final model for forecasting and visuals/reports to share and implement findings of analysis. 
A MySQL DB will be used to house the processed data- after first round feature generation- and before Exploration. While
the raw data will be stored and untouched throughout manipulation, I decided to generate a handful of obvious feaures
before storage into the DB. After this, exploration will lead to further manipulation and, eventually, a final report
indicating patterns found within the sale history. Lastly, a model will be crafted to forecast future sales for more
accurate budgeting and testing throughout the next tour. 

<br>
### Sourcing and Collecting the Data
The first step was to collect all necessary and/or useful data towards creating a system towards achieving the stated 
goals. The band has used <i>Atvenue</i> to track our sales in for the past few years, so connecting to and pulling 
historic data if our merch sales will be the primary resource. Their web portal used to access these numbers also 
provides a method of exporting the data- albeit in a method optimized for human viewing rather than any relational
or very organized format.The remainder of this post will focus on the decisions, processes, and code used to aggregate 
and clean this atvenue data into three relational formats- one for each specific goal above. 
<br>
<br>
#### Raw Data Format
###### <b>sales reports</b>
Data was exported into csv format and came in three different versions. First is 'sales reports' which display the
overall sales of each merch item for a tour. ie: the gross sales of a design and how the distribution of sales by 
size. Example head of excel view. <i>(Some columns are shortened to keep some information confidential.)</i>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="../img/tdwp_merch/sales_report_raw.png" style="width: 600px;"/><br>
Obviously not a great format to work with.. 

<br>
###### <b>Tour Summaries</b>
Next up are 'tour summaries'. Again, this exported in a format better for human viewing rather than what makes sense
for analyzing. Plenty of work needed to reset these into a useable format. Rather than the overall tour-wide reports
like above, these focus on the total merch sales per show of a tour- disregarding how the income was generated. This
will primarily be used for the forecasting goal listed above. 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="../img/tdwp_merch/tour_summaries_raw.png" style="width: 800px;"/><br>
Missing data abounds.

<br>
###### <b>Daily Reports</b>
Lastly from atvenue are are the 'daily reports'. By the far most difficult to use of the three given the formatting, this
revolves around per show sale counts by size. Expectedly, this will be msot useful in exploring how unit sales change based 
ongeo, tour type, season, day of week, etc. Each day was a separate spreadsheet, so work is also done to collect each of these
into one table per tour. 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="../img/tdwp_merch/daily_raw.png" style="width: 400px;"/><br>
Most of the table is unfilled. Manual calculations needed to figure sales counts.

<br>
###### <b>External Data</b>
Lastly, data collection also called for descriptions of the tour and merchandise. Each of these were manually created by myself. I
opted to keep these relatively simple and as objective as possible. As such, tour data includes temporal and geo information primarily-
season, year, country, etc. Additionally, It also has a binary value to indicate between support and headline tours.
The merchandise csv on the other hand revoles around the looks and design of each merch design. This includes color of shirt,
number of printed colors, etc. I also included numerous bool values to indicate if the design has our logo on it, lyrics, etc.
<br>
<br>
## Processing Raw Data
As mentioned the primary goal when processing data was to achieve an organized and relational format, with missing and erroneous 
data accounted for. Again, this is split into different cleaner files based on the data being worked with. Primary difficulties
revolved around ensuring the code could work for each csv file. With this in mind, I used a method of iterating through directories
to ensure the code was run on all appropriate files. I also joined the tour and merch datasets I created to each of these -as needed-
to provide all needed data into the final versions. This took two steps- first creating a dataset optimized for MySQL input, and a secon
which will be used for either analysis or modeling. 
Scripts were then written which, when the raw data is properly loaded into their directories, I can simply run the appropriate
bat file and all data will process/update. (All code viewable at my [GitHub](https://github.com/leaflettuce/tdwpDB).) 
<br>
As an example, one can see this set the data into a much more usable format. Below is the aggregate of sales reports:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="../img/tdwp_merch/processes_example.png" style="width: 800px;"/><br>

<br>
## MySQL
Last step for initializing this process was to upload the data into a MySQL server for storage and querying. While I'll probably
do most of my work on the csv's set out for analysis and modeling, I find the option to run a quick query to be extremely valuable.
I also wanted some more practice setting up a SQL DB. This step was pretty straightforward, and I'm not able to run SQL queries on 
the data, as in the example below I ran to test it with: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="../img/tdwp_merch/query_example.png" style="width: 400px;"/>

<br>
## Next Steps
So, with everything collected, processed, and stored efficiently, the next steps are to start EDA on the datasets. I plan to do this
in three different steps as well- one for each of the above goals. I'll use Tableau to explore patterns in Geo and temporal
variables, whille R will be utilized for most other exploration. Lastly, I'll also be looking to forecast sales of future tours,
so Python will be used as well. I upload Part II once these three steps are realized. 