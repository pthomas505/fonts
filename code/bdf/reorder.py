import argparse

# https://gitlab.com/Screwtapello/bdflib/
from bdflib import reader, writer

import pathlib


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('bdf_file_path_input', type=pathlib.Path)
  parser.add_argument('bdf_file_path_output', type=pathlib.Path)

  args = parser.parse_args()


  with open(str(args.bdf_file_path_input), 'rb') as handle:
    font = reader.read_bdf(handle)

  font.glyphs = sorted(font.glyphs, key=lambda glyph: glyph.codepoint)

  with open(str(args.bdf_file_path_output), 'wb') as handle:
    writer.write_bdf(font, handle)


if __name__ == "__main__":
  main()
