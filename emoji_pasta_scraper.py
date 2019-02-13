import praw
import os
import logging
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class EmojiPastaScraper():

    def __init__(self):
        self.REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
        self.REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
        self.REDDIT_USERNAME = os.environ['REDDIT_USERNAME']
        self.REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
        self.USER_AGENT= os.environ['USER_AGENT']
        self.SUBREDDIT_NAME = os.environ['SUBREDDIT_NAME']

        self.reddit = None
        self.subreddit = None

        self.init_reddit()

    def init_reddit(self):
        session = requests.Session()
        session.verify = False ## ignore cert issues 

        self.reddit = praw.Reddit(client_id=self.REDDIT_CLIENT_ID,
                    			  client_secret=self.REDDIT_CLIENT_SECRET,
                    			  user_agent=self.USER_AGENT,
                    			  username=self.REDDIT_USERNAME,
                    			  password=self.REDDIT_PASSWORD,
                                  requestor_kwargs={'session': session})

        self.subreddit = self.reddit.subreddit(self.SUBREDDIT_NAME)

    def main(self):
        f = open("emojipasta.txt", "a")
        count = 0

        for submission in self.subreddit.new(limit=10000):
            text = submission.selftext.replace("\n", " ")
            text += "\n"
            f.write(text)
            count += 1

        f.close()
        logging.info("Scraped " + str(count) + " emoji pastas 😂👌")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    emojiPastaScraper = EmojiPastaScraper()
    emojiPastaScraper.main()
