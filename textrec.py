from PIL import Image
from pytesseract import pytesseract
import re
import os

# <!-- <div class="col-xl-4 col-sm-6 mb-5">
#     <div class="bg-white rounded shadow"><img src="{{ i['poster']}}" alt=""  class="img-fluid  mb-3 ">
#         <h5 class="mb-0 px-2">Name : {{ i['name'] }}</h5>
#         <div class="small text-uppercase text-muted px-2">Venue : {{ i['venue'] }}</div>
#         <div class="small text-uppercase text-muted px-2">Date : {{ i['datetime'] }}</div>
#         <a href="#" class="btn btn-primary px-2">Learn More</a>
#         {% if var %}
#         <a href="#" class="btn btn-primary admin-visible">Edit</a>
#         {% endif %}
#     </div>
#   </div>-->

path_to_tesseract = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
image_path = r"static/images/uploaded/brochure2.jpeg"
pytesseract.tesseract_cmd = path_to_tesseract
# for root, dirs, file_names in os.walk(image_path):
#     for file_name in file_names:
img = Image.open(image_path )
text = pytesseract.image_to_string(img)
ocr_text=text.lower().capitalize()
venue_pattern = r'\b(?:[A-Z][a-z]*\s)*[A-Z][a-z]*\s(?:[A-Z][a-z]*\s)*\b(?:Auditorium|Classroom|Hotel|Floor|Venue)\b'
venues = re.findall(venue_pattern, ocr_text)
print("Venues:", venues)
date_pattern = r"(\d{1,2})\s(January|February|March|April|May|June|July|August|September|October|November|December|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(\d{4})"
dates = re.findall(date_pattern, ocr_text)
print("Dates:", dates)
time_pattern = r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b'
times = re.findall(time_pattern, ocr_text)
print("Times:", times)
# open text file
text_file = open("data.txt", "w")
 
#write string to file
text_file.write(text)
 
#close file
text_file.close()

from dateutil.parser import parse
with open('data.txt', 'r') as f:
    text = f.read()
for word in text.split():
    try:
        date = parse(word, fuzzy=True)
        print(date)
    except ValueError:
        pass



            





