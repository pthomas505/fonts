import argparse

import fontforge

import pathlib

import xml.etree.ElementTree as ET


# Opens a font in FontForge and exports it as a minimal UFO font.


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('input_file_path', type=pathlib.Path)
  parser.add_argument('ufo_file_path', type=pathlib.Path)

  args = parser.parse_args()


  font = fontforge.open(str(args.input_file_path))

  args.ufo_file_path.mkdir(exist_ok=True)


  # fontinfo.plist

  fontinfo_file_path = args.ufo_file_path / 'fontinfo.plist'

  fontinfo_node = ET.Element('plist', version='1.0')
  dict_node = ET.SubElement(fontinfo_node, 'dict')
  key_node = ET.SubElement(dict_node, 'key')
  key_node.text = 'unitsPerEm'
  integer_node = ET.SubElement(dict_node, 'integer')
  integer_node.text = str(font.em)

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

  glyph_name_to_glyph_file_name_dict = {}

  for glyph in font.glyphs():
    glyph_name = glyph.glyphname
    glyph_node = ET.Element('glyph', name=glyph_name, format='2')

    advance = glyph.width
    ET.SubElement(glyph_node, 'advance', width=str(advance))

    unicode = '{:04X}'.format(glyph.unicode)
    ET.SubElement(glyph_node, 'unicode', hex=unicode)

    outline_node = ET.SubElement(glyph_node, 'outline')

    layer = glyph.foreground

    for contour in layer:
      contour_node = ET.SubElement(outline_node, 'contour')

      for point in contour:
        ET.SubElement(contour_node, 'point', x=str(point.x), y=str(point.y), type='line')

    glyph_file_name = glyph_name + '.glif'
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
