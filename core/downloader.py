"""
Module responsible for handling media downloads from external sources.
"""
import os
import yt_dlp

class DownloadError(Exception):
    """Custom exception raised for download-related errors."""
    pass

class AudioDownloader:
    """Handles downloading and extracting audio from URLs."""
    
    @staticmethod
    def download_from_youtube(url: str, output_dir: str) -> str:
        """
        Downloads the best audio stream from a given URL and converts it to MP3.
        
        Args:
            url (str): The video URL.
            output_dir (str): The directory where the file will be temporarily saved.
            
        Returns:
            str: The absolute path to the downloaded MP3 file.
            
        Raises:
            DownloadError: If the download or extraction fails.
        """
        out_tmpl = os.path.join(output_dir, 'yt_audio_%(id)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': out_tmpl,
            'quiet': True,
            'noplaylist': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                expected_filename = ydl.prepare_filename(info)
                final_filename = os.path.splitext(expected_filename)[0] + '.mp3'
                return final_filename
        except yt_dlp.utils.DownloadError as e:
            raise DownloadError(f"Failed to download media. Check the URL. Details: {str(e)}")