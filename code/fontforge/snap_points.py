import fontforge
import math


# Moves every point in the selected glyphs to the closest point in a generated list.


def get_cell_point_list(x_offset, y_offset, scale):
  sqrt2 = math.sqrt(2.0)

  point_A = (0, 0)
  point_B = (0, 1)
  point_C = (1, 1)
  point_D = (1, 0)
  point_E = (1 - (1 / sqrt2), 0)
  point_F = (0, 1 - (1 / sqrt2))
  point_G = ((1 / sqrt2) - 0.5, 0.5)
  point_H = (0, 1 / sqrt2)
  point_I = (1 - (1 / sqrt2), 1)
  point_J = (0.5, 1 - (1 / sqrt2) + 0.5)
  point_K = (1 / sqrt2, 1)
  point_L = (1, 1 / sqrt2)
  point_M = (1 - (1 / sqrt2) + 0.5, 0.5)
  point_N = (1, 1 - (1 / sqrt2))
  point_O = (1 / sqrt2, 0)
  point_P = (0.5, (1 / sqrt2) - 0.5)

  point_list = [point_A, point_B, point_C, point_D, point_E, point_F, point_G, point_H, point_I, point_J, point_K, point_L, point_M, point_N, point_O, point_P]
  point_list = [(round(scale * (point[0] + x_offset)), round(scale * (point[1] + y_offset))) for point in point_list]

  return point_list


def main():
  scale = 128
  offset_min = -5
  offset_max = 15

  guide_point_list = []
  for x_offset in range(offset_min, offset_max):
    for y_offset in range(offset_min, offset_max):
      cell_point_list = get_cell_point_list(x_offset, y_offset, scale)
      guide_point_list.extend(cell_point_list)

  font = fontforge.activeFont()
  for glyph in font.selection.byGlyphs:
    layer = glyph.foreground

    for contour in layer:
      for point in contour:
        diff = [(guide_point, math.dist((point.x, point.y), guide_point)) for guide_point in guide_point_list]

        snap_point = min(diff, key=lambda t: t[1])[0]
        point.x = snap_point[0]
        point.y = snap_point[1]

      glyph.setLayer(layer, 'Fore')


if __name__ == "__main__":
  main()
