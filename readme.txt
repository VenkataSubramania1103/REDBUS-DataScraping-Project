REDBUS DataScraping Project

This project is for scraping the bus details from REDBUS webpage for all the Bus services along with the required details.
We are using Python, Selenium, MySQL and streamlit

1. data_scraping file:
    we have three function blocks for scraping the data scraping
    1. first page - to get the list of hyperlinks for bus services
    2. second page - to get the list of hyperlinks and name for routes
    3. final page scraping - scraping the whole bus details
    
    Since we are scraping the whole redBus bus services, it is taking 1.5-2 hrs of time

2.  output_redbus
        The data processed by data_scraping file will be processed and stored as "output_redbus.xlsx" file

3. database_creation file:
    in this we will be converting the excel data to sql data using pandas and mysql

4. streamlit_app file:
    in this file we will be connecting to the redbus database and fetch the data from the bus_routes table

