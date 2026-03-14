import argparse

# https://github.com/tomchen/bdfparser
import bdfparser

import itertools
import pathlib

from PIL import Image


def main():
  parser = argparse.ArgumentParser(description="Displays each glyph in the bdf font located at 'bdf_file_path_1' above the corresponding glyph in the bdf font located at 'bdf_file_path_2'. If the glyphs differ then they are colored red.")

  parser.add_argument('bdf_file_path_1', type=pathlib.Path, help='path to BDF font')
  parser.add_argument('bdf_file_path_2', type=pathlib.Path, help='path to BDF font')
  parser.add_argument('--cols', type=int, default=32, help='maximum number of glyphs in each row')

  args = parser.parse_args()

  cols = max(args.cols, 1)

  font_1 = bdfparser.Font(str(args.bdf_file_path_1))
  font_2 = bdfparser.Font(str(args.bdf_file_path_2))

  cp_set = set(font_1.itercps()) | set(font_2.itercps())
  cp_list = sorted(list(cp_set))

  bmp_pair_list = []
  for cp in cp_list:
    glyph_1 = font_1.glyphbycp(cp)
    glyph_2 = font_2.glyphbycp(cp)

    compare_bmp_1 = bdfparser.Bitmap(['0'])
    compare_bmp_2 = bdfparser.Bitmap(['0'])

    display_bmp_1 = bdfparser.Bitmap(['0'])
    display_bmp_2 = bdfparser.Bitmap(['0'])

    if glyph_1 is not None:
      compare_bmp_1 = glyph_1.draw(1)
      display_bmp_1 = glyph_1.draw()

    if glyph_2 is not None:
      compare_bmp_2 = glyph_2.draw(1)
      display_bmp_2 = glyph_2.draw()

    if compare_bmp_1.bindata != compare_bmp_2.bindata:
      # Sets the color of the glyphs to red when translated to a PIL RGB image.
      display_bmp_1 = display_bmp_1.replace(1, 2)
      display_bmp_2 = display_bmp_2.replace(1, 2)

    bmp_pair = bdfparser.Bitmap.concatall([display_bmp_1, display_bmp_2], direction=0, align=1, offsetlist=[5])
    bmp_pair_list.append(bmp_pair)

  bmp_pair_tuple_list = list(itertools.batched(bmp_pair_list, cols))

  bmp_row_list = []
  for bmp_pair_tuple in bmp_pair_tuple_list:
    offset_list = [5] * (len(bmp_pair_tuple) - 1)
    bmp_row = bdfparser.Bitmap.concatall(bmp_pair_tuple, direction=1, align=1, offsetlist=offset_list)
    bmp_row_list.append(bmp_row)

  offset_list = [10] * (len(bmp_row_list) - 1)
  bmp = bdfparser.Bitmap.concatall(bmp_row_list, direction=0, align=1, offsetlist=offset_list)

  image = Image.frombytes('RGB', (bmp.width(), bmp.height()), bmp.tobytes())
  image.show()


if __name__ == "__main__":
  main()
