from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
import argparse
from http import client
import httplib2
import os
import time
import threading
import pyautogui

import googleapiclient
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, client.NotConnected,
                        client.IncompleteRead, client.ImproperConnectionState,
                        client.CannotSendRequest, client.CannotSendHeader,
                        client.ResponseNotReady, client.BadStatusLine)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config["YouTube"]["API_KEY"]
metaJson="metadata.json"
tags = ["reddit", "funny", "askreddit", "best", "montage", "compilation"]
description = """Reddit funny moments compilation from r/askreddit! 
Be sure to subscribe for daily funny reddit posts. Check out my
channel for more hilarious reddit clips!
"""
description = config["YouTube"]["DESCRIPTION"]
tags = config["YouTube"]["TAGS"]

def executeClicks():
  time.sleep(5)
  screen_width, screen_height = pyautogui.size()

# Perform a mouse click on username
  pyautogui.moveTo(960, 540)
  pyautogui.click()
  time.sleep(3)

# Perform a mouse click on continue
  pyautogui.moveTo(780, 610)
  pyautogui.click()
  time.sleep(3)
# Perform a mouse click on allow
  pyautogui.moveTo(1150, 900)
  pyautogui.click()
  # time.sleep(3)

def executeRequest(filePath, title):
  SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
  CLIENT_SECRETS_FILE = config["YouTube"]["CLIENT_SECRETS_FILE"]
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_local_server(scopes=SCOPES)
  youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
  print("Title-", f"{title} #shorts")
  request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": "22",
            "description": description,
            "title": f"{title} #shorts",
            "tags": tags
          },
          "status": {
            "privacyStatus": "public"
          }
        },
       
        media_body=MediaFileUpload(filePath)
    )
  response = request.execute()
  try:
  	if response['status']['uploadStatus'] == 'uploaded':
  		print('Uploaded')
  	else:
  		print('Upload failed')
  except Exception as e:
  	print('Upload failed')


  return response

def uploadVideo(filePath, title):
  thread1 = threading.Thread(target=lambda: executeRequest(filePath, title))
  thread2 = threading.Thread(target=executeClicks)
  thread1.start()
  thread2.start()
  thread1.join()
  thread2.join()

  # executeRequest()
  # response = request.execute()
  # print(response)