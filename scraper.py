from Scweet.scweet import scrape
from Scweet.user import get_user_information
from argparse import ArgumentParser
from datetime import datetime
import pandas as pd
import numpy as np
import os
import platform
import winsound

GROUP = 31
CATEGORY = 'RBRD'
TOPIC = 'Leni cheated during the 2016 General Election'

def main():
    collector, since, until, keywords, hashtags = get_command_args()
    df = scrape(
        words=keywords,
        since=since,
        until=until,
        interval=1,
        hashtag=hashtags
    )

    notify_user()

    df = remove_unrelated_tweets(df, keywords, since, until)
    df = build_required_dataframe(df, collector, keywords)
    df = fill_user_information(df)

    save_as_csv(df, since, until)

    notify_user()

def get_command_args():
    parser = ArgumentParser()

    parser.description = \
        'This program automates the data collection for the CS 132 Project. \
        This automatically saves a CSV file (format: <SINCE_DATE>---<UNTIL_DATE>) \
        of the formed dataframe from scraped tweets.\
        Please place in double quotes the command argument value/s. \
        Example usage of this program: \
        python test.py -c "Marinas, Gabriel Kenneth" -s "2016-01-01" \
        -u "2016-03-1" -k "fakevp" "leni mandaraya" \
        -H "FakeVP" "ImpeachLeni"'

    parser.add_argument(
        '-c',
        '--collector',
        metavar='COLLECTOR_NAME',
        help='Your name. Format: <Last Name>, <First Name>, e.g. "Marinas, Gabriel Kenneth"',
        type=str,
        required=True
    )

    parser.add_argument(
        '-s',
        '--since',
        metavar='DATE',
        help='Start date of parsing. Format: YYYY-MM-DD',
        type=str,
        required=True
    )

    parser.add_argument(
        '-u',
        '--until',
        metavar='DATE',
        help='End date of parsing. Format: YYYY-MM-DD',
        type=str,
        required=True
    )

    parser.add_argument(
        '-k',
        '--keywords',
        nargs='+',
        metavar='keyword',
        help='Keywords used for scraping. You can specify many keywords, e.g. -k "fakevp" "leni mandaraya" "2016 election"',
        type=str,
        required=True
    )

    parser.add_argument(
        '-H',
        '--hashtags',
        nargs='+',
        metavar='hashtag',
        help='Hashtags used for scraping. You can specify many hashtags, e.g. -h "#FakeVP" "#ImpeachLeni" "#LeniResign"',
        type=str,
        required=True
    )

    args = parser.parse_args()

    collector: str = args.collector
    since: str = args.since
    until: str = args.until
    keywords: list[str] = args.keywords
    hashtags: list[str] = args.hashtags

    return (collector, since, until, keywords, hashtags)

def remove_unrelated_tweets(
        df: pd.DataFrame, 
        keywords: list[str], 
        since: str, 
        until: str) -> pd.DataFrame:
    tweets_removed = 0
    tweets_remaining = 0

    total_tweets = len(df)

    print('\nAfter scraping all tweets related to the keywords {} from {} up to {}, you will now remove all tweets that does not spread mis/disinformation about the topic "{}".\n'.format(keywords, since, until, TOPIC))
    for i, iterrow in enumerate(list(df.iterrows())):
        username = iterrow[1]['UserName']
        print('====================================================================')
        print('({}/{}) Tweet by {}:\n'.format(i+1, total_tweets, username))
        print(iterrow[1]['Text'])
        if len(iterrow[1]['Embedded_text']) > 0:
            print('\nHas an image/video attached: {}'.format(iterrow[1]['Embedded_text']))

        while True:
            ans = input('\nDiscard this tweet? [y/n]: ')

            if ans.lower() == 'y':
                df.drop(i, inplace=True)
                print('Discard tweet by {}.'.format(username))
                tweets_removed += 1
                break
            elif ans.lower() == 'n':
                print('Keep tweet by {}.'.format(username))
                tweets_remaining += 1
                break
            else:
                continue

        print('')

    print('Finished manual removal of unrelated tweets.')
    print('Total number of discard tweets: {}'.format(tweets_removed))
    print('Total number of remaining tweets: {}'.format(tweets_remaining))
    df.reset_index()
    return df

