import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import html as hhtml
import requests
from urllib.parse import urlparse
import pandas as pd
import re
from tqdm import tqdm