import os
import time

from mako.lookup import TemplateLookup
from mako.template import Template

import autosubliminal

mako_path = os.path.normpath(os.path.join(autosubliminal.PATH, 'web/templates'))
# TODO: configure mako cache
# mako_cache = os.path.normpath(os.path.join(autosubliminal.CACHE_DIR, 'mako'))
mako_cache = None
mako_lookup = TemplateLookup(directories=[mako_path], module_directory=mako_cache)


class MakoPageTemplate(Template):
    """
    Mako page template.
    """

    def __init__(self, filename):
        self.lookup = mako_lookup
        self.template = self.lookup.get_template(filename)
        # Default arguments for all pages
        self.arguments = {
            'appPID': str(autosubliminal.PID)
        }

    def render(self, *args, **kwargs):
        """
        Render the Page template.
        """
        for key in self.arguments:
            if key not in kwargs:
                kwargs[key] = self.arguments[key]
        # Default render arguments (must be set at render time)
        kwargs['makoStartTime'] = time.time()
        # Render unicode by default
        return self.template.render_unicode(*args, **kwargs)
