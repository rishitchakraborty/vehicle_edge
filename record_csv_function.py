import cv2
import time
import sys
from datetime import datetime
import glob
import pandas as pd
from secrets import access_key, secret_access_key
import multipleVideo
import boto3
import os
import multiprocessing


def transferVideoFiles():
    print("Transfer Video Called....")

    client = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')

    print("File Uploading")
    video_list = multipleVideo.multipleVideoPlayingFunction('RECORD')
    frame_list = []
    # print(video_list)
    for file in video_list:
        if '.avi' in file:
            print(video_list)
            upload_file_bucket = 'rishit-lambda'
            # upload_file_key = 'RECORDS/' + str(file)
            upload_file_key = str(file)
            client.upload_file(file, upload_file_bucket, upload_file_key)
            print("Done Uploading")


def recordVideoFileAndSaveCSVsFunction(fps, width, height, control, folder_path_saving, csv_folder_saving_name, camera_index):
    try:
        if control == True:

            fps = fps
            width = width
            height = height
            video_codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")

            print("\nTHE EDITORIAL CODE IS RUNNING")
            print("===================================")

            name = folder_path_saving
            cap = cv2.VideoCapture(camera_index)
            ret = cap.set(3, width)
            ret = cap.set(4, height)
            cur_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

            start = time.time()
            video_file_count = 1
            file = datetime.now().strftime("%Y%m%d-%H_%M_%S")

            video_file = os.path.join(name, str(file)+str(video_file_count) + ".avi")

            print("Capture video saved location : {}".format(video_file))

            # Create a video write before entering the loop
            video_writer = cv2.VideoWriter(
                video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
            )

            while cap.isOpened():
                start_time = time.time()
                ret, frame = cap.read()
                if ret == True:
                    cv2.imshow("frame", frame)
                    if time.time() - start > 10:
                        start = time.time()
                        curr_time = datetime.now()

                        video_file_count += 1

                        # file = datetime.now().strftime("%Y%m%d-%H%M%S")
                        # video_file1 = os.path.join(name, str(video_file_count) + ".avi")
                        video_file = os.path.join(name, str(file) + str(video_file_count) + ".avi")
                        video_writer = cv2.VideoWriter(
                            video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
                        )
                        # No sleeping! We don't want to sleep, we want to write
                        # time.sleep(10)

                    # Write the frame to the current video writer
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    frame = cv2.putText(frame, str(datetime.now()), (10, 30), font, 1, (210, 155, 155), 2, cv2.LINE_AA)
                    video_writer.write(frame)
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()

            x = 'RECORD'
            y = './CSVs'
            video_list = [items for items in glob.glob(x + "/*")]
            cleaned_mp4s = [files.replace("\\", "/") for files in video_list]
            final_videos = [str(item) for item in cleaned_mp4s]

            # unique id creation portion
            unique_id_mp4s1 = [files.replace("RECORDS\\", "") for files in video_list]
            unique_id_mp4s2 = [files.replace(".avi", "") for files in unique_id_mp4s1]
            t1 = [str(item) for item in unique_id_mp4s2]
            t2 = []
            t3 = []
            for i in range(len(final_videos)):
                # calculate timestamp of the video files
                time_c = time.ctime(os.path.getctime(final_videos[i]))
                x = time_c.split(" ")
                time_elem = x[3]
                t2.append(time_elem)
                # calculate the size of the video files
                file_size = os.stat(final_videos[i])
                file_size_format = os.path.join(str(file_size.st_size) + " bytes")
                t3.append(file_size_format)

            print("\nUnique id of files are:")
            print("==========================================")
            print(t1)
            print("\nvideo file creation times are:")
            print("===========================================")
            print(t2)
            print("\nsize of files are:")
            print("===========================================")
            print(t3)

            # writing details to a csv file

            # dictionary of lists
            dict = {'id': t1, 'timestamp': t2, 'file_size': t3}

            df = pd.DataFrame(dict)

            # saving the dataframe
            df.to_csv('./CSVs/output.csv', index=False)

        else:
            pass
    except Exception as exp:
        print("error occured.....")


if __name__ == "__main__":

    W = 864
    H = 640
    FPS = 30
    PATH = 'RECORD'
    CAMERA = 0
    PATH2 = './CSVs'
    p1 = multiprocessing.Process(target=recordVideoFileAndSaveCSVsFunction, args=(FPS, W, H, True, PATH, PATH2, CAMERA))
    p2 = multiprocessing.Process(target=transferVideoFiles)

    p1.start()
    p1.join()

    p2.start()
    p2.join()









