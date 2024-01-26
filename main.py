from moviepy.editor import *
import reddit, screenshot, time, subprocess, random, configparser, sys, math, youtube
from os import listdir
from os.path import isfile, join

def clearFolderContent(folder_path):
    try:
        # Check if the folder exists
        if os.path.exists(folder_path):
            # Remove all files in the folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

            print(f"The content of the folder {folder_path} has been cleared.")
        else:
            print(f"The folder {folder_path} does not exist.")

    except Exception as e:
        print(f"An error occurred: {e}")

def createVideo():
    config = configparser.ConfigParser()
    config.read('config.ini')
    outputDir = config["General"]["OutputDirectory"]

    startTime = time.time()

    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if (len(sys.argv) == 2):
        script = reddit.getContentFromId(outputDir, sys.argv[1])
    else:
        postOptionCount = int(config["Reddit"]["NumberOfPostsToSelectFrom"])
        script = reddit.getContent(outputDir, postOptionCount)
    fileName = script.getFileName()

    # Create screenshots
    screenshot.getPostScreenshots(fileName, script)

    # Setup background clip
    bgDir = config["General"]["BackgroundDirectory"]
    # bgPrefix = config["General"]["BackgroundFilePrefix"]
    
    bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f))]
    bgCount = len(bgFiles)
    bgIndex = random.randint(0, bgCount-1)
    backgroundVideo = VideoFileClip(
        filename=f"{bgDir}/{bgFiles[bgIndex]}", 
        audio=False)
    startPoint = int(script.getDuration())+1
    endPoint = int(backgroundVideo.duration)
    randomVideoPoint = random.randint(startPoint, endPoint)
    backgroundVideo = backgroundVideo.subclip(randomVideoPoint - script.getDuration(), randomVideoPoint)
    backgroundVideo = backgroundVideo.fx(vfx.resize,(720,1280),width= 720)
    w, h = backgroundVideo.size

    bgAudDir = config["General"]["BackgroundAudioDirectory"]
    bgAudFiles = [f for f in listdir(bgAudDir) if isfile(join(bgAudDir, f))]
    bgCount = len(bgFiles)
    bgAudioIndex = random.randint(0, bgCount-1)
    bgAudClip = AudioFileClip(f"{bgAudDir}/{bgAudFiles[bgAudioIndex]}")
    startPoint = int(script.getDuration())+1
    endPoint = int(bgAudClip.duration)
    randomAudioPoint = random.randint(startPoint, endPoint)
    bgAudClip = bgAudClip.subclip(randomAudioPoint - script.getDuration(), randomAudioPoint)

    def __createClip(screenShotFile, audioClip, marginSize):
        imageClip = ImageClip(
            screenShotFile,
            duration=audioClip.duration
            ).set_position(("center", "center"))
        imageClip = imageClip.resize(width=(w-marginSize))
        videoClip = imageClip.set_audio(audioClip)
        videoClip.fps = 1
        return videoClip

    # Create video clips
    print("Editing clips together...")
    clips = []
    marginSize = int(config["Video"]["MarginSize"])
    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize))
    for comment in script.frames:
        clips.append(__createClip(comment.screenShotFile, comment.audioClip, marginSize))

    # Merge clips into single track
    contentOverlay = concatenate_videoclips(clips).set_position(("center", "center"))

    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay], 
        size=backgroundVideo.size).set_audio(CompositeAudioClip([contentOverlay.audio,bgAudClip.volumex(0.5)]))
    final.duration = script.getDuration()
    final.set_fps(backgroundVideo.fps)

    print("Rendering final video...")
    bitrate = config["Video"]["Bitrate"]
    threads = config["Video"]["Threads"]
    outputFile = f"{outputDir}/{fileName}.mp4"
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate,
    )
    print(f"Video completed in {time.time() - startTime}")

    # Preview in VLC for approval before uploading
    # if (config["General"].getboolean("PreviewBeforeUpload")):
    #     vlcPath = config["General"]["VLCPath"]
    #     print('vlcPath- ', vlcPath, ' ,outputFile-', outputFile)
    #     p = subprocess.Popen([vlcPath, outputFile])
    #     print("Waiting for video review. Type anything to continue")
    #     wait = input()

    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")
    print("Uploading video...")
    youtube.uploadVideo(outputFile, script.title)
    # print("Uploaded")

if __name__ == "__main__":
    createVideo()
    clearFolderContent('Screenshots')
    clearFolderContent('Voiceovers')
    # clearFolderContent('OutputVideos')

