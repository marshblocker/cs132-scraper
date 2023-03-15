### Before running this program:

1. Install these libraries Scweet, pandas, numpy
    - for Scweet: https://github.com/Altimis/Scweet
2. The Scweet is not currently maintained and the Tweet text data is not
   properly scraped due to Twitter UI change. To fix this, in VS Code (other
   code editor have this feature too), right click the `scrape()` function
   in the code and click `Go to Definition`. You will be directed to `scweet.py`.
   Within the directory of `scweet.py`, you will see `utils.py`, go that file.
   Replace line 47 with
   ```python
   text = card.find_element_by_xpath('.//div[@data-testid="tweetText"]').text
   ```

### How to run:
```
usage: scraper.py [-h] -c COLLECTOR_NAME -s DATE -u DATE -k keyword [keyword ...]

This program automates the data collection for the CS 132 Project. This automatically saves a CSV file (format:
<SINCE_DATE>---<UNTIL_DATE>) of the formed dataframe from scraped tweets. Please place in double quotes the command
argument value/s. Example usage of this program: python test.py -c "Marinas, Gabriel Kenneth" -s "2016-01-01" -u
"2016-03-1" -k "fakevp" "leni mandaraya" "2016 election"

options:
  -h, --help            show this help message and exit
  -c COLLECTOR_NAME, --collector COLLECTOR_NAME
                        Your name. Format: <Last Name>, <First Name>, e.g. "Marinas, Gabriel Kenneth"
  -s DATE, --since DATE
                        Start date of parsing. Format: YYYY-MM-DD
  -u DATE, --until DATE
                        End date of parsing. Format: YYYY-MM-DD
  -k keyword [keyword ...], --keywords keyword [keyword ...]
                        Keywords used for scraping. You can specify many keywords, e.g. -k "fakevp" "leni mandaraya" "2016
                        election"
```