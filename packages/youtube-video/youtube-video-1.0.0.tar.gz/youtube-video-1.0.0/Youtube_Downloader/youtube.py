from pytube import YouTube
class download:
    def __init__(self):
        print("Hello Users")

    def Download_video_in_360_resolution(self,link,path):
        yt = YouTube(link)
        yt.streams.filter(res="360p").first().download(path)



d = download()
d.Download_video_in_360_resolution('https://www.youtube.com/watch?v=RiWqigGW9cA&t=137s','D:\\')
