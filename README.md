# s3-file-fetcher-gui

### setup

1. brew install python
2. python3 -m venv venv
3. source venv/bin/activate (for mac)
4. pip install -r requirements.txt
5. nano ~/.zshrc or nano ~/.bashrc
6. add aliases
   1. alias s3-dailyBucket="source /path/to/your/venv/bin/activate && python3 /path/to/your/script/dailyBucket.py" (full path)
   2. alias s3-storeBucket="source /path/to/your/venv/bin/activate && python3 /path/to/your/script/storeBucket.py" (full path)
7. source ~/.zshrc or source ~/.bashrc
8. add env vars in .env

Now you can use alias to fetch vehicle request raw response or vehicle data from s3

---

### example

- dailyBucket:
  -> s3-dailyBucket {environmentName} {date} "{url}" {url body}(optional)"
  -> s3-dailyBucket prod 20240821 "www.some-url.com"

- store bucket:
  -> s3-storeBucket {environmentName} "{storeId}"
  -> s3-storeBucket prod "ee315ac12567a2b44ae03fc30b093334"

---

environmentNames: dev, stage, prod

##### personal helper commands

pip freeze > requirements.txt

---

##### disclaimer

since this is small internal program intended to automate process i.e. speed things up:

- code is not written to be fabolous and reusable :D
- positional params used
