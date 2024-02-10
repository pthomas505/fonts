import argparse
import fontforge
import math


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('file', type=str, help='The path to a vector font that can be opened in FontForge.')
  parser.add_argument('min', type=int)
  parser.add_argument('max', type=int)
  parser.add_argument('scale', type=int)
  args = parser.parse_args()

  font = fontforge.open(args.file)

  distances = set()
  for offset in range(args.min, args.max):
    cell_distances = create_cell_distances(args.scale, offset)
    distances = distances.union(cell_distances)

  for glyph in font.glyphs():
    layer = glyph.foreground
    for contour in layer:
      for point in contour:
        if (not point.x in distances) and (not point.y in distances):
          print('{} : (*{}*, *{}*)'.format(glyph.glyphname, point.x, point.y))
        elif not point.x in distances:
          print('{} : (*{}*, {})'.format(glyph.glyphname, point.x, point.y))
        elif not point.y in distances:
          print('{} : ({}, *{}*)'.format(glyph.glyphname, point.x, point.y))


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
