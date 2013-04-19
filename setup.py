from distutils.core import setup
import py2exe

setup(
    console=[ 'pyFetch.py' ],
    options={ 'py2exe': 
    	{
			'skip_archive': True,
    	}
    }
)
