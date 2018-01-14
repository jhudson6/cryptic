# cryptic

Use main to create a book of coins where the desired coins are retrieved using a specific coin/currency pair and an exchange that pair is traded on.  For example btcusd:gdax.

The classes module contains the classes coin and book and model.  The coin is the class for a single pair:exchange, the model class contains the information needed for modeling such as data and model name/location, and the book class contains a wallet of coins supplied upon initialization and a list of models created using coins from its wallet.

The mySQLFunctions module contains everything needed to get data from a mySql database, create needed tables into the database and to load data into those tables.  Also has function to check for existence of desired tables.
  Naming Schema:  My database is called cryptic and all my tables are named after their pair:exchange handle, for example you could have      cryptic.btcusd_gdax (underscor instead of colon due to mySQL restrictions on naming)

The cryptoFunctions module currently only pings the cryptowat.ch API (https://api.cryptowat.ch).  It uses the module requests to make the pulls and get the resultant information in a json format.  Then each function breaks up the resultant json text into the correct componants by finding unique identifies in the text, for example {"open":666.66} would be converted to just 666.66.
  This can pull OHLC data, orderBook data, trades data as well as lists of available markets (pair:exchange), available exchanges,            available pairs, etc.
  There is an allowance variable that is global and updated after every pull.  This represents the remaining cpu time available for the      current IP address for that hour.  The initial cpu time allowance is 8000000000 cpu seconds.
  
The LSTM_TF contains the code neccessary to prepare data for fitting based on desired number of time steps for each iteration as well as the code neccessary for training a (currently) single layer LSTM using tensorflow.  This module is still having its basic functionality fleshed out.

The myMappings module simple contain functions to do minmax of z-normalization mapping of variables.  Currently used by LSTM_TF.

The feedparser and rss module is the least developed module and it will be used to create features for coins or markets based off of titles pulled from a google news rss feed that is following 'cryptocurrency'.

Needed:
-Completed model class in classes.py, needs to be easy to append a new 'blank' model to book.models and then train model on desired data and update all wallet.model[new_model_index] variables accordingly. (X_data,y_data,time_steps,model, etc.)
-Script and logic to pull data every X minutes/hours/days and load into mySQL
-TensorFlow stuff:
--Variable number of LSTM layers
--Ability to reset variables used for a specific model or define model specific variables to prevent issues when trying to create an additional model in a book that has existing models already.
--Ability to send prediction results to a mySQL table solely for the predicted data, as well as routines to generate goodness of fit parameters
-Shape detection and classification module (not started)
-Feature Generation from FeedParser
-Creation of 'potential' for use in feature generation from orderBook data
-Creation of function to calculate total volume as well as traded volume over time interval
-Function to identify correlations between different coin histories using a rolling window
-Add other trading signal-processing functions such as MACD, PPO, etc.  Have several of these elsewhere and will update when found.
-function to load data from CSV files into mySQL
-in insertData function and any other function that involves saving data create routine to automatically save a back up file as csv to specified location.
-mySQL function to export existing data to csv files for easy transfer over gitHub
-IMPORTANT: function to find and drop duplicates from existing tables in cryptic, important to prevent exploding database size.

mySQL:
To set up:
-download mySQL community server and install.
-open mySQL 5.7 Command Line Client and login as root using password supplied during startup (suggest to use mellon so no code needs to be rewritten)
-type 'Create database cryptic' to create database called cryptic
-database should now be good to interface with supplied mySQL module.
-DATA: Currently no data of use in database, as data is stored and a pull request is started, all stored data should be saved in csv_files that are named based off datatable name, then a function will be written to find files and load into corresponding tables in cryptic database.
