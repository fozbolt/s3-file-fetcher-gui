# s3-file-fetcher-gui

### setup

1. brew install python
2. python3 -m venv venv
3. source venv/bin/activate (for mac)
4. pip install -r requirements.txt
5. nano ~/.zshrc or nano ~/.bashrc
6. add aliases (activate virtual environment and run given script in it)
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

##### creating executable file

1. Install `auto-py-to-exe`.
2. Run `auto-py-to-exe` to launch the GUI.
3. Select your script, choose "One File", add an icon (optional), and click "Convert".
4. Add .env files (prod,stage,dev)
   - GUI -> additional files (doesn't show .env files so upload readme for example and then change name)
   - CMD: pyinstaller --noconfirm --onedir --windowed --icon "/Users/{user name}/Downloads/60159_analysis_check_review_search_search docs_icon.ico" --add-data "/Users/{user name}/Projects/s3-file-fetcher-gui/.env.prod:." --add-data "/Users/{user name}/Projects/s3-file-fetcher-gui/.env.stage:." --add-data "/Users/{user name}/Projects/s3-file-fetcher-gui/.env.prod:." "/Users/{user name}/Projects/s3-file-fetcher-gui/app.py"
5. Done! Your `.exe` is ready in the `dist` folder.

##### personal helper commands

pip freeze > requirements.txt

---

##### disclaimer

since this is small internal program intended to automate process i.e. speed things up:

- code is not written to be fabolous and reusable :D
- positional params used
