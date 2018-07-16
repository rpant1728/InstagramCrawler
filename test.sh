echo "Query account 'instagram', download 20 photos and their captions"
python instagramcrawler.py -q 'instagram' -n 20

echo "Query account 'instagram', crawl followers and following usernames, download all posts and save in directory 'instagram/'"
python instagramcrawler.py -q 'instagram' -n -1 -t all -d ./instagram