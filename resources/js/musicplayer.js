// start playing
var music_play = function () {
    $.ajax({
        url : "./play",
        method : "POST"
    }).done(refresh)
}

// start playing
var music_pause = function () {
    $.ajax({
        url : "./pause",
        method : "POST"
    }).done(refresh)
}

// start playing
var music_clear = function () {
    $.ajax({
        url : "./clear",
        method : "POST"
    }).done(refresh)
}

// play the next song
var music_prev = function() {
    $.ajax({
        url : "./prev",
        method : "POST"
    }).done(refresh);
}

// play the next song
var music_next = function() {
    $.ajax({
        url : "./next",
        method : "POST"
    }).done(refresh);
}

var music_add_click = function () {
    music_add($("#music-target").val())
}

// start playing
var music_add = function (target) {
    $.ajax({
        url : "./add",
        method : "POST",
        data: {target: target}
    }).done(refresh)
}

var current_id = 0

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
                var li = $('<li>').append(song.artist + " - " + song.title)
                
                // mark the current song
                if (song.id == current_id) li.addClass('selected')
                
                // set the id of the song
                li.prop("data-id", song.id)

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

        if (data.play == "play")
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

var file_click = function () {
    $this = $(this)
    console.log($this)
    music_add($this.attr('data-path'))
}

var expand_album = function (event) {
    
    // toggle expansion
    $this = $(this).toggleClass("collapsed").toggleClass("expanded")

    // find children container
    $container = $(this).siblings(".children")
    artist = $container.attr("data-artist")
    album = $container.attr("data-album")

    if ($container.hasClass("loaded"))
        return

    $.ajax({
        url : "./list_album",
        method : "GET",
        data : {"artist" : artist, "album" : album}
    }).fail(function (error) {
        $container.text("Could not load song list for album " + album)
    }).done(function (data) {

        // the container has now been loaded
        $container.addClass("loaded")

        data.forEach(function (data, index) {
            // artist description
            $song = $('<div class="entry file song">')
                .attr("data-path", data.file)
                .text(data.track + " - " + data.name)
                .click(file_click)
            
            // song
            $container.append($song)
        })
    })
}

var expand_artist = function (event) {
    
    // toggle expansion
    $this = $(this).toggleClass("collapsed").toggleClass("expanded")

    // find children container
    $container = $(this).siblings(".children")
    artist = $container.attr("data-artist")

    if ($container.hasClass("loaded"))
        return

    $.ajax({
        url : "./list_artist",
        method : "GET",
        data : {"artist" : artist}
    }).fail(function (error) {
        $container.text("Could not load album list")
    }).done(function (data) {
        // the container has now been loaded
        $container.addClass("loaded")

        data.forEach(function (album, index) {
            if (album.length == 0)
                return

            // artist container
            $album = $("<div>")

            // artist description
            $description = $('<div class="entry directory collapsed album">')
                .attr("data-album", album)
                .text(album)
                .click(expand_album)
                .appendTo($album)

            // children (albums)
            $children = $('<div class="children album">')
                .attr("data-artist", artist)
                .attr("data-album", album)
                .appendTo($album)
            
            $container.append($album)
        })
    })
}

// start playing
var music_list = function () {
    // get the data 
    var data = {search : $("#music-target").val()}

    var container = $('#directory-container')

    $.ajax({
        url : "./list",
        method : "GET",
        data: data
    }).done(function(data) {
        // empty the container
        container.empty()

        data.forEach(function (data, index) {
            if (data.name.length == 0)
                return

            // artist container
            $artist = $("<div>")

            // artist description
            $description = $('<div class="entry directory collapsed artist">')
                .attr("data-artist", data.name)
                .text(data.name)
                .click(expand_artist)
                .appendTo($artist)
            
            // children (albums)
            $children = $('<div class="children artist">')
                .attr("data-artist", data.name)
                .appendTo($artist)

            container.append($artist)
        })
    })
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
            if (!quiet) music_pause()
            
            // update icon
            icon.html('<i class="fa fa-play"></i>Play')
        } else {
            // play
            if (!quiet) music_play()

            // update icon
            icon.html('<i class="fa fa-pause"></i>Pause')
        }
    }.bind($('#play-button'))

    // set button callbacks
    $('#play-button').click(function () { toggle_play(false) })
    $('#clear-button').click(music_clear)
    $('#add-button').click(music_add)
    $('#prev-button').click(music_prev)
    $('#next-button').click(music_next)

    toggle_play(true)

    music_list();

    // load data async
    refresh()

    // refresh every once in a while
    setInterval(refresh, 20 * 1000)
})
