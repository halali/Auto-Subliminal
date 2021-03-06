# coding=utf-8

import os
import uuid
import pkg_resources

from six.moves import getcwd

from autosubliminal import config, db, version
from autosubliminal.core import logger
from autosubliminal.indexer import MovieIndexer, ShowIndexer

# Config
CONFIGFILE = None
CONFIGVERSION = None
CONFIGUPGRADED = None

# System
PATH = None
CACHEDIR = None
DEREFERURL = None
GITHUBURL = None
VERSIONURL = None
USERAGENT = None
SYSENCODING = None
TIMEOUT = None
WANTEDQUEUE = None
WANTEDQUEUELOCK = None
WEBSOCKETMESSAGEQUEUE = None
WEBSOCKETBROADCASTER = None
SCHEDULERS = None
SCANDISK = None
CHECKSUB = None
CHECKVERSION = None

# Developer
DEVELOPER = None

# Indexers
TVDBAPIKEY = None
TVDBURL = None
IMDBURL = None
SHOWINDEXER = None
MOVIEINDEXER = None

# Db
DBFILE = None
DBVERSION = None

# Startup
EXECUTABLE = None
ARGS = None
DAEMON = None
STARTED = None
PID = None
UUID = None

# General config section
VIDEOPATHS = None
DEFAULTLANGUAGE = None
DEFAULTLANGUAGESUFFIX = None
ADDITIONALLANGUAGES = None
INDIVIDUALADDITIONALLANGUAGE = None
SCANDISKINTERVAL = None
CHECKSUBINTERVAL = None
CHECKVERSIONINTERVAL = None
CHECKVERSIONAUTOUPDATE = None
SCANEMBEDDEDSUBS = None
SKIPHIDDENDIRS = None
DETECTINVALIDSUBLANGUAGE = None
DETECTEDLANGUAGEPROBABILITY = None
MINVIDEOFILESIZE = None  # in MB
MAXDBRESULTS = None

# Logfile config section
LOGFILE = None
LOGLEVEL = None
LOGSIZE = None  # in MB
LOGNUM = None
LOGHTTPACCESS = None
LOGEXTERNALLIBS = None
LOGDETAILEDFORMAT = None
LOGREVERSED = None
LOGLEVELCONSOLE = None

# Webserver config section
WEBSERVERIP = None
WEBSERVERPORT = None
WEBROOT = None
USERNAME = None
PASSWORD = None
LAUNCHBROWSER = None

# Subliminal config section
SHOWMINMATCHSCORE = None
SHOWMINMATCHSCOREDEFAULT = None
SHOWMATCHSOURCE = None
SHOWMATCHQUALITY = None
SHOWMATCHCODEC = None
SHOWMATCHRELEASEGROUP = None
MOVIEMINMATCHSCORE = None
MOVIEMINMATCHSCOREDEFAULT = None
MOVIEMATCHSOURCE = None
MOVIEMATCHQUALITY = None
MOVIEMATCHCODEC = None
MOVIEMATCHRELEASEGROUP = None
SUBLIMINALPROVIDERMANAGER = None
SUBLIMINALPROVIDERS = None
SUBLIMINALPROVIDERCONFIGS = None
SUBTITLEUTF8ENCODING = None
MANUALREFINEVIDEO = None
REFINEVIDEO = None
PREFERHEARINGIMPAIRED = None
ADDIC7EDUSERNAME = None
ADDIC7EDPASSWORD = None
OPENSUBTITLESUSERNAME = None
OPENSUBTITLESPASSWORD = None

# Namemapping config section
SHOWNAMEMAPPING = None
ADDIC7EDSHOWNAMEMAPPING = None
ALTERNATIVESHOWNAMEMAPPING = None
MOVIENAMEMAPPING = None
ALTERNATIVEMOVIENAMEMAPPING = None

# Skip config section
SKIPSHOW = None
SKIPMOVIE = None

