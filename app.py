#IMPORTING ESSENTIAL LIBRARIES
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib
# from email import encoders
# from flask import Flask,render_template,request
# import smtplib
# from email.message import EmailMessage





# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/start',methods=['POST'])
# def hello_world():
#     # if len(sys.argv) == 5:
#     # data = request.form.get("singerName")
#     x =  request.form.get("singerName")
#     # print(x)
#     x = x.replace(' ','') + "songs"
#     try:
#         n = int(request.form['vidName'])
#         y = int(request.form['durName'])
#     except:
#         sys.exit("Wrong Parameters entered")
#     email=request.form['emailName']
#     output_name = str(request.form['fnName'])
#     print(x,n,y,email,output_name)

    
#     if os.path.exists(output_name):
#         os.remove(output_name)
#     return download_files(x,n,y,output_name,email)




import os
from os import path
from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import sys
    
#NEW>

def download_files(x,n,y,output_name,email):
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
    fin_sound = merge_sound(n,y)
    fin_sound.export(output_name, format="mp3")

    print("Mashup has been created successfully...")
    # server = "smtp-mail.outlook.com"
    # sender = "your-mail-id"
    # recipient = email
    # password = "mail-id-password"
    # msg = MIMEMultipart()       
    # msg.attach(MIMEText("This is the message body of the email"))
    # part = MIMEBase('application', "octet-stream")
    # part.set_payload(open(output_name, "rb").read())
    # encoders.encode_base64(part)
    # part.add_header('Content-Disposition', 'attachment', filename=output_name)
    # msg.attach(part)

    # smtp = smtplib.SMTP('smtp-mail.outlook.com', 587)
    # smtp.starttls()
    # smtp.login(sender, password)
    # smtp.sendmail(sender, recipient, msg.as_string())
    # print("Email Sent AHHH YEAH")
    # smtp.quit()
    return "Done"



def merge_sound(n,y):
    # fin_sound =None
    if os.path.isfile("song-0.mp3"):
        try:
            fin_sound = AudioSegment.from_file("song-0.mp3")[0:y*1000]
        except:
            fin_sound = AudioSegment.from_file("song-0.mp3",format="mp4")[0:y*1000]
    for i in range(1,n):
        aud_file = str(os.getcwd()) + "/song-"+str(i)+".mp3"
        try:
            f = AudioSegment.from_file(aud_file)
            fin_sound = fin_sound.append(f[0:y*1000],crossfade=1000)
        except:
            f = AudioSegment.from_file(aud_file,format="mp4")
            fin_sound = fin_sound.append(f[0:y*1000],crossfade=1000)
        
    return fin_sound
  
if __name__ == '__main__':
    app.run(debug=True,port='5001')
