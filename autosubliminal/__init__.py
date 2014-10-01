import os
import time
import pkg_resources

import subliminal

from autosubliminal import version, config, logger, db

# Config
CONFIGFILE = None
CONFIGVERSION = None
CONFIGUPGRADED = None

# System
VERSIONURL = None
USERAGENT = None
SYSENCODING = None
TIMEOUT = None
WANTEDQUEUE = None
WANTEDQUEUELOCK = None

# Db
DBFILE = None
DBVERSION = None

# Startup
DAEMON = None
STARTED = None
PID = None

# Mobile
MOBILE = None
MOBILEUSERAGENTS = None

# API
APIKEY = None
API = None
APICALLS = None
APICALLSLASTRESET = None
APICALLSRESETINT = None
APICALLSMAX = None

# General config section
PATH = None
VIDEOPATHS = None
DEFAULTLANGUAGE = None
DEFAULTLANGUAGESUFFIX = None
ADDITIONALLANGUAGES = None
MINMATCHSCORE = None
MINMATCHSCOREDEFAULT = None
MATCHSOURCE = None
MATCHQUALITY = None
MATCHCODEC = None
MATCHRELEASEGROUP = None
SCANDISK = None
CHECKSUB = None
SCHEDULERSCANDISK = None
SCHEDULERCHECKSUB = None
SKIPHIDDENDIRS = None

# Logfile config section
LOGFILE = None
LOGLEVEL = None
LOGSIZE = None
LOGNUM = None
LOGREVERSED = None
LOGHTTPACCESS = None
LOGLEVELCONSOLE = None

# Webserver config section
WEBSERVERIP = None
WEBSERVERPORT = None
WEBROOT = None
USERNAME = None
PASSWORD = None
LAUNCHBROWSER = None

# Subliminal config section
SUBLIMINALPROVIDERS = None
SUBLIMINALPROVIDERLIST = None
SUBLIMINALPROVIDERCONFIGS = None
INCLUDEHEARINGIMPAIRED = None
ADDIC7EDUSERNAME = None
ADDIC7EDPASSWORD = None

# Namemapping config section
USERNAMEMAPPING = None
USERNAMEMAPPINGUPPER = None
NAMEMAPPING = None
NAMEMAPPINGUPPER = None

# Skipshow config section
SKIPSHOW = None
SKIPSHOWUPPER = None

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
NOTIFYNMA = None
NMAAPI = None
NOTIFYGROWL = None
GROWLHOST = None
GROWLPORT = None
GROWLPASS = None
NOTIFYPROWL = None
PROWLAPI = None
PROWLPRIORITY = None

# PostProcessing config section
POSTPROCESS = None
POSTPROCESSCMD = None
POSTPROCESSUTF8ENCODING = None


