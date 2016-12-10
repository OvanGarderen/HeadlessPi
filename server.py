from flask import Flask, request, render_template, redirect, url_for, abort, Markup
from flask.json import jsonify

from musicserver import MusicServer
from videoserver import VideoServer

# initialise the server
app = Flask(__name__, static_folder = 'resources', template_folder = "resources")

# module dictionary
modules = {
    'musicplayer' : MusicServer(),
    'films' : VideoServer('Films', '/root/film'),
    'documentaries' : VideoServer('Documentaries', '/root/documentaries'),
    'comedy' : VideoServer('Comedy', '/root/comedy'),    
    'series' : VideoServer('Series', '/root/series'),
    'cartoons' : VideoServer('Cartoons', '/root/cartoons'),
    'anime' : VideoServer('Anime', '/root/anime')                
}

# construct menu
menu = ""
for module in sorted(modules.keys()):
    mod = modules[module]

    # get vars from mod
    module_name = mod.name()
    module_icon = mod.icon()

    # add menu entry
    menu += Markup('<a href="/%s/"><i class="fa fa-%s"></i>%s</a>') % (module, module_icon, module_name)

# main interface
@app.route("/")
def interface():
    return render_template("index.html", menu = menu)

# access a module
@app.route("/<string:module>/")
def render_module(module):
    if module not in modules:
        abort(404)

    # get the module
    mod = modules[module]

    return mod.render(get = request.args, template_args = {'menu' : menu} )

# send command to module
@app.route("/<string:module>/<path:command>", methods=['GET', 'POST'])
def command_module(module, command):
    if module not in modules:
        abort(404)

    # get the module
    mod = modules[module]
    
    # send command
    if request.method == 'POST':
        return mod.post(command, request.form, get = request.args)
    else:
        return mod.get(command, get = request.args)

# run the server
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80, debug = True)
