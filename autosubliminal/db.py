# coding=utf-8

import os
import sqlite3
import logging

import autosubliminal
from autosubliminal import version

log = logging.getLogger(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def dict_factory_items(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        # Languages should be returned as a list (so let's split the comma separated string)
        if col[0] == 'languages':
            d[col[0]] = row[idx].split(',')
        elif col[0] == 'dlanuages':
            d[col[0]] = row[idx].split(',')
        else:
            # Use default value from database
            d[col[0]] = row[idx]
    return d


class TvdbIdCache(object):
    def __init__(self):
        self._query_get_id = 'select tvdb_id from tvdb_id_cache where show_name = ?'
        self._query_set_id = 'insert into tvdb_id_cache values (?,?)'
        self._query_flush_cache = 'delete from tvdb_id_cache'

    def get_id(self, show_name):
        tvdb_id = None
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_get_id, [show_name.upper()])
        for row in cursor:
            tvdb_id = row[0]
        connection.close()
        if tvdb_id:
            return int(tvdb_id)

    def set_id(self, tvdb_id, show_name):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_set_id, [tvdb_id, show_name.upper()])
        connection.commit()
        connection.close()

    def flush_cache(self):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_flush_cache)
        connection.commit()
        connection.close()


class ImdbIdCache(object):
    def __init__(self):
        self._query_get_id = 'select imdb_id from imdb_id_cache where title = ? and year = ?'
        self._query_set_id = 'insert into imdb_id_cache values (?,?,?)'
        self._query_flush_cache = 'delete from imdb_id_cache'

    def get_id(self, title, year):
        imdb_id = None
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_get_id, [title.upper(), year])
        for row in cursor:
            imdb_id = row[0]
        connection.close()
        return imdb_id

    def set_id(self, imdb_id, title, year):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_set_id, [imdb_id, title.upper(), year])
        connection.commit()
        connection.close()

    def flush_cache(self):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_flush_cache)
        connection.commit()
        connection.close()


