import distutils
import py2exe
distutils.core.setup(
      console=['pyFetch.py'],
      zipfile=None,
      options={'py2exe':{
                         
                        }
      }
  )
