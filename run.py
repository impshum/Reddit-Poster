import praw
import schedule
from time import sleep
import configparser


config = configparser.ConfigParser()
config.read('conf.ini')
client_id = config['LOGIN']['client_id']
client_secret = config['LOGIN']['client_secret']
reddit_user = config['LOGIN']['reddit_user']
reddit_pass = config['LOGIN']['reddit_pass']
target_subreddit = config['POST']['subreddit']
post_title = config['POST']['post_title']
post_body = config['POST']['post_body']
times = config.items('TIMES')
sticky_id = ''

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='Reddit Poster (by /u/impshum)',
                     username=reddit_user,
                     password=reddit_pass)


def set_sticky_id(id):
    global sticky_id
    sticky_id = id


def set_sticky(id):
    submission = reddit.submission(id=id)
    submission.mod.sticky()


def delete_sticky():
    reddit.submission(id=sticky_id).delete()


def post(t):
    delete_sticky()
    id = reddit.subreddit(target_subreddit).submit(
        title=post_title, selftext=post_body)
    set_sticky_id(id)
    set_sticky(id)
    print(f'Posted {t}')


def main():
    for time in times:
        t = time[1]
        schedule.every().day.at(t).do(post, t)
        print(f'Scheduled post for {t}')

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
