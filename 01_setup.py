#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

PROJECT:        Fetch data about books from Adlibris
DESCRIPTION:    Create a scraper which collects data on books from Adlibris. 
                Model the data and insert into database.
                Select a random book based on filter(s) and show information on that book.

AUTHOR:         Anna Tykkyläinen
DATE CREATED:   2022-01-19

"""

##############################################################################
###   IMPORT LIBRARIES   #####################################################

import os
from pathlib import Path
import requests
import time
from datetime import date
import datetime as dt
import re
from selenium import webdriver #https://www.selenium.dev/documentation/webdriver/getting_started/upgrade_to_selenium_4/
from selenium.webdriver.chrome.service import Service as ChromeService #https://www.selenium.dev/documentation/webdriver/getting_started/upgrade_to_selenium_4/
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import json
import random
from random import randint
import glob
import mysql.connector
from mysql.connector import errorcode

##############################################################################
###   CREATE FOLDERS   #######################################################

home_folder = Path(os.getcwd())
data_folder = home_folder.joinpath("data")
log_urls_folder = data_folder.joinpath("urls log")
books_to_fetch_folder = data_folder.joinpath("01 books to fetch")
books_to_parse_folder = data_folder.joinpath("02 books to parse")
log_errors_folder = data_folder.joinpath("error log")




