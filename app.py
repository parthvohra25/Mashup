import os
from os import path
from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import sys
from urllib.parse import quote

#NEW>

def download_files(x, n, y, output_name):
    try:
        n = int(n)
        if n <= 0:
            raise Exception("Invalid value of 'n' provided. 'n' should be a positive integer.")
    except:
        raise Exception("Invalid value of 'n' provided. 'n' should be a positive integer.")

    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    count = 0
    for i in range(n):
        if i >= len(video_ids):
            break

        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i])
        if yt.length / 60 <= 5:
            print("Songs are downloading " + str(count) + " .......")
            mp4files = yt.streams.filter(only_audio=True).first().download(filename='song-' + str(count) + '.mp3')
            count += 1
        else:
            print("Song " + str(i + 1) + " has been skipped because of the length.")

    if count == 0:
        raise Exception("No video was found whose length is less than 5 minutes.")
    else:
        print("Your songs have been downloaded")
        print("Starting to create mashup.....")
    fin_sound = merge_sound(n, y)
    fin_sound.export(output_name, format="mp3")

    print("Mashup has been created successfully...")
    return "Done"



def merge_sound(n, y):
    if os.path.isfile("song-0.mp3"):
        try:
            fin_sound = AudioSegment.from_file("song-0.mp3")[0:y*1000]
        except:
            fin_sound = AudioSegment.from_file("song-0.mp3", format="mp4")[0:y*1000]
    for i in range(1, n):
        aud_file = str(os.getcwd()) + "/song-"+str(i)+".mp3"
        try:
            f = AudioSegment.from_file(aud_file)
            fin_sound = fin_sound.append(f[0:y*1000], crossfade=1000)
        except:
            f = AudioSegment.from_file(aud_file, format="mp4")
            fin_sound = fin_sound.append(f[0:y*1000], crossfade=1000)
        
    return fin_sound



def main():
    query = "Old Karan Aujla"  # Replace with your desired YouTube search query
    encoded_query = quote(query)  # URL encode the query

    n = 3  # Replace with the desired number of videos to download
    y = 30  # Replace with the desired duration in seconds
    output_name = "output_mashup.mp3"  # Replace with the desired output file name

    # Call the download_files function with the encoded query
    download_files(encoded_query, n, y, output_name)

# Execute the main function
main()
