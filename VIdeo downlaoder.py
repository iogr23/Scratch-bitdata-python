import yt_dlp

def download_video(url, path='.'):
    ydl_opts = {
        'outtmpl': f'{path}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    path = input("Enter the download path (leave empty for current directory): ")

    download_video(url, path if path else '.')
