import unittest
from unittest.mock import patch, MagicMock
from reddit_scraper import fetch_user_content

class TestRedditScraper(unittest.TestCase):
    @patch('reddit_scraper.praw.Reddit')
    def test_fetch_user_content(self, mock_reddit):
        # Mock Redditor and submissions/comments
        mock_user = MagicMock()
        mock_submission = MagicMock()
        mock_submission.title = 'Test Title'
        mock_submission.selftext = 'Test Body'
        mock_submission.subreddit = 'testsub'
        mock_submission.url = 'http://reddit.com/test'
        mock_submission.permalink = '/r/testsub/comments/1'
        mock_submission.created_utc = 1700000000
        mock_user.submissions.new.return_value = [mock_submission]
        mock_comment = MagicMock()
        mock_comment.body = 'Test Comment'
        mock_comment.subreddit = 'testsub'
        mock_comment.permalink = '/r/testsub/comments/2'
        mock_comment.created_utc = 1700000001
        mock_user.comments.new.return_value = [mock_comment]
        mock_reddit.return_value.redditor.return_value = mock_user

        data = fetch_user_content('testuser', limit=1)
        self.assertEqual(len(data['posts']), 1)
        self.assertEqual(len(data['comments']), 1)
        self.assertEqual(data['posts'][0]['title'], 'Test Title')
        self.assertEqual(data['comments'][0]['body'], 'Test Comment')

if __name__ == '__main__':
    unittest.main() 