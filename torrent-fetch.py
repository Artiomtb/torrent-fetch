#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import requests
import urllib
import re
import texttable
import sys

if len(sys.argv) < 2:
    print('Specify search query first. Like \'torrent-fetch big bang theory\'')
else:
    search_query = ' '.join(sys.argv[1:])

    RUTOR_DOMAIN = 'http://xrutor.org'
    RUTOR_SEARCH = '/search/0/0/000/8/'  # default 1 page and sorted by size

    PROGRAM_TO_OPEN = 'transmission-gtk'

    url = RUTOR_DOMAIN + RUTOR_SEARCH + urllib.quote_plus(search_query)

    torrents = {}

    get = requests.get(url)
    html = get.content

    rows_pattern = re.compile('<tr class="(?:gai|tum)">(.+?)<\/tr>')
    rows = re.findall(rows_pattern, html)
    index = 1
    for row in rows:
        href_p = re.compile('<a href="(.+?)">(.+?)</a>')
        href = re.findall(href_p, row)[0]
        id = re.findall(re.compile('/torrent/(\d+)/'), href[0])[0]
        download_link = RUTOR_DOMAIN + '/parse/d.rutor.org/download/' + id
        name = href[1]
        size = re.findall(re.compile('<td align="right">([^<td]+?)</td><td align="center"><span class="green">'), row)[
            0].replace('&nbsp;', ' ')
        torrents[index] = {'name': name, 'id': id, 'size': size, 'download': download_link}
        index += 1

    if len(torrents) == 0:
        print('No search results for query \'' + search_query + '\'. Try another one.')
    else:
        torrents_f = [["#", "Name", "Size"]]

        for index in torrents:
            torr = torrents[index]
            torrents_f.append([index, torr['name'], torr['size']])

        print('Search by query \'' + search_query + '\':\n')

        table = texttable.Texttable()
        table.set_deco(texttable.Texttable.HEADER)
        table.set_cols_width([3, 61, 10])
        table.set_cols_dtype(['i', 't', 't', ])
        table.set_cols_align(["l", "l", "r"])
        table.add_rows(torrents_f)

        print(table.draw())
        print('\n================================================================================\n')
        try:
            var = raw_input("Pass a number of selected torrent: ")
            var = int(var)
            if var in torrents:
                torrent = torrents[var]
                download_link = torrent['download']
                file_name = search_query + '.torrent'
                try:
                    urllib.urlretrieve(download_link, file_name)
                    print('\nSuccessfully downloaded and saved as \'' + file_name + '\'.')
                    print('Trying to open by ' + PROGRAM_TO_OPEN + '...')
                    os.system(PROGRAM_TO_OPEN + ' \'' + file_name + '\' &')
                    print('Successfully, exiting...')
                except Exception:
                    print('Error while downloading by link ' + download_link + '. Try later.')
            else:
                print('\nIncorrect key. Such key does not exist.')
        except ValueError:
            print('\nIncorrect key. Enter integers only.')
        except (KeyboardInterrupt, SystemExit):
            print('\n')
