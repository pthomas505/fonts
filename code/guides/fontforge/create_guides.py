# Patrick J. Thomas

import fontforge
import math

def main():
	f = fontforge.activeFont()
	guide = fontforge.layer()

	class options_type:
		pass

	options = options_type()

	options.scale = 128
	options.x_min = 0
	options.x_max = 10
	options.y_min = -5
	options.y_max = 15

	# [x_min, ..., x_max - 1]
	for x in range(options.x_min, options.x_max):
		# [y_min, ..., y_min - 1]
		for y in range(options.y_min, options.y_max):
			contours = create_cell_contours(x, y, options.scale)
			for c in contours:
				guide += c

	f.guide = guide

def create_cell_contours(x_offset, y_offset, scale):
	sqrt2 = math.sqrt(2.0)

	p0 = (0.0, 0.0)
	p1 = (0.0, 1.0)
	p2 = (1.0, 1.0)
	p3 = (1.0, 0.0)
	p4 = (1.0 - 1.0 / sqrt2, 0.0)
	p5 = (0.0, 1.0 - 1.0 / sqrt2)
	p6 = (1.0 / sqrt2 - 0.5, 0.5)
	p7 = (0.0, 1.0 / sqrt2)
	p8 = (1.0 - 1.0 / sqrt2, 1.0)
	p9 = (0.5, 1.0 - 1.0 / sqrt2 + 0.5)
	p10 = (1.0 / sqrt2, 1.0)
	p11 = (1.0, 1.0 / sqrt2)
	p12 = (1.0 - 1.0 / sqrt2 + 0.5, 0.5)
	p13 = (1.0, 1.0 - 1.0 / sqrt2)
	p14 = (1.0 / sqrt2, 0.0)
	p15 = (0.5, 1.0 / sqrt2 - 0.5)

	points = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15]
	points = [(scale * (p[0] + x_offset), scale * (p[1] + y_offset)) for p in points]
	points = [(round(p[0]), round(p[1])) for p in points]

	p0 = points[0]
	p1 = points[1]
	p2 = points[2]
	p3 = points[3]
	p4 = points[4]
	p5 = points[5]
	p6 = points[6]
	p7 = points[7]
	p8 = points[8]
	p9 = points[9]
	p10 = points[10]
	p11 = points[11]
	p12 = points[12]
	p13 = points[13]
	p14 = points[14]
	p15 = points[15]

	s0 = (p0, p5)
	s1 = (p5, p7)
	s2 = (p7, p1)
	s3 = (p1, p8)
	s4 = (p8, p10)
	s5 = (p10, p2)
	s6 = (p2, p11)
	s7 = (p11, p13)
	s8 = (p13, p3)
	s9 = (p3, p14)
	s10 = (p14, p4)
	s11 = (p4, p0)
	s12 = (p4, p5)
	s13 = (p5, p6)
	s14 = (p6, p7)
	s15 = (p7, p8)
	s16 = (p8, p9)
	s17 = (p9, p10)
	s18 = (p10, p11)
	s19 = (p11, p12)
	s20 = (p12, p13)
	s21 = (p13, p14)
	s22 = (p14, p15)
	s23 = (p15, p4)
	s24 = (p6, p9)
	s25 = (p9, p12)
	s26 = (p12, p15)
	s27 = (p15, p6)

	segments = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27]

	contours = []

	for i in segments:
		x1 = i[0][0]
		y1 = i[0][1]
		x2 = i[1][0]
		y2 = i[1][1]

		c = fontforge.contour()
		c.moveTo(x1, y1)
		c.lineTo(x2, y2)

		contours.append(c)

	return contours

main()