class Items(object):
    def __init__(self):
        self._query_get_wanted = 'select * from items where wanted = %s and skipped = %s order by timestamp desc'
        self._query_get_all = 'select * from items order by timestamp desc'
        self._query_get = 'select * from items where videopath=?'
        self._query_set = 'insert into items values (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        self._query_update_wanted = 'update items set timestamp=?, languages=?, type=?, title=?, ' \
                                    'year=?, season=?, episode=?, quality=?, source=?, codec=?, releasegrp=?, ' \
                                    'tvdbid=?, imdbid=?, available=?, wanted=?, skipped=? where videopath=?'
        self._query_update = 'update items set timestamp=?, dlanguages=?, type=?, title=?, ' \
                             'year=?, season=?, episode=?, quality=?, source=?, codec=?, releasegrp=?, tvdbid=?, ' \
                             'imdbid=?, available=?, wanted=?, skipped=? where videopath=?'
        self._query_delete = 'delete from items where videopath=?'
        self._query_update_subtitle = 'update items set subtitles=? where videopath=?'
        self._query_skip_item = 'update items set skipped=? where videopath=?'
        self._query_skip_show = 'update items set skipped=? where title=?'
        self._query_skip_season = 'update items set skipped=? where title=? and season=?'
        self._query_delete_wanted = 'delete from items where videopath=?'
        self._query_flush = 'delete from items'

    def get_items(self):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        connection.row_factory = dict_factory_items
        cursor = connection.cursor()
        cursor.execute(self._query_get_all)
        result_list = cursor.fetchall()
        connection.close()
        return result_list

    def get_wanted_items(self):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        connection.row_factory = dict_factory_items
        cursor = connection.cursor()
        cursor.execute(self._query_get_wanted % ('1', '0'))
        result_list = cursor.fetchall()
        connection.close()
        return result_list

    def get_item(self, video_path):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        connection.row_factory = dict_factory_items
        cursor = connection.cursor()
        cursor.execute(self._query_get, [video_path])
        item = cursor.fetchone()
        connection.close()
        return item

    def set_item(self, item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()

        # Can be unavailable in dict
        if 'tvdbid' not in item:
            item['tvdbid'] = None
        if 'imdbid' not in item:
            item['imdbid'] = None
        if 'subtitles' not in item:
            item['subtitles'] = ''
        if 'available' not in item:
            item['available'] = False
        if 'wanted' not in item:
            item['wanted'] = False
        if 'skipped' not in item:
            item['skipped'] = False

        cursor.execute(self._query_set, [
            item['videopath'],
            ','.join(item['subtitles']),
            item['timestamp'],
            # Store languages as comma separated string
            ','.join(item['languages']),
            # Store languages as comma separated string
            ','.join(item['dlanguages']),
            item['type'],
            item['title'],
            item['year'],
            item['season'],
            item['episode'],
            item['quality'],
            item['source'],
            item['codec'],
            item['releasegrp'],
            item['tvdbid'],
            item['imdbid'],
            item['available'],
            item['wanted'],
            item['skipped']])
        connection.commit()
        connection.close()

    def delete_item(self, item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_delete, [item['videopath']])
        connection.commit()
        connection.close()

    def delete_wanted_item(self, wanted_item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_delete_wanted, [wanted_item['videopath']])
        connection.commit()
        connection.close()

    def skip_item(self, wanted_item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_skip_item, [wanted_item['skipped'], wanted_item['videopath']])
        connection.commit()
        connection.close()

    def update_subtitle(self, wanted_item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_update_subtitle, [wanted_item['subtitles'], wanted_item['videopath']])
        connection.commit()
        connection.close()

    def skip_show(self, wanted_item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_skip_show, [wanted_item['skipped'], wanted_item['title']])
        connection.commit()
        connection.close()

    def skip_season(self, wanted_item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_skip_season, [wanted_item['skipped'], wanted_item['title'], wanted_item['season']])
        connection.commit()
        connection.close()

    def update_wanted_item(self, item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()

        # Can be unavailable in dict
        if 'tvdbid' not in item:
            item['tvdbid'] = None
        if 'imdbid' not in item:
            item['imdbid'] = None
        if 'available' not in item:
            item['available'] = False
        if 'wanted' not in item:
            item['wanted'] = False
        if 'skipped' not in item:
            item['skipped'] = False

        cursor.execute(self._query_update_wanted, [
            item['timestamp'],
            ','.join(item['languages']),
            item['type'],
            item['title'],
            item['year'],
            item['season'],
            item['episode'],
            item['quality'],
            item['source'],
            item['codec'],
            item['releasegrp'],
            item['tvdbid'],
            item['imdbid'],
            item['available'],
            item['wanted'],
            item['skipped'],
            item['videopath']])
        connection.commit()
        connection.close()

    def update_item(self, item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()

        # Can be unavailable in dict
        if 'tvdbid' not in item:
            item['tvdbid'] = None
        if 'imdbid' not in item:
            item['imdbid'] = None
        if 'available' not in item:
            item['available'] = False
        if 'wanted' not in item:
            item['wanted'] = False
        if 'skipped' not in item:
            item['skipped'] = False

        cursor.execute(self._query_update, [
            item['timestamp'],
            ','.join(item['dlanguages']),
            item['type'],
            item['title'],
            item['year'],
            item['season'],
            item['episode'],
            item['quality'],
            item['source'],
            item['codec'],
            item['releasegrp'],
            item['tvdbid'],
            item['imdbid'],
            item['available'],
            item['wanted'],
            item['skipped'],
            item['videopath']])
        connection.commit()
        connection.close()

    def flush_wanted_items(self):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_flush)
        connection.commit()
        connection.close()


class LastDownloads(object):
    def __init__(self):
        self._query_get = 'select * from last_downloads order by timestamp desc'
        self._query_set = 'insert into last_downloads values (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        self._query_flush = 'delete from last_downloads'

    def get_last_downloads(self):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        cursor.execute(self._query_get)
        result_list = cursor.fetchall()
        connection.close()

        # Return the max number of results or all (autosubliminal.MAXDBRESULTS = 0)
        if 0 < autosubliminal.MAXDBRESULTS < len(result_list):
            return result_list[0:autosubliminal.MAXDBRESULTS]
        else:
            return result_list

    def set_last_downloads(self, download_item):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()

        if 'source' not in download_item:
            download_item['source'] = None

        cursor.execute(self._query_set, [
            download_item['type'],
            download_item['title'],
            download_item['year'],
            download_item['season'],
            download_item['episode'],
            download_item['quality'],
            download_item['source'],
            download_item['downlang'],
            download_item['codec'],
            download_item['timestamp'],
            download_item['releasegrp'],
            download_item['subtitle'],
            download_item['provider']])
        connection.commit()
        connection.close()

    def flush_last_downloads(self):
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(self._query_flush)
        connection.commit()
        connection.close()


def create():
    # Create the database
    try:
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()

        query = 'CREATE TABLE tvdb_id_cache (tvdb_id INTEGER, show_name TEXT)'
        cursor.execute(query)
        connection.commit()

        query = 'CREATE TABLE imdb_id_cache (imdb_id TEXT, title TEXT, year TEXT)'
        cursor.execute(query)
        connection.commit()

        query = 'CREATE TABLE items (id INTEGER PRIMARY KEY, videopath TEXT, subtitles TEXT, timestamp DATETIME, ' \
                'languages TEXT, dlanguages TEXT, type TEXT, title TEXT, year TEXT, season TEXT, episode TEXT, ' \
                'quality TEXT, source TEXT, codec TEXT, releasegrp TEXT, tvdbid TEXT, imdbid TEXT, available BLOB, ' \
                'wanted BLOB, skipped BLOB)'
        cursor.execute(query)
        connection.commit()

        query = 'CREATE TABLE wanted_items (id INTEGER PRIMARY KEY, videopath TEXT, timestamp DATETIME, ' \
                'languages TEXT, type TEXT, title TEXT, year TEXT, season TEXT, episode TEXT, quality TEXT, ' \
                'source TEXT, codec TEXT, releasegrp TEXT, tvdbid TEXT, imdbid TEXT, available BLOB)'
        cursor.execute(query)
        connection.commit()

        query = 'CREATE TABLE last_downloads (id INTEGER PRIMARY KEY, type TEXT, title TEXT, year TEXT, season TEXT, ' \
                'episode TEXT, quality TEXT, source TEXT, language TEXT, codec TEXT, timestamp DATETIME, ' \
                'releasegrp TEXT, subtitle TEXT, provider TEXT)'
        cursor.execute(query)
        connection.commit()

        query = 'CREATE TABLE info (database_version NUMERIC)'
        cursor.execute(query)
        connection.commit()

        query = 'INSERT INTO info VALUES (%d)' % version.DB_VERSION
        cursor.execute(query)
        connection.commit()

        connection.close()

        print('INFO: Succesfully created the sqlite database.')
        autosubliminal.DBVERSION = version.DB_VERSION
    except Exception:
        print('ERROR: Could not create database.')
        print('ERROR: Please check if Auto-Subliminal has write access to file %s.' % autosubliminal.DBFILE)

    return True


def upgrade(from_version, to_version):
    print('INFO: Upgrading database from version %d to version %d.' % (from_version, to_version))
    upgrades = to_version - from_version
    if upgrades != 1:
        print('INFO: More than 1 upgrade required. Starting subupgrades.')
        for x in list(range(from_version, upgrades + 1)):
            upgrade((from_version - 1) + x, x + 1)
    else:
        if from_version == 1 and to_version == 2:
            # Add codec and timestamp
            # New table, info with dbversion
            connection = sqlite3.connect(autosubliminal.DBFILE)
            cursor = connection.cursor()
            cursor.execute('ALTER TABLE last_downloads ADD COLUMN %s TEXT' % 'codec')
            cursor.execute('ALTER TABLE last_downloads ADD COLUMN %s TEXT' % 'timestamp')
            cursor.execute('CREATE TABLE info (database_version NUMERIC);')
            cursor.execute('INSERT INTO info VALUES (%d)' % 2)
            connection.commit()
            connection.close()
        if from_version == 2 and to_version == 3:
            # Add Releasegrp
            connection = sqlite3.connect(autosubliminal.DBFILE)
            cursor = connection.cursor()
            cursor.execute('ALTER TABLE last_downloads ADD COLUMN %s TEXT' % 'releasegrp')
            cursor.execute('ALTER TABLE last_downloads ADD COLUMN %s TEXT' % 'subtitle')
            cursor.execute('UPDATE info SET database_version = %d WHERE database_version = %d' % (3, 2))
            connection.commit()
            connection.close()
        if from_version == 3 and to_version == 4:
            # Create id_cache table from scratch with tvdb_id
            connection = sqlite3.connect(autosubliminal.DBFILE)
            cursor = connection.cursor()
            cursor.execute('DROP TABLE id_cache;')
            cursor.execute('CREATE TABLE id_cache (tvdb_id INTEGER, show_name TEXT);')
            cursor.execute('UPDATE info SET database_version = %d WHERE database_version = %d' % (4, 3))
            connection.commit()
            connection.close()
        if from_version == 4 and to_version == 5:
            # Add provider column to last_downloads table
            connection = sqlite3.connect(autosubliminal.DBFILE)
            cursor = connection.cursor()
            cursor.execute('ALTER TABLE last_downloads ADD COLUMN %s TEXT' % 'provider')
            cursor.execute('UPDATE info SET database_version = %d WHERE database_version = %d' % (5, 4))
            connection.commit()
            connection.close()
        if from_version == 5 and to_version == 6:
            connection = sqlite3.connect(autosubliminal.DBFILE)
            cursor = connection.cursor()
            # Recreate last_downloads
            cursor.execute(
                'CREATE TABLE tmp_last_downloads (id INTEGER PRIMARY KEY, type TEXT, title TEXT, year TEXT, '
                'season TEXT, episode TEXT, quality TEXT, source TEXT, language TEXT, codec TEXT, timestamp DATETIME, '
                'releasegrp TEXT, subtitle TEXT, provider TEXT)'
            )
            cursor.execute(
                'INSERT INTO tmp_last_downloads SELECT id, episode, show_name, NULL, season, episode, quality, source, '
                'language, codec, timestamp, releasegrp, subtitle, provider FROM last_downloads')
            cursor.execute('DROP TABLE last_downloads')
            cursor.execute(
                'CREATE TABLE last_downloads (id INTEGER PRIMARY KEY, type TEXT, title TEXT, year TEXT, season TEXT, '
                'episode TEXT, quality TEXT, source TEXT, language TEXT, codec TEXT, timestamp DATETIME, '
                'releasegrp TEXT, subtitle TEXT, provider TEXT)'
            )
            cursor.execute('INSERT INTO last_downloads SELECT * FROM tmp_last_downloads')
            cursor.execute('DROP TABLE tmp_last_downloads')
            # Create imdb_id_cache
            cursor.execute('CREATE TABLE imdb_id_cache (imdb_id TEXT, title TEXT, year TEXT)')
            # Create tvdb_id_cache
            cursor.execute('CREATE TABLE tvdb_id_cache (tvdb_id TEXT, show_name TEXT)')
            # Drop id_cache
            cursor.execute('DROP TABLE id_cache')
            # Update database version
            cursor.execute('UPDATE info SET database_version = %d WHERE database_version = %d' % (6, 5))
            connection.commit()
            connection.close()
        if from_version == 6 and to_version == 7:
            connection = sqlite3.connect(autosubliminal.DBFILE)
            cursor = connection.cursor()
            # Create wanted_items
            cursor.execute(
                'CREATE TABLE wanted_items (id INTEGER PRIMARY KEY, videopath TEXT, timestamp DATETIME, '
                'languages TEXT, type TEXT, title TEXT, year TEXT, season TEXT, episode TEXT, quality TEXT, '
                'source TEXT, codec TEXT, releasegrp TEXT, tvdbid TEXT, imdbid TEXT)'
            )
            # Update database version
            cursor.execute('UPDATE info SET database_version = %d WHERE database_version = %d' % (7, 6))
            connection.commit()
            connection.close()
        if from_version == 7 and to_version == 8:
            connection = sqlite3.connect(autosubliminal.DBFILE)
            cursor = connection.cursor()
            # Add available to wanted_items
            cursor.execute('ALTER TABLE wanted_items ADD COLUMN %s BLOB' % 'available')
            # Update database version
            cursor.execute('UPDATE info SET database_version = %d WHERE database_version = %d' % (8, 7))
            connection.commit()
            connection.close()


def get_version():
    try:
        query_get_version = 'SELECT database_version FROM info'
        connection = sqlite3.connect(autosubliminal.DBFILE)
        cursor = connection.cursor()
        cursor.execute(query_get_version)

        db_version = None
        for row in cursor:
            db_version = row[0]
        connection.close()

        return int(db_version)
    except Exception:
        return 1


def initialize():
    # Check if file is already there
    db_file = os.path.join(autosubliminal.PATH, autosubliminal.DBFILE)
    if not os.path.exists(db_file):
        create()

    autosubliminal.DBVERSION = get_version()

    if autosubliminal.DBVERSION < version.DB_VERSION:
        upgrade(autosubliminal.DBVERSION, version.DB_VERSION)
    elif autosubliminal.DBVERSION > version.DB_VERSION:
        print('ERROR: Database version higher then this version of Auto-Subliminal supports. Update.')
        os._exit(1)
