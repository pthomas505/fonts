# Patrick J. Thomas

import argparse

# https://font.tomchen.org/bdfparser_py/
import bdfparser

import fontforge
import matplotlib.pyplot as plt
import numpy as np
import shapely

import array_to_polygons


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
  ff_font.encoding = 'iso10646-1'
  ff_font.em = args.units_per_em

  for bdf_glyph in bdf_font.iterglyphs():
    multi_polygon_list = process_glyph(bdf_font, bdf_glyph, args.scale)

    codepoint = bdf_glyph.meta['codepoint']

    chr = ff_font.createChar(codepoint)
    pen = ff_font[codepoint].glyphPen()
    for polygon in shapely.get_parts(multi_polygon_list):
      ext_coords = tuple(polygon.exterior.coords)
      ext_coords = ext_coords[:-1]
      pen.moveTo(ext_coords[0])
      for point in tuple(ext_coords[1:]):
        pen.lineTo(point)
      pen.endPath()
      #plt.plot(*polygon.exterior.xy)
    #plt.axis('square')
    #plt.show()

    chr.canonicalContours()
    chr.canonicalStart()

    chr.width = (fbbx + 1) * args.scale

  ff_font.encoding = 'compacted'
  ff_font.generate(args.output_font_path)


def process_glyph(bdf_font, bdf_glyph, scale):
  bmp = bdf_glyph.draw()
  array = np.array(bmp.todata(2))

  multi_polygon_list = array_to_polygons.array_to_multi_polygon_list(array)

  fbbyoff = bdf_font.headers['fbbyoff']
  multi_polygon_list = shapely.affinity.translate(multi_polygon_list, xoff=0, yoff=fbbyoff)

  multi_polygon_list = shapely.affinity.scale(multi_polygon_list, xfact=scale, yfact=scale, origin=(0, 0))

  return multi_polygon_list


main()
