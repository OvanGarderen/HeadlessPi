from flask import Flask, request, render_template, redirect, url_for, abort, Markup
from flask.json import jsonify

from pathlib import Path

from musicserver import MusicServer
from videoserver import VideoServer
from plugin import Server

# initialise the server
app = Flask(__name__, static_folder = 'resources', template_folder = "resources")

# try to open config
from utils import Config

modconfig = Config('~/.config/headlesspi/modules.config')
defconfig = Config('~/.config/headlesspi/defaults.config')

modules = dict()
menu = ""
for module in modconfig.sections():
    # get the settings
    settings = modconfig.get(module)

    # discern the type
    mtype = settings.get('mod-type', 'unknown')

    if mtype in ['videoplayer', 'video']:
        mod = VideoServer(defconfig.get('videoplayer'), settings)
    elif mtype in ['mpd', 'musicplayer', 'music']:
        mod = MusicServer(defconfig.get('musicplayer'), settings)
    else:
        mod = Server(defconfig.get('server'), settings)

    # save the module
    modules[module] = mod

    # we allow the mod to set defaults
    mname = mod.name()
    micon = mod.icon()

    # add a menu line
    menu += Markup('<a href="/%s/"><i class="fa fa-%s"></i>%s</a>') % (module, micon, mname)    

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
    # try to start the server on port 80
    try:
        app.run(host = "0.0.0.0", port = 80, debug=True)
    # otherwise we run on port 5000
    except:
        app.run(host = "0.0.0.0", debug = True)
