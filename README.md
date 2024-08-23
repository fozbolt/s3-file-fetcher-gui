# s3-file-fetcher-gui

1. brew install python
2. python3 -m venv venv
3. source venv/bin/activate (for mac)
4. pip install -r requirements.txt
5. nano ~/.zshrc or nano ~/.bashrc
6. add aliases
   1. alias s3-dailyBucket="source /path/to/your/venv/bin/activate && python3 /path/to/your/script/dailyBucket.py" (full path)
   2. alias s3-storeBucket="source /path/to/your/venv/bin/activate && python3 /path/to/your/script/storeBucket.py" (full path)
7. source ~/.zshrc or source ~/.bashrc

Now you can use alias to fetch raw response
example: s3-dailyBucket "{url}" {date} "{url body}(optional)"
example: s3-dailyBucket "https://www.finn.no/car/used/ad.html?finnkode=363567021" 20240821

example: example: s3-storeBucket "{storeId}"
example: example: s3-storeBucket "ee315ac12567a2b44ae03fc30b093334"

### personal helper commands

pip freeze > requirements.txt
