# Patrick J. Thomas

from robofab.world import OpenFont
import math

def main():

	class options_type:
		pass

	options = options_type()
	guide_distances = set()
	unicode_values = []


	options.scale = 128
	options.min = -15
	options.max = 15

	# [options.min, ..., options.max - 1]
	for offset in range(options.min, options.max):
		cell_distances = create_cell_distances(options.scale, offset)
		guide_distances = guide_distances | cell_distances


	path = raw_input("path to UFO font: ")
	if not path:
		return

	font = OpenFont(path)

	for glyph in font:
		unicode_values.append(glyph.unicode)

	character_mapping = font.getCharacterMapping()
	for unicode_value in sorted(unicode_values):
		name = character_mapping[unicode_value][0]
		glyph = font[name]
		for contour in glyph:
			for point in contour.points:
				if point.x not in guide_distances or point.y not in guide_distances:
					print glyph.name + ': (' + str(point.x) + ', ' + str(point.y) + ')'


def create_cell_distances(scale, offset):
	sqrt2 = math.sqrt(2.0)

	d0 = 0.0
	d1 = 1.0 / sqrt2 - 0.5
	d2 = 1.0 - 1.0 / sqrt2
	d3 = 0.5
	d4 = 1.0 / sqrt2
	d5 = 1.0 - 1.0 / sqrt2 + 0.5
	d6 = 1.0

	distances = set([d0, d1, d2, d3, d4, d5, d6])
	distances = set(scale * (distance + offset) for distance in distances)
	distances = set(int(round(distance)) for distance in distances)

	return distances

main()

