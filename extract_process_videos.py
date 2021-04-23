from skimage.metrics import structural_similarity as ssim
import cv2
import os
from pathlib import Path
import uuid

def remove_if_similar(imageA, imageB, percentile):
  s = ssim(imageA, imageB)
  if (s > percentile):
    return None
  return imageB

def check_folder_size(foldername):
  path, dirs, files = next(os.walk(foldername))
  file_count = len(files)
  if file_count < 6:
    return True
  return False


def dirs_to_frames(src, dst):
    empty_videos = []
    long_vidoes = {}

    if(os.path.exists(src) == False):
        print(src + " folder dosen't exist.")
    for subdir, dirs, files in os.walk(src):
        for dir_name in dirs:
            src_dir = src + "\\" + dir_name
            dst_dir = dst + "\\" + dir_name
            dir_to_frame(src_dir, dst_dir, empty_videos, long_vidoes)
    
    print("The following video files were empty:")
    for i in empty_videos:
        print(empty_videos)
    print("The following video files were unusually long and skipped")
    for video_name, frame_count in long_vidoes.items():
        print("name: {} frames: {}".format(video_name, frame_count))


def dir_to_frame(src, dst, empty_videos_list, long_vidoes_dict):
    print("Converting {} to frames.".format(src))
    for subdir, dirs, files2 in os.walk(src):    
        for directory in files2:
            file_path = os.path.join(subdir, directory)
            vidcap = cv2.VideoCapture(file_path)
            vid_length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            success,image = vidcap.read()

            dst_directory = dst + "\\" + directory
            # If video length is over 400 frames, the video is probably not a single hand sign and is skipped
            if(vid_length > 400):
                long_vidoes_dict[dst_directory] = vid_length
            else:
                # Ensures output directory exists
                Path(dst_directory).mkdir(parents=True, exist_ok=True)
                
                count = 0
                while success:
                    # save frame as JPEG file  
                    cv2.imwrite(dst_directory + "\\%d.jpg" % count, image)         
                    success, image = vidcap.read()
                    #print('Read a new frame: ', success)
                    count += 1
                # If it were an unreadable video file, it will be empty. Deletes empty output directory folder.
                if(count == 0):
                    empty_videos_list.append(dst_directory)
                    os.rmdir(dst_directory)
                

def remove_similar_start_end_imgs(rootdir, outputdir, percentile, original):
  print("Started Preprocessing " + rootdir + " with percentile : " + str(percentile))

  for subdir, dirs, files in os.walk(rootdir):
      for file_name in files:
          contrast = cv2.imread(os.path.join(subdir, file_name))
          contrast_gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
          # compare the images. end images are named a uuid to prevent overlap with final dataset
          removed = remove_if_similar(original, contrast_gray, percentile)
          if removed is not None:
              cv2.imwrite(outputdir + "/{}.jpg".format(uuid.uuid1()), contrast)
  
  if check_folder_size(outputdir):
      remove_similar_start_end_imgs(rootdir, outputdir, percentile + 0.01, original)

def remove_similarity_dirs(src, dst, percentile):
    for subdir, dirs, files in os.walk(src):
        for dir_name in dirs:
            src_dir = src + "\\" + dir_name
            dst_dir = dst + "\\" + dir_name
            remove_similarity_one_dir(src_dir, dst_dir, percentile)


def remove_similarity_one_dir(src, dst, percentile):
    for subdir, dirs, files in os.walk(src):
        for dir_name in dirs:
            src_dir = src + "\\" + dir_name
            dst_dir = dst + "\\" + dir_name
            for subdir, dirs, files2 in os.walk(src_dir): 
                start_img_sample = src_dir + "\\" + files2[0]

            original = cv2.imread(start_img_sample)
            original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            
            Path(dst_dir).mkdir(parents=True, exist_ok=True)
            
            remove_similar_start_end_imgs(src_dir, dst_dir, percentile, original_gray)


def process_all_dirs():
    video_input = "input_videos"

    frame_input = "frames"

    percentile = 0.90 #0.91 is optimal in most cases
    processed_frames = "processed_frames"
    # Takes ALL input vidoes from source and makes them into frames in dest
    dirs_to_frames(video_input, frame_input)
    # Removes similarity from ALL directories in input folder
    remove_similarity_dirs(frame_input, processed_frames, percentile)

def process_target_dir(target_dir):
    video_input_one_dir = "input_videos\\" + targeted_dir
    frame_input_one_dir = "frames\\" + targeted_dir
    processed_frames_one_dir = "processed_frames\\" + targeted_dir
    # Takes input vidoes in target directory and turns them into frames to dst
    empty_videos = []
    long_vidoes = {}
    dir_to_frame(video_input_one_dir, frame_input_one_dir, empty_videos, long_vidoes)
    
    # Removes similarity in targeted directory
    percentile = 0.90 #0.91 is optimal in most cases
    remove_similarity_one_dir(frame_input_one_dir, processed_frames_one_dir, percentile)

targeted_dir = "walk"

#process_all_dirs()
process_target_dir(targeted_dir)