import pyFetch.Debug
import pyFetch.Platform
import pyFetch.Art
import pyFetch.Format

import gpu
import normal

def draw(system, options, args, mode):
	if mode == gpu:
		return gpu.draw(system, options, args)

	else:
		return normal.draw(system, options, args)