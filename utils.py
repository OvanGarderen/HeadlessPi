from pathlib import Path

def realpath(path):
    return Path(path).expanduser().as_posix()

# class that traverses a directory and returns the files as json
# @todo make interactive (instead of slow)
class DirectoryCrawl:
    def __init__(self, base, search = '', depth = -1):
        self._path = Path(base).expanduser()
        print(self._path);
        self._results = self.read_dir(self._path)
        self._results['name'] = '/'

    def read_dir(self, path, depth = -1):
        # recurse
        if not path.is_dir() or depth == 0:
            children = None
        elif depth == -1:
            children = sorted([self.read_dir(x, depth = -1) for x in path.iterdir()], key=lambda x: x['name'])
        else:
            children = sorted([self.read_dir(x, depth = depth - 1) for x in path.iterdir()], key=lambda x: x['name'])

        # make dictionary
        return {'path' : path.relative_to(self._path).as_posix(), 'name' : path.parts[-1], 'isdir' : path.is_dir(), 'children' : children}
        
    def results(self):
        return self._results

from configparser import ConfigParser

# wrap the configparser 
class Config:    
    def __init__(self, path):
        self._path = Path(path).expanduser().as_posix()
        self._config = ConfigParser()
        self._config.read(self._path)

    # get all the options in a section
    def get(self, section):
        try:
            return dict(self._config.items(section))
        except:
            print("No section", section, "in config", self._path)
            return dict()

    def sections(self):
        return self._config.sections()
