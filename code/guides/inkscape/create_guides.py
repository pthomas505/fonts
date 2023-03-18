# Patrick J. Thomas

import inkex
import math

def createGuide(position, orientation, parent):
	# Creates a sodipodi:guide node
	# (look into inkex's namespaces to find 'sodipodi' value in order to make a "sodipodi:guide" tag)
	inkex.etree.SubElement(parent, '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide', {'position':position, 'orientation':orientation})

class Create_Guides(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

		self.OptionParser.add_option("--scale",
		action = "store", type = "int", 
		dest = "scale", help = "Scale")

		self.OptionParser.add_option("--x_min",
		action = "store", type = "int",
		dest = "x_min", help = "X min");

		self.OptionParser.add_option("--x_max",
		action = "store", type = "int",
		dest = "x_max", help = "X max");

		self.OptionParser.add_option("--y_min",
		action = "store", type = "int",
		dest = "y_min", help = "Y min");

		self.OptionParser.add_option("--y_max",
		action = "store", type = "int",
		dest = "y_max", help = "Y max");

	def effect(self):
		scale = self.options.scale

		x_min = self.options.x_min * scale
		x_max = self.options.x_max * scale
		y_min = self.options.y_min * scale
		y_max = self.options.y_max * scale

		sqrt2 = math.sqrt(2.0)


		# removes any existing guides

		nv = self.document.xpath('/svg:svg/sodipodi:namedview', namespaces = inkex.NSS)[0]

		# gets all the guides
		children = self.document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide', namespaces = inkex.NSS)

		# removes each guide
		for element in children:
			nv.remove(element)


		# adds the new guides

		for x in range(x_min, x_max + 1, scale):
			# vertical guides spaced along the bottom X axis
			position = (x, y_min) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '1,0' # guide angle: 90 degrees
			createGuide(position_str, orientation_str, nv)

		for y in range(y_min, y_max + 1, scale):
			# horizontal guides spaced along the left Y axis
			position = (x_min, y) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '0,1' # guide angle: 0 degrees
			createGuide(position_str, orientation_str, nv)


		for x in range(x_min, x_max, scale):
			# 45 degree guides spaced along the bottom X axis
			position = (x + scale * (1.0 / sqrt2), y_min) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '-1,1' # guide angle: 45 degrees
			createGuide(position_str, orientation_str, nv)

			position = (x + scale * (1.0 - 1.0 / sqrt2), y_min) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '-1,1' # guide angle: 45 degrees
			createGuide(position_str, orientation_str, nv)


			# 135 degree guides spaced along the bottom X axis
			position = (x + scale * (1.0 / sqrt2), y_min) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '1,1' # guide angle: 135 degrees
			createGuide(position_str, orientation_str, nv)

			position = (x + scale * (1.0 - 1.0 / sqrt2), y_min) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '1,1' # guide angle: 135 degrees
			createGuide(position_str, orientation_str, nv)


		for y in range(y_min, y_max, scale):
			# 45 degree guides spaced along the left Y axis
			position = (x_min, y + scale * (1.0 / sqrt2)) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '-1,1' # guide angle: 45 degrees
			createGuide(position_str, orientation_str, nv)

			position = (x_min, y + scale * (1.0 - 1.0 / sqrt2)) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '-1,1' # guide angle: 45 degrees
			createGuide(position_str, orientation_str, nv)


			# 135 degree guides spaced along the right Y axis
			position = (x_max, y + scale * (1.0 / sqrt2)) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '1,1' # guide angle: 135 degrees
			createGuide(position_str, orientation_str, nv)

			position = (x_max, y + scale * (1.0 - 1.0 / sqrt2)) # guide origin
			position = (round(position[0]), round(position[1])) # round guide origin
			position_str = str(position[0]) + ',' + str(position[1])
			orientation_str = '1,1' # guide angle: 135 degrees
			createGuide(position_str, orientation_str, nv)

if __name__ == '__main__':
	effect = Create_Guides()
	effect.affect()

