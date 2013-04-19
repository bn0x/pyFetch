from distutils.core import setup
import py2exe

buildinfo = open('buildinfo').read()

setup(
	name="pyFetch",
    console=[
    	{
    		'script': 'pyFetch.py',
    		'other_resources': [
    			(u'buildinfo', 1, buildinfo)
    		],
    	}
    ],
    zipfile=None,
    options={ 'py2exe':
    	{
			'bundle_files': 1,
    	}
    }
)
