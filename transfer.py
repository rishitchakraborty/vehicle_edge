from secrets import access_key, secret_access_key
import multipleVideo
import boto3
import os

client = boto3.client('s3',
                        aws_access_key_id = access_key,
                        aws_secret_access_key = secret_access_key)

print("File Uploading")
video_list = multipleVideo.multipleVideoPlayingFunction('RECORDS')
frame_list = []
# print(video_list)
for file in video_list:
    if '.avi' in file:
        print(video_list)
        upload_file_bucket = 'rishit-bucket'
        #upload_file_key = 'RECORDS/' + str(file)
        upload_file_key = str(file)
        client.upload_file(file, upload_file_bucket, upload_file_key)
        print("Done Uploading")
