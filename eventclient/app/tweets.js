
// Globals here to store map and our current map markers
var map;
var map_markers = [];


// Haversine stuff stolen from here: https://gist.github.com/kirbysayshi/417612
function haversine(latA, longA, latB, longB){
    var dLat = (latA - latB).toRad(); 
    var dLon = (longA - longB).toRad();
    var dLatDiv2 = dLat / 2;
    var dLonDiv2 = dLon / 2;
    var latBRad = latB.toRad();
    var latBRadCos = Math.cos(latBRad);
    var dLatDiv2Sin = Math.sin(dLatDiv2);
    var dLonDiv2Sin = Math.sin(dLonDiv2);
    var a = dLatDiv2Sin * dLatDiv2Sin + latBRadCos * latBRadCos * dLonDiv2Sin * dLonDiv2Sin;
    return 6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

Number.prototype.toRad = function() {
    return this * 3.14 / 180;
}

function updateStatusMessage(tweet_count) {
    var status = '';
    if (tweet_count === 0) {
        status = "No tweets match your search.";
    } else if (tweet_count === 1) {
        status = "One tweet matches your search.";
    } else {
        status = tweet_count + " tweets match your search.";
    }
    $('#status').html(status);
}

function clearMarkers() {
    // blow away all existing markers
    map_markers.forEach(function (marker) {
        marker.setMap(null);
    });
    map_markers = [];

}

function tweetIsValid(tweet) {
    // a tweet is valid if it's within our current viewport in order
    // to clean up the display if the backend returns us some bad data
    bounds = map.getBounds();
    neLat = bounds.getNorthEast().lat();
    neLng = bounds.getNorthEast().lng();
    swLat = bounds.getSouthWest().lat();
    swLng = bounds.getSouthWest().lng();
    twLat = tweet.location[1];
    twLng = tweet.location[0];

    if (swLat < twLat && twLat < neLat &&
        swLng < twLng && twLng < neLng) {
        return true;
    } else {
        return false;
    }
}

function displayTweets(tweets) {
    container = $('#tweets');
    container.empty();

    template = $('#tweetTemplate');
    label = 1;

    clearMarkers();
    tweets.forEach(function (hit) {
        if (!tweetIsValid(hit)) {
            return;
        }
        tweet = template.clone();
        tweet.find('#label').text(label.toString());
        tweet.find('#message').text(hit.message);
        tweet.find('#creator').text(hit.creator);
        var dateString = new Date(Number(hit.timestamp)).toLocaleString();
        tweet.find('#timestamp').text(dateString);
        tweet.css('visibility', 'initial');

        var marker = new google.maps.Marker({
            position: {lat: hit.location[1], lng: hit.location[0]},
            label: label.toString(),
            map: map
        });
        map_markers.push(marker);
        container.append(tweet);

        label++;
    });
}

function updateTweets() {
    var tags = $('#tags_input').val();

    bounds = map.getBounds();
    neLat = bounds.getNorthEast().lat();
    neLng = bounds.getNorthEast().lng();
    swLat = bounds.getSouthWest().lat();
    swLng = bounds.getSouthWest().lng();

    lat = swLat + (neLat - swLat) / 2;
    lng = swLng + (neLng - swLng) / 2;

    // A circular inscribed within the square will miss some elements
    // but this will will get some false positives which I think is
    // better. Even better would be to use the real bounding box within
    // the ES query but this may have performance implications
    radius = haversine(swLat, swLng, neLat, neLng) / 2;
    console.log('got radius: ' + radius);

    $.get('http://jerryhebert.me/events_api/events', {
        lat: lat,
        lon: lng,
        distance: Math.trunc(radius).toString() + "km",
        tags: tags
    }, function (data) {
        updateStatusMessage(data.total);
        displayTweets(data.hits);
    });
};


function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.2858, lng: -122.141},
        zoom: 8
    });

    map.addListener('dragend', function () {
        updateTweets();
    });

    map.addListener('zoom_changed', function () {
        updateTweets();
    });

    // there doesn't seem to be a great event for "on map loaded" but this works.. 
    map.addListener('projection_changed', function () {
        updateTweets();
    });
}

$(document).ready(function () {
    $("#searchForm").on('submit', function () {
        return false;
    });

});

