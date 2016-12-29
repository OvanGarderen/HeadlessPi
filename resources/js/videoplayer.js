// start playing
var video_add = function () {
    // get the data 
    var data = {target : $("#video-target").val()}

    video_play(data)
}

var video_play = function (data) {
    $('#status-text').text("Playing " + data.target + " ...");

    $.ajax({
        url : "./play",
        method : "POST",
        data: data
    }).fail(function() {
        $('#status-text').text("Could not play file " + data.target + ".");
    }).done(function() {
        $('#status-text').text("Finished playing");
    })
}


// start playing
var video_play_local = function () {
    // get the data 
    var data = {target : $("#video-target").val()}

    var status = $('#status-text')
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
    console.log($(this))
}

var file_click = function () {
    $this = $(this)

    data = {target : $this.attr('data-path')}

    console.log(data)
    console.log($this)

    video_play(data)
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
$(document).ready( function() {

    // set button callbacks
    $('#play-button').click(video_add)

    // set button callbacks
    $('#play-local-button').click(video_play_local)

    video_list()
})
