import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# function to get worksheet by name from Google Sheet
def get_worksheet_by_name(sheet_name):
    sheet = client.open(sheet_name).sheet1
    return sheet

# function to get all values from a worksheet in Google Sheet
def get_all_values_from_worksheet(sheet_name):
    sheet = get_worksheet_by_name(sheet_name)
    values = sheet.get_all_values()
    return values

# function to add a new row to a worksheet in Google Sheet
def add_row_to_worksheet(sheet_name, values):
    sheet = get_worksheet_by_name(sheet_name)
    sheet.append_row(values)

# function to clear all rows from a worksheet in Google Sheet
def clear_worksheet(sheet_name):
    sheet = get_worksheet_by_name(sheet_name)
    sheet.clear()
