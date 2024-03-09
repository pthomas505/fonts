# Patrick J. Thomas

import argparse

# https://font.tomchen.org/bdfparser_py/
import bdfparser

import fontforge
import numpy
import shapely
import skimage


def main():
  parser = argparse.ArgumentParser(description='Creates a vector font from a BDF font by translating each filled pixel in the BDF font to a vector square.')

  parser.add_argument('bdf_file_path', type=str)
  parser.add_argument('output_font_path', type=str)

  parser.add_argument('--units_per_em', type=int, default=2048, help='The units per em of the generated font.')
  parser.add_argument('--scale', type=int, default=128, help='The length of the sides of the vector squares in the generated font.')

  args = parser.parse_args()

  bdf_font = bdfparser.Font(args.bdf_file_path)
  fbbx = bdf_font.headers['fbbx']

  ff_font = fontforge.font()
  ff_font.strokedfont = 1
  ff_font.em = args.units_per_em

  for bdf_glyph in bdf_font.iterglyphs():
    polygon_list = process_glyph(bdf_font, bdf_glyph, args.scale)

    codepoint = bdf_glyph.meta['codepoint']

    chr = ff_font.createChar(codepoint)
    pen = ff_font[codepoint].glyphPen()
    for polygon in polygon_list:
      ext_coords = tuple(polygon.exterior.coords)
      ext_coords = ext_coords[:-1]
      pen.moveTo(ext_coords[0])
      for point in tuple(ext_coords[1:]):
        pen.lineTo(point)
      pen.endPath()

    chr.canonicalContours()
    chr.canonicalStart()

    chr.width = (fbbx + 1) * args.scale

  ff_font.encoding = 'iso8859-1'
  ff_font.encoding = 'compacted'
  ff_font.generate(args.output_font_path)


def process_glyph(bdf_font, bdf_glyph, scale):
  bmp = bdf_glyph.draw()
  data = numpy.array(bmp.todata(2))
  data = data.transpose()
  data = numpy.fliplr(data)

  fbbyoff = bdf_font.headers['fbbyoff']

  labels = skimage.measure.label(data, 0, False, 1)
  regions = skimage.measure.regionprops(labels)

  polygon_list = []
  for region in regions:
    square_polygon_list = []
    for (x, y) in region.coords:
      square_coords = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
      square_coords = [((point[0] + x) * scale, (point[1] + y + fbbyoff) * scale) for point in square_coords]
      square_polygon = shapely.Polygon(square_coords)
      square_polygon_list.append(square_polygon)

    polygon = shapely.coverage_union_all(square_polygon_list)
    polygon = shapely.normalize(polygon)
    polygon = shapely.simplify(polygon, 0, True)
    polygon = shapely.normalize(polygon)
    polygon_list.append(polygon)

  return polygon_list

main()
