import unittest
from unittest.mock import patch
from tools.youtube_tool import (
    extract_video_id,
    get_video_transcript,
    format_transcript,
    process_youtube_url
)

class TestYouTubeTool(unittest.TestCase):
    def test_extract_video_id(self):
        # Test standard YouTube URL
        self.assertEqual(
            extract_video_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            'dQw4w9WgXcQ'
        )
        
        # Test short YouTube URL
        self.assertEqual(
            extract_video_id('https://youtu.be/dQw4w9WgXcQ'),
            'dQw4w9WgXcQ'
        )
        
        # Test invalid URLs
        self.assertIsNone(extract_video_id('https://example.com'))
        self.assertIsNone(extract_video_id('not a url'))
        self.assertIsNone(extract_video_id(''))
    
    @patch('tools.youtube_tool.YouTubeTranscriptApi')
    def test_get_video_transcript(self, mock_api):
        # Test successful transcript fetch
        mock_transcript = [{'text': 'Hello', 'start': 0.0, 'duration': 1.0}]
        mock_api.get_transcript.return_value = mock_transcript
        
        result = get_video_transcript('test_video_id')
        self.assertEqual(result, mock_transcript)
        mock_api.get_transcript.assert_called_once_with('test_video_id')
        
        # Test failed transcript fetch
        mock_api.get_transcript.side_effect = Exception('Transcript not available')
        result = get_video_transcript('test_video_id')
        self.assertIsNone(result)
    
    def test_format_transcript(self):
        # Test with valid transcript
        transcript = [
            {'text': 'Hello', 'start': 0.0, 'duration': 1.0},
            {'text': 'World', 'start': 1.0, 'duration': 1.0}
        ]
        expected = 'Hello\nWorld'
        self.assertEqual(format_transcript(transcript), expected)
        
        # Test with empty transcript
        self.assertEqual(format_transcript([]), '')
        self.assertEqual(format_transcript(None), '')
    
    @patch('tools.youtube_tool.get_video_transcript')
    @patch('tools.youtube_tool.extract_video_id')
    def test_process_youtube_url(self, mock_extract, mock_get_transcript):
        # Test successful processing
        mock_extract.return_value = 'test_video_id'
        mock_get_transcript.return_value = [
            {'text': 'Hello', 'start': 0.0, 'duration': 1.0},
            {'text': 'World', 'start': 1.0, 'duration': 1.0}
        ]
        
        result = process_youtube_url('https://youtube.com/watch?v=test')
        self.assertEqual(result, 'Hello\nWorld')
        
        # Test invalid URL
        mock_extract.return_value = None
        result = process_youtube_url('invalid_url')
        self.assertIsNone(result)
        
        # Test transcript fetch failure
        mock_extract.return_value = 'test_video_id'
        mock_get_transcript.return_value = None
        result = process_youtube_url('https://youtube.com/watch?v=test')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()