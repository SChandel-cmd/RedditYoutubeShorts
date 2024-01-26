
# Reddit Video Generator

*This project is based on this [original project](https://github.com/Shifty-The-Dev/RedditVideoGenerator)*
*More information is available in [this video](https://youtu.be/ZmSb3LZDdf0)*

---
This program generates a .mp4 video automatically by querying the top post on the
r/askreddit subreddit, and grabbing several comments. The workflow of this program is:
- Install dependencies
- Make a copy of config.example.ini and rename to config.ini
- Make folders named BackgroundMusic, BackgroundVideos, OutputVideos, Screenshots, Voiceovers.
- Put random music and videos in the first 2 folders which you want to get used in the shorts.
- Register with Reddit to create an application [here](https://www.reddit.com/prefs/apps/) and copy the credentials
- Use the credentials from the previous step to update config.ini (lines 22 -> 24)

I have made minor quality of life modifications to this project to ease the input process and to put background music in the generated videos.
I have also made it possible for the user to automatically upload the generated videos onto their YouTube channel by using the [YouTube Data API](https://developers.google.com/youtube/v3)

- Simply login to your [GCP console](https://console.cloud.google.com)
- Create a project
- Enable the Youtube Data API and create OAuth credentials for the same.
- Download the client_secret.json file and put the path in config/ini along with the YouTube Data API Key.

Now, you can run `python main.py` to be prompted for which post to choose. Alternatively,
you can run `python main.py <reddit-post-id>` to create a video for a specific post.
