import datetime
import math
import re

from django.utils.html import strip_tags


def count_words(html_string):
    # html_string = """
    # <h1>This is a title</h1>
    # """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string) 
    count = len(matching_words)
    return count

# this is going to be used and tested in python manage.py shell
# for does purposes , change the indentation form tabs to 4 spaces in case you get an indentation error

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0) # assuming 200 words per minute reading
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    # you set to return a string or a datetime type
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min) # read_time



