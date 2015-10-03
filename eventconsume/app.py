from eventconsume.consumers.twitter import TwitterConsumer

def success(event):
    print event.text

def failure(error):
    print error

t = TwitterConsumer()
t.connect()
t.start(success, failure)

