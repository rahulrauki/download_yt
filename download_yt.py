from pytube import YouTube, Playlist
from extract_yt_links import extract_links
import argparse, re

def _download_video(link, success):
    try:
        print(f"Starting to download : {link}")
        YouTube(link).streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().download()
        print("Download completed successfully, going forward !!!")
        success[0] += 1
    except Exception as e:
        print(f"Error downloading : {link} : {e}")
    print(" - - - - - - - - - - - - - - - - - - - - - - - - ")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Absolute file path")
    parser.add_argument("start", help="Start number of video to extract")
    parser.add_argument("end", help="End number of video to extract")
    args = parser.parse_args()
    file_path = args.input
    start, end  = int(args.start), int(args.end)
    playlist_pattern = re.compile(r".*\bplaylist\b.*")

    if not start < end: print(f"Start should be less than End !!!")
    link_list = extract_links(file_path, output=False)
    success, length, pl_videos = [0], len(link_list), 0
    if end > length and start > length:
        print(f"The start number is greater than the number of videos present, enter a value lesser than {length}")
    elif end < length:
        length = end
        
    for link in link_list[start - 1 : length]:
        if playlist_pattern.match(link):
            print(f"Starting to download playlist : {link}")
            urls = Playlist(link).video_urls
            pl_videos += len(urls)
            for url_link in urls:
                _download_video(url_link, success)
        else: _download_video(link, success)
    print("################################")    
    print(f"Downloaded {success[0]} / {length} videos found in the file !!!")

if __name__ == "__main__":
    main()