# Notifications config section
NOTIFY = None
NOTIFYMAIL = None
MAILSRV = None
MAILFROMADDR = None
MAILTOADDR = None
MAILUSERNAME = None
MAILPASSWORD = None
MAILSUBJECT = None
MAILAUTH = None
MAILENCRYPTION = None
NOTIFYTWITTER = None
TWITTERKEY = None
TWITTERSECRET = None
NOTIFYPUSHALOT = None
PUSHALOTAPI = None
NOTIFYPUSHOVER = None
PUSHOVERKEY = None
PUSHOVERAPI = None
PUSHOVERDEVICES = None
NOTIFYNMA = None
NMAAPI = None
NMAPRIORITY = None
NOTIFYGROWL = None
GROWLHOST = None
GROWLPORT = None
GROWLPASS = None
GROWLPRIORITY = None
NOTIFYPROWL = None
PROWLAPI = None
PROWLPRIORITY = None
NOTIFYPUSHBULLET = None
PUSHBULLETAPI = None
NOTIFYTELEGRAM = None
TELEGRAMBOTAPI = None
TELEGRAMCHATID = None

# PostProcessing config section
POSTPROCESS = None
POSTPROCESSINDIVIDUAL = None
POSTPROCESSUTF8ENCODING = None
SHOWPOSTPROCESSCMD = None
SHOWPOSTPROCESSCMDARGS = None
MOVIEPOSTPROCESSCMD = None
MOVIEPOSTPROCESSCMDARGS = None


