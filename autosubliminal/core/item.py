# coding=utf-8

import datetime

from autosubliminal.util.common import get_today

# A subtitle will be searched on each run, as long as the file is not older than 4 weeks
search_deadline = datetime.timedelta(weeks=30)

# Once a video file is older than the search deadline, it will only be searched once a week
search_delta = datetime.timedelta(weeks=1)


# TODO: Refactor wanted_item dict to WantedItem class! For now we use the wanted_item dict inside the WantedItem class!
class WantedItem(object):
    """
    Class holding all the data for a wanted item.
    """

    def __init__(self, wanted_item):
        # TODO: Remove dict when all properties are available and usage of dict has been replaced by this class
        self.wanted_item = wanted_item

    @property
    def search_active(self):
        """
        Check if the search is active for the wanted item.
        The search will be active:
        - on each run when file age is less or equal to 4 weeks
        - once every week (calculated from file timestamp) when file age is more than 4 weeks
        """
        file_datetime = datetime.datetime.strptime(self.wanted_item['timestamp'], '%Y-%m-%d %H:%M:%S')
        file_search_deadline = file_datetime + search_deadline
        today = get_today()
        file_age_in_days = (today.date() - file_search_deadline.date()).days
        if today.date() <= file_search_deadline.date():
            return True
        elif file_age_in_days % search_delta.days == 0:
            return True
        else:
            return False
