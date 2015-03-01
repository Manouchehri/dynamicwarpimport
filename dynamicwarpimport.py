# This is a sample program that shows downloading and dynamically importing a module.

__author__ = 'David Manouchehri (david@davidmanouchehri.com)'

try:  # Python 3
    import urllib.request as urllib2
    from urllib.parse import urlparse
except ImportError:  # Python 2
    import urlparse
    import urllib2


def grab_module(url, name=''):
    print('Downloading ' + url + '...')
    content = urllib2.urlopen(url).read().decode('utf-8')  # Decode is not needed in Python 2.
    if not name:
        import os
        # Split the URL, get the name of the file and slice the extension off.
        name = os.path.splitext(os.path.basename(urlparse.urlsplit(url).path))[0]
        print('Name not given, importing as ' + name)

    try:
        import sys
        import imp  # imp is not as reliable, and may fail.

        module = imp.new_module(name)
        exec(content, module.__dict__)

        sys.modules[name] = module
        globals()[name] = __import__(name)
    except ImportError:
        c = {}
        exec(content, c)

        class Holder(object):
            pass
        tester = Holder()

        for key, value in c.iteritems():
            setattr(tester, key, value)
        globals()[name] = tester

    print('Successfully imported ' + name)

if __name__ == '__main__':
    # Simply give the full URL and the name you want to give to the module.
    grab_module('https://gist.githubusercontent.com/Manouchehri/dc93dc6f5d1ce7a16862/'
                'raw/331d708a272b13576fc6bd526b906043c54c2feb/test.py', 'tester')
    tester.printhello()

    grab_module('http://svn.python.org/projects/python/trunk/Lib/subprocess.py', 'suby')
    suby.call(["df", "-h"])

    # Alternatively, you can leave out the name and the name will be automatically set to the filename.
    grab_module('http://svn.python.org/projects/python/trunk/Lib/subprocess.py')
    subprocess.call(["df", "-h"])