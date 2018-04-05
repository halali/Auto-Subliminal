# coding=utf-8

import logging

from six import text_type

import autosubliminal
from autosubliminal.util.common import sanitize

log = logging.getLogger(__name__)


def skip_show(show_name, season, episode):
    """Check if a show should be skipped."""
    show_name_sanitized = sanitize(show_name)
    for x in autosubliminal.SKIPSHOW:
        if show_name_sanitized == sanitize(x):
            log.debug('Found match in skipshow for %s', show_name)
            for s in autosubliminal.SKIPSHOW[x].split(','):
                if s == '00':
                    log.debug('Found all season match in skipshow, skipping all seasons for %s', show_name)
                    return True
                elif int(s) == int(season):
                    log.debug('Found season match in skipshow, skipping season %s for %s', season, show_name)
                    return True


def skip_movie(title, year):
    """Check if a movie should be skipped."""
    movie = title
    if year:
        movie += ' (' + text_type(year) + ')'
    movie_sanitized = sanitize(movie)
    for x in autosubliminal.SKIPMOVIE:
        if movie_sanitized == sanitize(x):
            log.debug('Found match in skipmovie, skipping movie %s', movie)
            return True
