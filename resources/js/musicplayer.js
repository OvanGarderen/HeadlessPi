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

var dir_expand = function () {
    $(this).toggleClass('collapsed').toggleClass('expanded')
}

var file_click = function () {
    $this = $(this)

    music_add($this.attr('data-path'))
}

var show_dir = function (data) {
    var el = $('<div>')

    if (data.isdir) {
        var header = $('<div class="entry directory collapsed" data-path="' + data.path + '">').click(dir_expand).text(data.name)
        
        var children = $('<div class="children">')

        data.children.forEach(function (item, index) {
            children.append(show_dir(item))
        })

        return el.append(header).append(children)
    } else {        
        var header = $('<a class="entry file" data-path="' + data.path + '">').click(file_click).text(data.name)

        return el.append(header)
    }
}

// start playing
var music_list = function () {
    // get the data 
    var data = {search : $("#music-target").val()}

    var status = $('#status-text')
    var container = $('#directory-container')

    container.empty()

    $.ajax({
        url : "./list",
        method : "GET",
        data: data
    }).fail(function() {

        // update status
        status.text("Could not list directory.")

    }).done(function(data) {

        // get directory listing
        dirs = show_dir(data).addClass('directory-list')

        // add dir to container
        container.append(dirs)

        // auto-expand first dir
        dir_expand.bind(dirs.children('.directory'))()
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
