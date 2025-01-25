import os
import logging
import argparse
from typing import Optional, Dict, List
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from tools.llm_api import query_llm

logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from YouTube URL."""
    try:
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
            elif parsed_url.path.startswith('/v/'):
                return parsed_url.path.split('/')[2]
        elif parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        return None
    except Exception as e:
        logger.error(f"Error extracting video ID: {str(e)}")
        return None

def get_video_transcript(video_id: str) -> Optional[List[Dict]]:
    """Get video transcript."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        logger.error(f"Error fetching transcript: {str(e)}")
        return None

def format_transcript(transcript: List[Dict]) -> str:
    """Format transcript into text."""
    if not transcript:
        return ""
    
    formatted_text = ""
    for entry in transcript:
        formatted_text += f"{entry['text']}\n"
    return formatted_text.strip()

def summarize_transcript(transcript_text: str) -> Optional[str]:
    """Use LLM to summarize video content in Chinese."""
    if not transcript_text:
        return None
    
    try:
        prompt = f"""请用中文总结以下视频内容的要点。即使原文是英文，也请用中文回答：

{transcript_text}

请提供一个结构清晰的中文总结。"""
        summary = query_llm(prompt)
        return summary
    except Exception as e:
        logger.error(f"Error summarizing transcript: {str(e)}")
        return None

def process_youtube_url(url: str, summarize: bool = False) -> Optional[str]:
    """Process YouTube URL and return transcript text or summary."""
    video_id = extract_video_id(url)
    if not video_id:
        logger.error(f"Invalid YouTube URL: {url}")
        return None
    
    transcript = get_video_transcript(video_id)
    if not transcript:
        return None
    
    transcript_text = format_transcript(transcript)
    if summarize:
        return summarize_transcript(transcript_text)
    return transcript_text

def main():
    parser = argparse.ArgumentParser(description='Extract and summarize YouTube video transcripts')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--output', help='Output file path for the transcript')
    parser.add_argument('--summarize', action='store_true', help='Summarize the video content')
    args = parser.parse_args()
    
    result = process_youtube_url(args.url, args.summarize)
    if result:
        if args.output:
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"{'Summary' if args.summarize else 'Transcript'} saved to {args.output}")
        else:
            print(result)

if __name__ == '__main__':
    main()