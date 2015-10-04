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

function displayTweets(tweets) {
    container = $('#tweets');
    container.empty();
    console.log($('#tweetTemplate'));

    template = $('#tweetTemplate');
    tweets.forEach(function (hit) {
        tweet = template.clone();
        tweet.find('#message').text(hit.message);
        tweet.find('#creator').text(hit.creator);
        var dateString = new Date(Number(hit.timestamp)).toLocaleString();
        tweet.find('#timestamp').text(dateString);
        tweet.css('visibility', 'initial');

        container.append(tweet);
    });
}

$(document).ready(function () {
    $("#searchForm").on('submit', function () {
        var lat = $('#lat_input').val();
        var lon = $('#lon_input').val();
        var radius = $('#radius_input').val();

        $.get('http://jerryhebert.me/events_api/events', {
            lat: 39.75944444, //lat,
            lon: -84.19166667, //lon,
            distance: '50000000km' //radius
        }, function (data) {
            updateStatusMessage(data.total);
            displayTweets(data.hits);
        });

        return false;
    });
});

