#! python

import os
import subprocess

# Function to convert a video
def convert_video(input_file, output_file, output_resolution):
    process = subprocess.Popen(["ffmpeg", "-i", input_file, "-vf", f"scale={output_resolution}", "-c:a", "copy", output_file], stderr=subprocess.PIPE, universal_newlines=True)

    for line in process.stderr:
        line = line.strip()
        if "frame=" in line and ("fps=" in line or "fps =" in line) and "time=" in line:
            frame_info_parts = line.split()
            for part in frame_info_parts:
                if part.startswith("frame="):
                    frame_info = part.replace("frame=", "")
                    if frame_info.isdigit():
                        frames_done = int(frame_info)
                        percent_done = int((frames_done / total_frames) * 100)
                        print(f"\rConverting: {input_file} - {percent_done}% done", end="")
                        break

    process.wait()
    print(f"\rConverting: {input_file} - 100% done")



# Get the current directory name
current_directory_name = os.path.basename(os.getcwd())

# Create a directory with the current directory's name within Downloads
output_directory = os.path.join(r"C:\Users\Admin\Downloads", current_directory_name)
os.makedirs(output_directory, exist_ok=True)


# Ask the user for the desired output resolution
output_resolution = input("Select output resolution (480p, 720p, 1080p): ").strip().lower()

# Validate user input and set resolution accordingly
if output_resolution == "480p":
    output_resolution = "854x480"
elif output_resolution == "720p":
    output_resolution = "1280x720"
elif output_resolution == "1080p":
    output_resolution = "1920x1080"
else:
    print("Invalid input. Using default resolution: 480p")
    output_resolution = "854x480"

# Loop through video files in the current directory and its subdirectories
for root, _, files in os.walk('.'):
    for input_file in files:
        if input_file.lower().endswith(".mp4"):
            input_file_path = os.path.join(root, input_file)
            output_file_dir = os.path.join(output_directory, os.path.relpath(root, '.'))  # Preserve folder structure
            os.makedirs(output_file_dir, exist_ok=True)
            output_file = os.path.join(output_file_dir, os.path.splitext(input_file)[0] + f".mp4")
            total_frames = int(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames", "-of", "default=nokey=1:noprint_wrappers=1", input_file_path], universal_newlines=True))
            convert_video(input_file_path, output_file, output_resolution)

print(f"Conversion of all video files to {output_resolution} completed. Converted videos are in the '{output_directory}' directory.")