def initialize():
    global CONFIGFILE, CONFIGVERSION, CONFIGUPGRADED, \
        CACHEDIR, DEREFERURL, GITHUBURL, VERSIONURL, USERAGENT, SYSENCODING, TIMEOUT, WANTEDQUEUE, WANTEDQUEUELOCK, \
        WEBSOCKETMESSAGEQUEUE, WEBSOCKETBROADCASTER, SCHEDULERS, SCANDISK, CHECKSUB, CHECKVERSION, \
        DEVELOPER, \
        TVDBAPIKEY, TVDBURL, IMDBURL, SHOWINDEXER, MOVIEINDEXER, \
        DBFILE, DBVERSION, \
        DAEMON, STARTED, PID, UUID, \
        PATH, VIDEOPATHS, DEFAULTLANGUAGE, DEFAULTLANGUAGESUFFIX, ADDITIONALLANGUAGES, INDIVIDUALADDITIONALLANGUAGE, \
        SCANDISKINTERVAL, CHECKSUBINTERVAL, CHECKVERSIONINTERVAL, CHECKVERSIONAUTOUPDATE, SCANEMBEDDEDSUBS, \
        SKIPHIDDENDIRS, DETECTINVALIDSUBLANGUAGE, DETECTEDLANGUAGEPROBABILITY, MINVIDEOFILESIZE, MAXDBRESULTS, \
        LOGFILE, LOGLEVEL, LOGSIZE, LOGNUM, LOGHTTPACCESS, LOGEXTERNALLIBS, LOGDETAILEDFORMAT, LOGREVERSED, \
        LOGLEVELCONSOLE, \
        WEBSERVERIP, WEBSERVERPORT, WEBROOT, USERNAME, PASSWORD, LAUNCHBROWSER, \
        SHOWMINMATCHSCORE, SHOWMINMATCHSCOREDEFAULT, SHOWMATCHSOURCE, SHOWMATCHQUALITY, SHOWMATCHCODEC, \
        SHOWMATCHRELEASEGROUP, \
        MOVIEMINMATCHSCORE, MOVIEMINMATCHSCOREDEFAULT, MOVIEMATCHSOURCE, MOVIEMATCHQUALITY, MOVIEMATCHCODEC, \
        MOVIEMATCHRELEASEGROUP, \
        SUBLIMINALPROVIDERMANAGER, SUBLIMINALPROVIDERS, SUBLIMINALPROVIDERCONFIGS, \
        SUBTITLEUTF8ENCODING, MANUALREFINEVIDEO, REFINEVIDEO, PREFERHEARINGIMPAIRED, \
        ADDIC7EDUSERNAME, ADDIC7EDPASSWORD, OPENSUBTITLESUSERNAME, OPENSUBTITLESPASSWORD, \
        SHOWNAMEMAPPING, ADDIC7EDSHOWNAMEMAPPING, ALTERNATIVESHOWNAMEMAPPING, \
        MOVIENAMEMAPPING, ALTERNATIVEMOVIENAMEMAPPING, \
        SKIPSHOW, SKIPMOVIE, \
        NOTIFY, NOTIFYMAIL, MAILSRV, MAILFROMADDR, MAILTOADDR, MAILUSERNAME, MAILPASSWORD, MAILSUBJECT, MAILAUTH, \
        MAILENCRYPTION, NOTIFYTWITTER, TWITTERKEY, TWITTERSECRET, NOTIFYPUSHALOT, PUSHALOTAPI, \
        NOTIFYPUSHOVER, PUSHOVERKEY, PUSHOVERAPI, PUSHOVERDEVICES, NOTIFYNMA, NMAAPI, NMAPRIORITY, \
        NOTIFYGROWL, GROWLHOST, GROWLPORT, GROWLPASS, GROWLPRIORITY, NOTIFYPROWL, PROWLAPI, PROWLPRIORITY, \
        NOTIFYPUSHBULLET, PUSHBULLETAPI, NOTIFYTELEGRAM, TELEGRAMBOTAPI, TELEGRAMCHATID, \
        POSTPROCESS, POSTPROCESSINDIVIDUAL, POSTPROCESSUTF8ENCODING, SHOWPOSTPROCESSCMD, SHOWPOSTPROCESSCMDARGS, \
        MOVIEPOSTPROCESSCMD, MOVIEPOSTPROCESSCMDARGS

    # Fake some entry points to get libraries working without installation
    _fake_entry_points()

    # System settings
    PATH = os.path.abspath(getcwd())
    CACHEDIR = os.path.abspath(os.path.join(PATH, 'cache'))
    DEREFERURL = 'http://www.dereferer.org/?'
    GITHUBURL = 'https://github.com/h3llrais3r/Auto-Subliminal'
    VERSIONURL = 'https://raw.github.com/h3llrais3r/Auto-Subliminal/master/autosubliminal/version.py'
    USERAGENT = 'Auto-Subliminal/' + version.RELEASE_VERSION
    TIMEOUT = 300

    # Wanted queue settings
    WANTEDQUEUE = []
    WANTEDQUEUELOCK = False

    # Websocket settings
    WEBSOCKETMESSAGEQUEUE = []

    # Scheduler settings
    SCHEDULERS = {}

    # Developer settings
    DEVELOPER = False

    # Indexer settings
    TVDBAPIKEY = '76F2D5362F45C5EC'
    TVDBURL = 'http://thetvdb.com/?tab=series&id='
    IMDBURL = 'http://www.imdb.com/title/'
    SHOWINDEXER = ShowIndexer()
    MOVIEINDEXER = MovieIndexer()

    # Startup settings
    STARTED = False
    UUID = uuid.uuid4()  # Generate random uuid each time we initialize the application

    # Score settings
    SHOWMINMATCHSCOREDEFAULT = 330
    MOVIEMINMATCHSCOREDEFAULT = 90

    # Webserver settings
    LAUNCHBROWSER = True

    # Cache settings
    _init_cache()

    # Subliminal settings
    SUBLIMINALPROVIDERMANAGER = _init_subliminal()
    SUBLIMINALPROVIDERCONFIGS = {}

    # Langdetect settings
    _init_langdetect()

    # Config settings
    CONFIGUPGRADED = False
    if CONFIGFILE is None:
        CONFIGFILE = 'config.properties'
    config.read_config(True)
    if CONFIGUPGRADED:
        print('INFO: Config seems to be upgraded. Writing config.')
        config.write_config()
        print('INFO: Writing config done.')

    # Change to the new work directory
    if os.path.exists(PATH):
        os.chdir(PATH)
    else:
        print('ERROR: PATH does not exist, check config.')
        os._exit(1)

    # Database settings
    DBFILE = 'database.db'
    db.initialize()

    # Logging settings
    logger.initialize()


