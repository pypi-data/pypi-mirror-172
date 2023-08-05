from app_utils.django import clean_setting

TASKMONITOR_DATA_MAX_AGE = clean_setting("TASKMONITOR_DATA_MAX_AGE", 24)
"""Max age of logged tasks in hours. Older logs be deleted automatically."""

TASKMONITOR_HOUSEKEEPING_FREQUENCY = clean_setting(
    "TASKMONITOR_HOUSEKEEPING_FREQUENCY", 15
)
"""Frequency of house keeping runs in minutes."""

TASKMONITOR_REPORTS_MAX_AGE = clean_setting("TASKMONITOR_REPORTS_MAX_AGE", 30)
"""Max age of cached reports in minutes."""

TASKMONITOR_REPORTS_MAX_TOP = clean_setting("TASKMONITOR_REPORTS_MAX_TOP", 20)
"""Max items to show in the top reports. e.g. 10 will shop the top ten items."""

TASKMONITOR_TRUNCATE_NESTED_DATA = clean_setting(
    "TASKMONITOR_TRUNCATE_NESTED_DATA", True
)
"""Whether deeply nested task params and results are truncated."""
