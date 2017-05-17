import logging
import os
import re
import time
from autosubliminal.indexer import ShowIndexer, MovieIndexer

from guessit import guessit

import autosubliminal
from autosubliminal import utils

log = logging.getLogger(__name__)

release_group_regex = "(.*)\[.*?\]"


def process_file(dirname, filename):
    """
    Process a file with guessit and construct the wanted_item dict.
    Items used in wanted_item for type = 'episode':
    - 'videopath'
    - 'timestamp'
    - 'languages'
    - 'type'
    - 'title'
    - 'year'
    - 'season'
    - 'episode'
    - 'source'
    - 'quality'
    - 'codec'
    - 'releasegrp'
    - 'tvdbid'
    Items used in wanted_item for type = 'movie':
    - 'videopath'
    - 'timestamp'
    - 'languages'
    - 'type'
    - 'title'
    - 'year'
    - 'source'
    - 'quality'
    - 'codec'
    - 'releasegrp'
    - 'imdbid'
    """

    log.info("Processing file: %s" % filename)
    file_path = os.path.join(dirname, filename)

    # Check minimal video file size if needed
    if autosubliminal.MINVIDEOFILESIZE:
        file_size = os.path.getsize(file_path)
        # MINVIDEOFILESIZE is size in MB
        if file_size < autosubliminal.MINVIDEOFILESIZE * 1024 * 1024:
            log.warning("File size (%s) is lower than %sMB, skipping" % (
                utils.humanize_bytes(file_size), autosubliminal.MINVIDEOFILESIZE))
            return None

    # Guess
    try:
        log.debug("Guessing file info")
        guess = guessit(file_path)
        log.debug("Guess result: %r" % guess)
    except Exception, e:
        log.error("Could not guess file info for: %s" % file_path)
        log.error(e)
        return None

    # Create dict from guess
    result_dict = _dict_from_guess(guess)

    # Enrich dict
    if result_dict:
        _enrich_dict(result_dict, file_path)

    return result_dict


def _dict_from_guess(guess):
    """
    Create a dict from a guess:
    - The same dict is used for both episode and movie
    - If no 'screenSize' is found, it will default to 'SD' quality
    """
    result_dict = {'type': _property_from_guess(guess, 'type'),
                   'title': _property_from_guess(guess, 'title'),
                   'year': _property_from_guess(guess, 'year'),
                   'season': _property_from_guess(guess, 'season'),
                   'episode': _property_from_guess(guess, 'episode'),
                   'source': _property_from_guess(guess, 'format'),
                   'quality': _property_from_guess(guess, 'screen_size'),
                   'codec': _property_from_guess(guess, 'video_codec'),
                   'releasegrp': _split_release_group(_property_from_guess(guess, 'release_group'))}
    log.debug("Dict from guess: %r" % result_dict)

    # Check if mandatory elements are available in the guess
    if result_dict['type'] == 'movie' and result_dict['title']:
        log.debug("Video guessed as movie")
        return result_dict
    # Season and episode are numbers, so need to check explicitly for not None (0 results in False in Python)
    elif result_dict['type'] == 'episode' and result_dict['title'] and result_dict['season'] is not None \
            and result_dict['episode'] is not None:
        log.debug("Video guessed as episode")
        return result_dict
    else:
        log.error("Could not guess all the mandatory elements")
        return None


def _property_from_guess(guess, property_name, default_value=None):
    property_value = default_value
    if property_name in guess.keys():
        property_value = guess[property_name]
    return property_value


def _split_release_group(release_group):
    if release_group:
        # Remove release group provider (part between []) if present (f.e. KILLERS[rarbg])
        match = re.search(release_group_regex, release_group)
        if match:
            # Return first parenthesized group (=release group without [] part)
            return match.group(1)
    return release_group


def _enrich_dict(result_dict, file_path):
    log.debug("Enriching dict with metadata")

    # Enrich with common data
    result_dict['videopath'] = file_path
    result_dict['timestamp'] = unicode(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(result_dict['videopath']))))
    # Languages cannot be derived from the processing file, so set the outside the fileprocessor (i.e. in diskscanner)
    result_dict['languages'] = []

    # Enrich with episode data
    if result_dict['type'] == 'episode':
        result_dict['tvdbid'] = ShowIndexer().get_tvdb_id(result_dict['title'])

    # Enrich with movie data
    elif result_dict['type'] == 'movie':
        result_dict['imdbid'], result_dict['year'] = MovieIndexer().get_imdb_id_and_year(result_dict['title'],
                                                                                         result_dict['year'])

    log.debug("Enriched dict: %r" % result_dict)
