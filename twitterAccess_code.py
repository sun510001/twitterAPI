import tweepy
from pathlib import Path
import time


class TwitterAccess(object):
    def s_access_token(self, key_flag, key_num):
        '''
        To get keys from ../twitterKey.txt and access the oauth
        '''
        if key_num == 0:
            key_path = Path("../twitterKey.txt")
        elif key_num == 1:
            key_path = Path("../twitterKey2.txt")
        #  print(key_num)
        key_list = []
        if key_path.exists() and key_flag == 0:
            with open(key_path, 'r') as f_key:
                for line in f_key.readlines():
                    if len(line.strip()) != 0:
                        key_list.append(line.strip())
            len_key = len(key_list)
            #  print(key_list, len_key)
        else:
            len_key = 0

        if len_key == 4:
            consumer_key = key_list[0]
            consumer_secret = key_list[1]
            access_token = key_list[2]
            access_token_secret = key_list[3]
        else:
            consumer_key = input("Please input the consumer_key: ")
            consumer_secret = input("Please input the consumer_secret: ")
            access_token = input("Please input the access_token: ")
            access_token_secret = input(
                "Please input the access_token_secret: ")
            try:
                with open(key_path, 'w') as w_key:
                    w_key.write(consumer_key + '\n')
                with open(key_path, 'a') as a_key:
                    a_key.write(consumer_secret + '\n')
                    a_key.write(access_token + '\n')
                    a_key.write(access_token_secret)
                #  print("Save the key to the local.")
            except BaseException:
                print(
                    "ERROR! Something wrong of creating or writing the twitterKey.txt!")
                time.sleep(2)

        # start access oauth and get api
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def get_tweets(self):
        key_flag = 0  # =1 When the key_list is 4 lines and it is a wrong key.
        key_num = 0
        api = self.s_access_token(key_flag, key_num)
        try:
            public_tweets = api.home_timeline()
            print("Get tweets successfully ... ")
            for each in public_tweets:
                print(each.text)
        except BaseException:
            print("ERROR! May be the key you inputted is wrong! \nPlease try again...")
            key_flag = 1
            #  s_access_token(key_flag)
            self.get_tweets(key_flag)


if __name__ == '__main__':
    # main function
    TwitterAccess().get_tweets()