def initialize():
    global CONFIGFILE, CONFIGVERSION, CONFIGUPGRADED, \
        VERSIONURL, USERAGENT, SYSENCODING, TIMEOUT, WANTEDQUEUE, WANTEDQUEUELOCK, \
        DBFILE, DBVERSION, \
        DAEMON, STARTED, PID, \
        MOBILE, MOBILEUSERAGENTS, \
        APIKEY, API, APICALLS, APICALLSLASTRESET, APICALLSRESETINT, APICALLSMAX, \
        PATH, VIDEOPATHS, DEFAULTLANGUAGE, DEFAULTLANGUAGESUFFIX, ADDITIONALLANGUAGES, MINMATCHSCORE, \
        MINMATCHSCOREDEFAULT, MATCHSOURCE, MATCHQUALITY, MATCHCODEC, MATCHRELEASEGROUP, SCANDISK, CHECKSUB, \
        SCHEDULERSCANDISK, SCHEDULERCHECKSUB, SKIPHIDDENDIRS, \
        LOGFILE, LOGLEVEL, LOGSIZE, LOGNUM, LOGREVERSED, LOGHTTPACCESS, LOGLEVELCONSOLE, \
        WEBSERVERIP, WEBSERVERPORT, WEBROOT, USERNAME, PASSWORD, LAUNCHBROWSER, \
        SUBLIMINALPROVIDERS, SUBLIMINALPROVIDERLIST, SUBLIMINALPROVIDERCONFIGS, INCLUDEHEARINGIMPAIRED, \
        ADDIC7EDUSERNAME, ADDIC7EDPASSWORD, \
        USERNAMEMAPPING, USERNAMEMAPPINGUPPER, NAMEMAPPING, NAMEMAPPINGUPPER, \
        SKIPSHOW, SKIPSHOWUPPER, \
        NOTIFY, NOTIFYMAIL, MAILSRV, MAILFROMADDR, MAILTOADDR, MAILUSERNAME, MAILPASSWORD, MAILSUBJECT, MAILAUTH, \
        MAILENCRYPTION, NOTIFYTWITTER, TWITTERKEY, TWITTERSECRET, NOTIFYPUSHALOT, PUSHALOTAPI, NOTIFYNMA, NMAAPI, \
        NOTIFYGROWL, GROWLHOST, GROWLPORT, GROWLPASS, NOTIFYPROWL, PROWLAPI, PROWLPRIORITY, \
        POSTPROCESS, POSTPROCESSCMD, POSTPROCESSUTF8ENCODING

    # Fake some entry points to get libraries working without installation
    _fake_entry_points()

    # Version settings
    VERSIONURL = 'https://raw.github.com/h3llrais3r/Auto-Subliminal/master/autosubliminal/version.py'
    USERAGENT = 'Auto-Subliminal/' + version.RELEASE_VERSION

    # Default http timeout
    TIMEOUT = 300

    # Wanted queue settings
    WANTEDQUEUE = []
    WANTEDQUEUELOCK = False

    # Startup settings
    STARTED = False

    # Mobile settings
    MOBILE = True
    MOBILEUSERAGENTS = ["midp", "240x320", "blackberry", "netfront", "nokia", "panasonic",
                        "portalmmm", "sharp", "sie-", "sonyericsson", "symbian", "windows ce",
                        "benq", "mda", "mot-", "opera mini", "philips", "pocket pc", "sagem",
                        "samsung", "sda", "sgh-", "vodafone", "xda", "palm", "iphone", "ipod",
                        "ipad", "android", "windows phone"]

    # API settings
    # Currently not used anymore (perhaps reuse it for tvdb api calls when a custom tvdb api key is needed?)
    APIKEY = ""
    API = "http://.../%s/" % APIKEY
    APICALLSLASTRESET = time.time()
    APICALLSRESETINT = 86400
    APICALLSMAX = 300
    APICALLS = APICALLSMAX

    # Score settings
    MINMATCHSCOREDEFAULT = 60

    # Webserver settings
    LAUNCHBROWSER = True

    # Config file settings
    CONFIGUPGRADED = False
    if CONFIGFILE is None:
        CONFIGFILE = "config.properties"
    config.read_config()
    if CONFIGUPGRADED:
        print "INFO: Config seems to be upgraded. Writing config."
        config.write_config()
        print "INFO: Writing config done."

    # Change to the new work directory
    if os.path.exists(PATH):
        os.chdir(PATH)
    else:
        print "ERROR: PATH does not exist, check config"
        os._exit(1)

    # Database
    DBFILE = 'database.db'
    db.initialize()

    # Logging
    logger.initialize()

    # Subliminal settings
    _initialize_subliminal()


def _fake_entry_points():
    # Do not normalize the path or the entry point will be loaded under the wrong entry_key
    # current_path = os.path.dirname(os.path.normpath(__file__))
    current_path = os.path.dirname(__file__)
    distribution = pkg_resources.Distribution(location=os.path.dirname(current_path),
                                              project_name='fake_entry_points', version='1.0.0')
    # Add entry points here if needed
    entry_points = {}
    distribution._ep_map = pkg_resources.EntryPoint.parse_map(entry_points, distribution)
    pkg_resources.working_set.add(distribution)


def _initialize_subliminal():
    # Configure subliminal/dogpile cache
    # Use MutexLock otherwise some providers will not work due to fcntl module import error in windows
    # Do not reconfigure after a soft restart (without exiting main app) -> otherwise RegionAlreadyConfigured exception
    if not subliminal.cache_region.is_configured:
        cache_file = os.path.abspath(os.path.expanduser('subliminal.cache.dbm'))
        subliminal.cache_region.configure(backend='dogpile.cache.dbm',
                                          arguments={'filename': cache_file, 'lock_factory': subliminal.MutexLock})