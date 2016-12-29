// start playing
var media_play = function () {
    $.ajax({
        url : "./play",
        method : "POST"
    }).done(refresh)
}

// start playing
var media_pause = function () {
    $.ajax({
        url : "./pause",
        method : "POST"
    }).done(refresh)
}

// start playing
var media_clear = function () {
    $.ajax({
        url : "./clear",
        method : "POST"
    }).done(refresh)
}

// play the next song
var media_prev = function() {
    $.ajax({
        url : "./prev",
        method : "POST"
    }).done(refresh);
}

// play the next song
var media_next = function() {
    $.ajax({
        url : "./next",
        method : "POST"
    }).done(refresh);
}

// start playing
var media_add = function () {
    // get the data 
    var data = {'target' : $("#additional-song").val()}

    $.ajax({
        url : "./add",
        method : "POST",
        data: data
    }).done(refresh)
}

// refresh the playlist
var refresh_playlist = function() {
    $.ajax({
        url : "./playlist",
        method : "GET"
    }).done(function(data){   

        // get the playlist
        var playlist = $('#playlist')

        // renew the playlist
        playlist.empty()

        if (data.length == 0)
            playlist.append("Playlist empty")
        else 
            data.forEach(function (song, index) {
                // make element
                var li = $('<li>').append(song.name)
                
                // mark the current song
                if (song.iscurrent) li.addClass('selected')
                
                // add a line to the playlist
                playlist.append(li)
            })
    })
}

// refresh the playing status
var refresh_status = function() {
    $.ajax({
        url : "./status",
        method : "GET"
    }).done(function(data){   
        var playlist = $('#playlist');

        if (data == "playing")
            playlist.addClass('playing')
        else
            playlist.removeClass('playing')
    });
}

// refresh all values
var refresh = function () {
    refresh_status()
    refresh_playlist()
}

// install callbacks
$(document).ready( function () {

    // toggle helper function
    var toggle_play = function (quiet) {
        // get the icon
        var icon = $(this)

        // check if we are allready playing
        if ($('#playlist').hasClass('playing')) {
            // pause
            if (!quiet) media_pause()
            
            // update icon
            icon.html('<i class="fa fa-play"></i>Play')
        } else {
            // play
            if (!quiet) media_play()

            // update icon
            icon.html('<i class="fa fa-pause"></i>Pause')
        }
    }.bind($('#play-button'))

    // set button callbacks
    $('#play-button').click(function () { toggle_play(false) })
    $('#clear-button').click(media_clear)
    $('#add-button').click(media_add)
    $('#prev-button').click(media_prev)
    $('#next-button').click(media_next)

    toggle_play(true)

    // load data async
    refresh()

    // refresh every once in a while
    setInterval(refresh, 30 * 1000)
})
