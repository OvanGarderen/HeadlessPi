// start playing
var video_play_remote = function () {
    // get the data 
    var data = {target : $("#video-target").val()}

    video_play(data)
}

var video_play = function (data) {
    $.ajax({
        url : "./play",
        method : "POST",
        data: data
    }).fail(function() {
        $('#video-description').text("Could not play file " + data.target + ".");
    })
}

var video_pause = function (data) {
    $.ajax({
        url: "./pause",
        method : "POST",
    })
}

var video_stop = function (data) {
    $.ajax({
        url: "./stop",
        method : "POST",
    })
}

// start playing
var video_play_local = function () {
    // get the data 
    var data = {target : $("#video-target").val()}

    var status = $('#video-description')
    var container = $('#video-container')

    container.empty()

    $.ajax({
        url : "./play-local",
        method : "GET",
        data: data
    }).fail(function() {
        status.text("Could not find file " + data.target + ".")
    }).done(function(data) {
        // create video tag
        video = $('<video width="800" height="600" preload="none" controls autoplay>')

        // set the actual video source
        video.append($('<source>').prop('type', data.type).prop('src', data.src))

        // add to the container
        video.appendTo(container)
    })
}

var dir_expand = function () {
    $(this).toggleClass('collapsed').toggleClass('expanded')
}

var file_click = function () {
    // find the target
    target = $(this).attr('data-path')
    
    data = {target : target}

    $.ajax({
        url: "./metadata",
        data: data
    }).fail(function (){
        $('#video-description').text("Could not find description for file " + data.target + ".")
    }).done(function (data){
        // update description
        $('#video-description').text(data.description)

        // update thumbnail
        var $thumb = $('#video-thumbnail')
        $thumb.empty()
   
        var thumburl = encodeURI(data.thumbnail)
        
        // set the thumbnail
        if (data.thumbnail)
            $thumb.prop('style','background-image: url("' + thumburl + '"')

        // set the file target
        $('#video-target').val(target)
    })
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
var video_list = function () {
    // get the data 
    var data = {search : $("#video-target").val()}

    var status = $('#video-description')
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

// seek callback
var video_seek = function (value) {
    $.ajax({
        url : "./seek",
        method : "POST",
        data: {value: value}
    })
}

// install callbacks
$(document).ready( function() {

    // set button callbacks
    $('#play-button').click(video_play_remote)
    $('#play-local-button').click(video_play_local)
    $('#pause-button').click(video_pause)
    $('#stop-button').click(video_stop)
    
    // initialise the slider
    var slider = new Slider($('#track-slider'), video_seek)     

    video_list()

    var getState = function () {
        $.ajax({
            url : "./state",
            method : "GET"
        }).done(function (data) {
            if (data == undefined)
                return

            // set seek slider
            slider.update(data.position)

            // check if the pause button needs to be updated
            var pause = $('#pause-button')
            var childpaused = !pause.children('i').hasClass('fa-pause')
            var changed = data.paused ? !childpaused : childpaused;

            console.log('pausedd', childpaused)
            console.log('changed', changed)
            console.log('data', data.paused)
            // change the pause button appearance
            if (changed) {
                pause.empty()
                
                if (data.paused) {
                    pause.append($('<i class="fa fa-play">'))
                    pause.append("Continue")
                } else {
                    pause.append($('<i class="fa fa-pause">'))
                    pause.append("Pause")                
                }
            }
        })
    }

    // load data async
    getState()

    // refresh every once in a while
    setInterval(getState, 1000)
})