def build_required_dataframe(df: pd.DataFrame, collector_str: str, keywords_list: list[str]) -> pd.DataFrame:
    df_rows = len(df)

    identification = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    timestamp = np.full(
        (df_rows, ), 
        datetime.now().strftime("%m/%d/%Y %H:%M:%S"), 
        dtype=object
    )
    tweet_url = df['Tweet URL'].to_numpy(dtype=str)
    group = np.full(
        (df_rows, ),
        GROUP,
        dtype=object
    )
    collector = np.full(
        (df_rows, ),
        collector_str,
        dtype=object
    )
    category = np.full(
        (df_rows, ),
        CATEGORY,
        dtype=object
    )
    topic = np.full(
        (df_rows, ),
        TOPIC,
        dtype=object
    )
    keywords = np.full(
        (df_rows, ),
        ', '.join(keywords_list),
        dtype=object
    )
    account_handle = df['UserName'].to_numpy(dtype=str)
    account_name = df['UserScreenName'].to_numpy(dtype=str)
    account_bio = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    account_type = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    joined = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    following = np.zeros(
        (df_rows, ),
        dtype=int
    )
    followers = np.zeros(
        (df_rows, ),
        dtype=int
    )
    location = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    tweet = df['Text'].to_numpy(dtype=str)
    tweet_translated = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    tweet_type = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    date_posted = df['Timestamp'].to_numpy()
    screenshot = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    content_type = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    likes = df['Likes'].replace(r'^\s*$', 0, regex=True).to_numpy(dtype=int)
    replies = df['Comments'].replace(r'^\s*$', 0, regex=True).to_numpy(dtype=int)
    retweets = df['Retweets'].replace(r'^\s*$', 0, regex=True).to_numpy(dtype=int)
    quote_tweets = np.zeros(
        (df_rows, ),
        dtype=int
    )
    views = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    rating = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    reasoning = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    remarks = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    tweet_id = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    reviewer = np.full(
        (df_rows, ),
        '',
        dtype=object
    )
    review = np.full(
        (df_rows, ),
        '',
        dtype=object
    )

    data = {
        'ID': identification,
        'Timestamp': timestamp,
        'Tweet URL': tweet_url,
        'Group': group,
        'Collector': collector,
        'Category': category,
        'Topic': topic,
        'Keywords': keywords,
        'Account handle': account_handle,
        'Account name': account_name,
        'Account bio': account_bio,
        'Account type': account_type,
        'Joined': joined,
        'Following': following,
        'Followers': followers,
        'Location': location,
        'Tweet': tweet,
        'Tweet Translated': tweet_translated,
        'Tweet Type': tweet_type,
        'Date posted': date_posted,
        'Screenshot': screenshot,
        'Content type': content_type,
        'Likes': likes,
        'Replies': replies,
        'Retweets': retweets,
        'Quote Tweets': quote_tweets,
        'Views': views,
        'Rating': rating,
        'Reasoning': reasoning,
        'Remarks': remarks,
        'Tweet ID': tweet_id,
        'Reviewer': reviewer,
        'Review': review
    }

    df = pd.DataFrame(data=data)

    return df

def fill_user_information(df: pd.DataFrame) -> pd.DataFrame:
    print('\nStarting to scrape user information...')
    for index, iterrow in enumerate(list(df.iterrows())):
        account_handle = iterrow[1]['Account handle']
        print('\nScraping user information for {}...'.format(account_handle))

        tries = 1
        max_tries = 10
        users_info = {}

        while tries <= max_tries:
            print('{}/10 attempts made.'.format(tries))
            users_info = get_user_information([account_handle])
            if users_info is None:
                print('Failed to get user information. Trying again...')
                tries += 1
                continue
            break

        if tries > max_tries:
            print('Failed to get user information for {}. Hanapin mo na lang sa twitter HAHAHA.'.format(account_handle))
            continue

        assert users_info is not None, 'users_info is None'

        print(users_info)

        following, followers, join_date, birthday, location, website, desc = \
            users_info[account_handle]
        
        # convert join date to mm/yyyy format
        try:
            join_date = join_date.split(' ')[1:]
            join_date = ' '.join(join_date)
            join_date = datetime.strptime(join_date, '%B %Y')
            join_date = join_date.strftime('%m/%Y')
            print('join date:', join_date)
        except ValueError:
            join_date = ''
        
        df.loc[index, 'Account bio'] = desc
        df.loc[index, 'Joined'] = join_date
        df.loc[index, 'Following'] = following
        df.loc[index, 'Followers'] = followers
        df.loc[index, 'Location'] = location

    return df
    
def save_as_csv(df: pd.DataFrame, since: str, until: str):
    csv_filename = f"{since}---{until}.csv"
    csv_filename_path = os.path.join(os.path.dirname(__file__), csv_filename)
    try:
        os.remove(csv_filename_path)
    except FileNotFoundError:
        pass

    df.to_csv(csv_filename, index=False)

# Create a cross-platform function that notifies the user that the program is done
# by creating a sound. Do it for Windows, Linux, and Mac. Run it three times.
# Use a python stdlib to find the current OS.
def notify_user():
    # Windows
    if platform.system() == 'Windows':
        for _ in range(3):
            winsound.Beep(1000, 1000)
    # Linux
    elif platform.system() == 'Linux':
        for _ in range(3):
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (1, 1000))
    # Mac
    elif platform.system() == 'Darwin':
        for _ in range(3):
            os.system('say "A task has been completed."')
    else:
        for _ in range(3):
            print('\a')


if __name__ == '__main__':
    main()
