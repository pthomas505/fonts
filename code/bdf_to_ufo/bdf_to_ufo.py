import argparse
import numpy as np
import os
import xml.etree.ElementTree as ET

# https://font.tomchen.org/bdfparser_py/
from bdfparser import Font

import ufo_naming


def main():
  parser = argparse.ArgumentParser(description='Creates a UFO font from a BDF font by translating each filled pixel in the BDF font to a vector square.')
  parser.add_argument('bdf_file_path', type=str)
  parser.add_argument('ufo_folder_path', type=str)
  parser.add_argument('--units_per_em', type=int, default=2048, help='The units per em of the generated UFO font.')
  parser.add_argument('--scale', type=int, default=128, help='The length of the sides of the vector squares in the generated UFO font.')
  args = parser.parse_args()

  font = Font(args.bdf_file_path)

  contents_node = ET.Element('plist', version='1.0')
  dict_node = ET.SubElement(contents_node, 'dict')

  for glyph in font.iterglyphs():
    xml = process_glyph(font, glyph, args.scale)

    glyph_name = glyph.meta['glyphname']
    glyph_file_name = ufo_naming.userNameToFileName(glyph_name + '.glif')

    key_node = ET.SubElement(dict_node, 'key')
    key_node.text = glyph_name
    string_node = ET.SubElement(dict_node, 'string')
    string_node.text = glyph_file_name

    glyph_file_path = args.ufo_folder_path + '/glyphs/' + glyph_file_name
    os.makedirs(os.path.dirname(glyph_file_path), exist_ok=True)
    with open(glyph_file_path, mode='w', encoding="utf-8") as f:
      f.write(xml)
      f.write('\n')

  contents_file_path = args.ufo_folder_path + '/glyphs/contents.plist'
  os.makedirs(os.path.dirname(contents_file_path), exist_ok=True)
  with open(contents_file_path, mode='w', encoding='utf-8') as f:
    f.write(ET.tostring(contents_node, encoding='unicode'))
    f.write('\n')


  # fontinfo.plist

  fontinfo_node = ET.Element('plist', version='1.0')
  dict_node = ET.SubElement(fontinfo_node, 'dict')
  key_node = ET.SubElement(dict_node, 'key')
  key_node.text = 'unitsPerEm'
  integer_node = ET.SubElement(dict_node, 'integer')
  integer_node.text = str(args.units_per_em)

  fontinfo_file_path = args.ufo_folder_path + '/fontinfo.plist'
  with open(fontinfo_file_path, mode='w', encoding='utf-8') as f:
    f.write(ET.tostring(fontinfo_node, encoding='unicode'))
    f.write('\n')


  # metainfo.plist

  metainfo_node = ET.Element('plist', version='1.0')
  dict_node = ET.SubElement(metainfo_node, 'dict')
  key_node = ET.SubElement(dict_node, 'key')
  key_node.text = 'formatVersion'
  integer_node = ET.SubElement(dict_node, 'integer')
  integer_node.text = '3'

  metainfo_file_path = args.ufo_folder_path + '/metainfo.plist'
  with open(metainfo_file_path, mode='w', encoding='utf-8') as f:
    f.write(ET.tostring(metainfo_node, encoding='unicode'))
    f.write('\n')


def process_glyph(font, glyph, scale):
  bmp = glyph.draw()
  data = np.array(bmp.todata(2))
  data = data.transpose()
  data = np.fliplr(data)

  fbbx = font.headers['fbbx']
  fbbyoff = font.headers['fbbyoff']

  A = np.array([0, 0])
  B = np.array([0, 1])
  C = np.array([1, 1])
  D = np.array([1, 0])

  contour_list = []
  for (x, y), value in np.ndenumerate(data):
    if value == 1:
      contour_list.append((np.array([A, B, C, D]) + (x, y) + (0, fbbyoff)) * scale)

  glyph_node = ET.Element('glyph', name=glyph.meta['glyphname'], format='2')
  advance_node = ET.SubElement(glyph_node, 'advance', width=str(fbbx * scale + scale))
  unicode_node = ET.SubElement(glyph_node, 'unicode', hex='{:04X}'.format(glyph.cp()))
  outline_node = ET.SubElement(glyph_node, 'outline')
  for contour in contour_list:
    contour_node = ET.SubElement(outline_node, 'contour')
    for point in contour:
      ET.SubElement(contour_node, 'point', x=str(point[0]), y=str(point[1]), type='line')

  return ET.tostring(glyph_node, encoding="unicode")


main()
