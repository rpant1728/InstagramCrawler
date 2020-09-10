# InstagramCrawler
A python script to crawl the Instagram profiles and scrape information (posts, followers, following, comment etc.)
Note - The crawler doesn't work any more, as the html tags for the elements have now been changed. The code template still remains the same.

**Login to crawl users with private profiles whom you follow**

To crawl followers/followings or private profiles of people you follow you will need to login with your Instagram credentials either by filling then in 'auth.json'.

Please copy the contents of 'auth.json.example', enter your credentials (username, password) and save it as 'auth.json'.

## Examples :

Download the first 100 photos, followers and followings list from username "instagram"

```
$ python3 InstagramCrawler.py -q 'instagram' -n 100 -t all
```

Download all photos from username "xyz" having a private profile (whom you follow), take login credentials from ./auth.json by default

```
$ python3 InstagramCrawler.py -q 'xyz' -n -1 -t posts -p private
```

Record all followers of the username "instagram", requires log in credentials from file ./auth.json

```
$ python3 InstagramCrawler.py -q 'instagram' -t 'followers' -a auth.json
```
## Full Usage :

'''
usage : InstagramCrawler.py [-h] [-d DIR] [-q QUERY] [-t CRAWL_TYPE] [-n NUMBER]  [-a AUTHENTICATION] [-p PROFILE_STATUS]
'''

- [-d DIR]: the directory to save crawling results, default is './Profiles/[query]'
- [-q QUERY] : username of profile you wish to crawl, e.g. 'instagram'
- [-t CRAWL_TYPE]: crawl_type, Options: 'posts | followers | following | details | all'
- [-n NUMBER]: number of posts, followers, or following to crawl, '0' by default, '-1' to crawl all
- [-a AUTHENTICATION]: path to a json file, which contains your instagram credentials, please see 'auth.json'
- [-l HEADLESS]: If set, script will be run as headless
- [-p PROFILE_STATUS]: profile security status, Options: 'public | private', authentication will be required if 'private'

## Requirements :

```
python 3.5
selenium 3.4
geckodriver
```
