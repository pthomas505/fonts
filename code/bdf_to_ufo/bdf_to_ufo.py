import argparse

# https://github.com/tomchen/bdfparser
import bdfparser

import numpy
import pathlib

import xml.etree.ElementTree as ET

import ufo_naming


# The array indices place the origin at the top left.
# The graph coordinates place the origin at the bottom left.
# The origin is (0, 0) for both.
# array.shape[0] is the number of rows in the array.
# array.shape[1] is the number of columns in the array.

# Translates the given row and column indices to x and y graph coordinates.
def rc_to_xy(array, r, c):
  r_max = array.shape[0] - 1
  y = r_max - r
  x = c
  return (x, y)


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('bdf_file_path', type=pathlib.Path)
  parser.add_argument('ufo_file_path', type=pathlib.Path)
  parser.add_argument('scale', type=int)
  parser.add_argument('units_per_em', type=int)

  args = parser.parse_args()


  args.ufo_file_path.mkdir(exist_ok=True)


  # fontinfo.plist

  fontinfo_file_path = args.ufo_file_path / 'fontinfo.plist'

  fontinfo_node = ET.Element('plist', version='1.0')
  dict_node = ET.SubElement(fontinfo_node, 'dict')
  key_node = ET.SubElement(dict_node, 'key')
  key_node.text = 'unitsPerEm'
  integer_node = ET.SubElement(dict_node, 'integer')
  integer_node.text = str(args.units_per_em)

  tree = ET.ElementTree(fontinfo_node)
  ET.indent(tree)
  tree.write(str(fontinfo_file_path), encoding="unicode", xml_declaration=True)


  # metainfo.plist

  metainfo_file_path = args.ufo_file_path / 'metainfo.plist'

  metainfo_node = ET.Element('plist', version='1.0')
  dict_node = ET.SubElement(metainfo_node, 'dict')
  key_node = ET.SubElement(dict_node, 'key')
  key_node.text = 'formatVersion'
  integer_node = ET.SubElement(dict_node, 'integer')
  integer_node.text = '3'

  tree = ET.ElementTree(metainfo_node)
  ET.indent(tree)
  tree.write(str(metainfo_file_path), encoding="unicode", xml_declaration=True)


  # .glif files

  glyphs_folder_path = args.ufo_file_path / 'glyphs'
  glyphs_folder_path.mkdir(exist_ok=True)

  font = bdfparser.Font(str(args.bdf_file_path))

  fbbx = font.headers['fbbx']
  fbbyoff = font.headers['fbbyoff']

  glyph_name_to_glyph_file_name_dict = {}

  for glyph in font.iterglyphs():
    glyph_name = glyph.meta['glyphname'].split('.')[0]
    glyph_node = ET.Element('glyph', name=glyph_name, format='2')

    advance = (fbbx + 1) * args.scale
    ET.SubElement(glyph_node, 'advance', width=str(advance))

    unicode = '{:04X}'.format(glyph.cp())
    ET.SubElement(glyph_node, 'unicode', hex=unicode)

    outline_node = ET.SubElement(glyph_node, 'outline')

    bmp = glyph.draw()
    data = numpy.array(bmp.todata(2))
    data = numpy.flipud(data)

    point_list = numpy.array([[0, 0], [0, 1], [1, 1], [1, 0]])

    for row in range(data.shape[0]):
      for col in range(data.shape[1]):
        if data[row, col] == 1:
          x = col
          y = row

          transformed_point_list = (point_list + (x, y) + (0, fbbyoff)) * args.scale

          contour_node = ET.SubElement(outline_node, 'contour')

          for transformed_point in transformed_point_list:
            ET.SubElement(contour_node, 'point', x=str(transformed_point[0]), y=str(transformed_point[1]), type='line')

    glyph_file_name = ufo_naming.userNameToFileName(glyph_name + '.glif')
    glyph_file_path = glyphs_folder_path / glyph_file_name

    tree = ET.ElementTree(glyph_node)
    ET.indent(tree)
    tree.write(str(glyph_file_path), encoding="unicode", xml_declaration=True)

    glyph_name_to_glyph_file_name_dict[glyph_name] = glyph_file_name


  # contents.plist

  contents_file_path = glyphs_folder_path / 'contents.plist'

  contents_node = ET.Element('plist', version='1.0')
  dict_node = ET.SubElement(contents_node, 'dict')
  for glyph_name, glyph_file_name in glyph_name_to_glyph_file_name_dict.items():
    key_node = ET.SubElement(dict_node, 'key')
    key_node.text = glyph_name
    string_node = ET.SubElement(dict_node, 'string')
    string_node.text = glyph_file_name

  tree = ET.ElementTree(contents_node)
  ET.indent(tree)
  tree.write(str(contents_file_path), encoding="unicode", xml_declaration=True)


if __name__ == "__main__":
  main()
