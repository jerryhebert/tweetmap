# EventMap

EventMap is designed to pull in events from multiple sources, extract
the information that we care about and then index them into Elasticsearch.
Three are three main components:

## EventConsume

This package is responsible for consuming events from our sources. Write
plugins for each type of event that you wish to consume. These plugins
execute simultaneously. Callbacks are set up so that we can capture the
data coming out of the plugins and persist this into Elasticsearch.

## EventServe

This package is a simple HTTP API on top of events. The only endpoint
currently supported is:
    GET /events
This takes the following query parameters to aid in filtering out the
events:
    tags - a list of tags to filter our events by
    lat - the latitude for our cell center
    lon - the longitude for our cell center
    radius - the radius from the center that we will select events from

A list of events within this region that match the given keywords is
then returned.

## EventClient

A simple web UI to allow a user to query events and view the results.
The client is served statically from `dist` so any web server should work. 

# Installation

Clone the git repository. All three systems currently exist in the same
repository. 

## Plugins

Each plugin will potentially require its own credentials. A config file
for each plugin should be installed next to that plugin.

### Twitter

Visit http://dev.twitter.com and create your twitter credentials for this
application to use. Once you've fetched a consumer key, consumer secret,
access token and access token secret, copy the example config file at
`eventcosnume/consumers/twitter.yml.example` to `eventcosnume/consumers/twitter.yml`
and make your edits.

## Try it

Once you've configured you're plugins, build the consumer and set up Elasticsearch:

```
cd eventconsume
./manage.sh build
```

This will create the virtualenv required to run your module. Now put
the elasticsearch mapping:

```
cd etc/es_mapping
curl -XPUT http://localhost:9200/events/event/_mapping -d @es_mapping.json
```

Now you're ready to start consuming events! Go back to the consumer root
and run the app:

```
cd ../..
./manage.sh run
```

Now we just have to start the server and we'll be good to go. In another
shell from the root of the project, go into the serve package directory,
build it and run it:

```
cd eventserve
./manage.sh build
./manage.sh run
```

## Plugins

Each plugin will potentially require its own credentials. A config file
for each plugin should be installed next to that plugin.

### Twitter

Visit http://dev.twitter.com and create your twitter credentials for this
application to use. Once you've fetched a consumer key, consumer secret,
access token and access token secret, copy the example config file at
`eventcosnume/consumers/twitter.yml.example` to `eventcosnume/consumers/twitter.yml`
and make your edits.