def _fake_entry_points():
    """
    Fake some entry points to get libraries working without installation.
    After setup, entry points can be retrieved by:
    pkg_resources.get_entry_info(dist='fake_entry_points', group=None, name='entry_point_namespace')
    """

    # Do not normalize the path or the entry point will be loaded under the wrong entry_key
    # current_path = os.path.dirname(os.path.normpath(__file__))
    current_path = os.path.dirname(__file__)
    distribution = pkg_resources.Distribution(location=os.path.dirname(current_path), project_name='fake_entry_points',
                                              version=version.RELEASE_VERSION)
    # Add entry points here if needed (currently none)
    entry_points = {}
    distribution._ep_map = pkg_resources.EntryPoint.parse_map(entry_points, distribution)
    pkg_resources.working_set.add(distribution)


def _init_cache():
    """
    Initialize internal cache.
    """

    # Imports
    from autosubliminal.core.cache import MutexFileLock, region

    # Make sure the cache dir exists
    if not os.path.exists(CACHEDIR):
        os.makedirs(CACHEDIR)

    # Configure autosubliminal/dogpile cache
    # Use MutexFileLock otherwise it will not work due to fcntl module import error in windows
    # Do not reconfigure after a soft restart (without exiting main app) -> otherwise RegionAlreadyConfigured exception
    if not region.is_configured:
        cache_file = os.path.abspath(os.path.join(CACHEDIR, 'autosubliminal.cache.dbm'))
        region.configure(backend='dogpile.cache.dbm', arguments={'filename': cache_file, 'lock_factory': MutexFileLock})


def _init_subliminal():
    """
    Initialize subliminal.
    This must always be done AFTER the registration of our fake_entry_points.
    Therefore the imports must be done here, otherwise the 'subliminal.providers' entry point is already initialized
    before we could register it ourselves.
    -> see subliminal.api.provider_manager
    """

    # Imports
    from subliminal.cache import region
    from subliminal.cli import MutexLock
    from subliminal.extensions import provider_manager, refiner_manager

    # Configure subliminal/dogpile cache
    # Use MutexLock otherwise some providers will not work due to fcntl module import error in windows
    # Do not reconfigure after a soft restart (without exiting main app) -> otherwise RegionAlreadyConfigured exception
    if not region.is_configured:
        cache_file = os.path.abspath(os.path.join(CACHEDIR, 'subliminal.cache.dbm'))
        region.configure(backend='dogpile.cache.dbm', arguments={'filename': cache_file, 'lock_factory': MutexLock})

    # Add our custom refiners to list of subliminal refiners
    manual_refiner = 'manual = autosubliminal.refiners.manual:refine'
    if manual_refiner not in refiner_manager.registered_extensions:
        refiner_manager.register(manual_refiner)
    namemapping_refiner = 'namemapping = autosubliminal.refiners.namemapping:refine'
    if namemapping_refiner not in refiner_manager.registered_extensions:
        refiner_manager.register(namemapping_refiner)

    # Add our custom addic7ed provider to list of subliminal providers
    provider = 'addic7ed_random_user_agent = autosubliminal.providers.addic7ed:Addic7edProvider'
    if provider not in provider_manager.registered_extensions:
        provider_manager.register(provider)

    # Return the provider manager with all providers
    return provider_manager


def _init_langdetect():
    """
    Initialize language detection.
    """
    # Imports
    import langdetect.detector_factory
    from langdetect.detector_factory import DetectorFactory

    # Init factory (to load the profiles at startup)
    langdetect.detector_factory.init_factory()

    # Language detection algorithm is non-deterministic, we might get different results every time you run it.
    # To enforce consistent results, call following code before the first language detection
    DetectorFactory.seed = 0
