import sys

# Find a better way to do this...
if sys.argv[0].find('test') >= 0:
    TESTING = True
else:
    TESTING = False

if TESTING:
    # WARNING: Using this requires that you have previously created
    # the test index and PUT its mapping. TODO: automate
    ES_INDEX = 'test'
else:
    ES_INDEX = 'events'

