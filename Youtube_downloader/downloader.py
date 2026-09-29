import os
import yt_dlp

def download_video(url, output_path=".", audio_only=False, progress_callback=None, is_cancelled_callback=None):
    """
    Downloads streams from YouTube. Reports live speed and percentage.
    Monitors is_cancelled_callback to abort downloads cleanly mid-stream.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Internal hook to intercept yt-dlp's data stream
    def yt_dlp_hook(d):
        # Check if the user hit 'Cancel' at any point during downloading or processing
        if is_cancelled_callback and is_cancelled_callback():
            raise yt_dlp.utils.DownloadCancelled("User cancelled the download.")

        if progress_callback and d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            
            if total > 0:
                percentage = downloaded / total
                speed_bytes = d.get('speed', 0)
                if speed_bytes:
                    speed_mb = speed_bytes / (1024 * 1024)
                    speed_str = f"{speed_mb:.1f} MB/s"
                else:
                    speed_str = "Calculating speed..."
                
                progress_callback(percentage, f"Downloading: {int(percentage * 100)}% ({speed_str})")
        
        elif progress_callback and d['status'] == 'finished':
            progress_callback(1.0, "Download complete! Processing/Stitching files...")

    # Configuration options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,  
        'progress_hooks': [yt_dlp_hook],  
    }

    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Check cancel status right before network resolution starts
            if is_cancelled_callback and is_cancelled_callback():
                return {"success": False, "message": "Download cancelled by user."}
                
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            
            ydl.download([url])
            
            file_type = "MP3 Audio" if audio_only else "HD Video"
            return {
                "success": True,
                "title": video_title,
                "message": f"Successfully downloaded ({file_type}):\n{video_title}"
            }

    except yt_dlp.utils.DownloadCancelled:
        return {"success": False, "message": "Download cancelled by user."}
    except yt_dlp.utils.DownloadError as e:
        return {"success": False, "message": f"YouTube Error: Invalid link or restricted video.\nDetails: {e}"}
    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {e}"}
