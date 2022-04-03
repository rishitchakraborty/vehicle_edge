import cv2
import warnings
import glob as glob
import time
import multiprocessing


def multipleVideoPlayingFunction(folder_path):
    x = folder_path

    video_list = [items for items in glob.glob("./" + x + "/*")]

    cleaned_mp4s = [files.replace("\\", "/") for files in video_list]

    final_videos = [str(item) for item in cleaned_mp4s]

    #final_video_list = [items.replace("./RECORD/","./") for items in final_videos]
      
    # #return final_video_list
    # def videosListParser(list_video):
    #     for items in list_video:
    #         return items
    # return videosListParser(list_video=final_videos)
    #
    return final_videos


if __name__ == "__main__":
    PATH = "RECORD"
    VID = multipleVideoPlayingFunction(PATH)
    print(VID)



