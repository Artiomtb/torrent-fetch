# torrent-fetch

##Console tool to find and download torrent files.

###Requirements:
* Python2
* requests library (http://docs.python-requests.org/en/master/) - ```pip install requests```
* texttable library (https://pypi.python.org/pypi/texttable/) - ```pip install texttable```

###Usage:

```python torrent-fetch.py <search query>```.

*Example:* ```python torrent-fetch.py big bang theory```

*Note: if you entering some restricted for bash command parameters symbols (like apostrophe) you should escape it.*

###Better usage:
1.  Add alias string for python torrent-fetch.py to file ~/.bash_aliases (create if not exists): ```alias torrent-fetch='python <dir with torrent.py>/torrent-fetch.py'```
2. ```torrent-fetch <search query>```.

*Example:* ```torrent-fetch big bang theory```
