from twitterAccess_code import TwitterAccess
import tweepy
import time
from pathlib import Path
import re

'''
1. Changing search_tweets.count to change the number of tweets you want to search
in one page. max = 100
2. Changing search_tweets.pages to change how many pages the tweets you want to
search. default = 10000
3. 'q' is the keyword you want to search.
'''


def find_last_line(file_path):
    with open(file_path, 'rb') as f:
        off = -50
        while True:
            f.seek(off, 2)
            lines = f.readlines()
            if len(lines) >= 2:
                last_line = lines[-1]
                break
            off *= 2
    return last_line


def search_tweets(search_word, key_flag):
    api = TwitterAccess()
    api2 = api.s_access_token(key_flag, 1)
    #  try:
    #  search_status = api2.search(search_word, result_type='recent',
    #  count=10)
    stop_flag = 0
    tweet_number = 0
    last_id = 0
    last_num = 0
    RT_counter = 0
    path = "../tweettext.txt"
    log_path = "../log.txt"

    check_file = Path(path)
    print("finding the file {}...".format(path))
    if check_file.exists():
        print("File exist, write after the last line.")
        temp_id = re.search(r'\|(.*?)\|(.*?)\|', str(find_last_line(path)))
        #  print("..", temp_id.group(2))
        if temp_id:
            last_num = int(temp_id.group(1)) + 1
            last_id = temp_id.group(2)
            print("Start at number:", last_num, "id:", last_id)
            tweet_number = last_num
        else:
            print("Something wrong, check", path)
    else:
        print("File is not exist, create the new file.")

    for search_status in tweepy.Cursor(api2.search, q=search_word,
                                       #  result_type='recent',
                                       tweet_mode='extended',
                                       lang='en',
                                       max_id=str(int(last_id) - 1),
                                       count=100).pages(10000000000):
        #  print("Get tweets successfully ... \n\n")
        print(search_status)

        with open(path, "a") as file_text:
            for i in range(0, len(search_status)):
                s_temp_text = search_status[i].full_text.replace("\n", "<br>")
                if re.match(r'^RT', s_temp_text):
                    RT_counter += 1
                else:
                    file_text.write("|{2}|{1}|{0}\n".format(
                        s_temp_text,
                        search_status[i].id,
                        tweet_number + 1))

                #  print("/*{2}*{1}*/{0}".format(
                #  s_temp_text,
                #  search_status[i].id,
                #  tweet_number + 1))
                tweet_number += 1
        time.sleep(2)
        stop_flag += 1
        if stop_flag > 150:
            with open(log_path, "a") as f_log:
                f_log.write(
                    "[{}]In sleeping...\n".format(
                        time.strftime(
                            "%Y-%m-%d %H:%M:%S",
                            time.localtime())))
            time.sleep(60 * 17)
            stop_flag = 0
        with open(log_path, "a") as f_log:
            f_log.write(
                "[{0}]Totally deleted useless tweets {1}\n".format(
                    time.strftime(
                        "%Y-%m-%d %H:%M:%S",
                        time.localtime()),
                    RT_counter))

    #  except BaseException:
    #  pass
    #  print("stop at page:"+)
    #  print("ERROR! May be the key you inputted is wrong! \nPlease try again...")
    #  key_flag = 1
    #  #  api2=api.s_access_token(key_flag)
    #  search_tweets(searchword, key_flag)


if __name__ == '__main__':
    key_flag = 0  # =1 When the key_list is 4 lines or it is a wrong key.
    # search test
    q = "#sarcasm OR #irony"
    #  q = "#皮肉"
    search_tweets(q, key_flag)
