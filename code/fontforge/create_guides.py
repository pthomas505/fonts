import fontforge
import math


# Creates a guide layer from a generated list of line segments.


def get_cell_contour_list(x_offset, y_offset, scale):
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

  point_A = point_list[0]
  point_B = point_list[1]
  point_C = point_list[2]
  point_D = point_list[3]
  point_E = point_list[4]
  point_F = point_list[5]
  point_G = point_list[6]
  point_H = point_list[7]
  point_I = point_list[8]
  point_J = point_list[9]
  point_K = point_list[10]
  point_L = point_list[11]
  point_M = point_list[12]
  point_N = point_list[13]
  point_O = point_list[14]
  point_P = point_list[15]

  segment_1 = (point_A, point_F)
  segment_2 = (point_F, point_H)
  segment_3 = (point_H, point_B)
  segment_4 = (point_B, point_I)
  segment_5 = (point_I, point_K)
  segment_6 = (point_K, point_C)
  segment_7 = (point_C, point_L)
  segment_8 = (point_L, point_N)
  segment_9 = (point_N, point_D)
  segment_10 = (point_D, point_O)
  segment_11 = (point_O, point_E)
  segment_12 = (point_E, point_A)
  segment_13 = (point_E, point_F)
  segment_14 = (point_F, point_G)
  segment_15 = (point_G, point_H)
  segment_16 = (point_H, point_I)
  segment_17 = (point_I, point_J)
  segment_18 = (point_J, point_K)
  segment_19 = (point_K, point_L)
  segment_20 = (point_L, point_M)
  segment_21 = (point_M, point_N)
  segment_22 = (point_N, point_O)
  segment_23 = (point_O, point_P)
  segment_24 = (point_P, point_E)
  segment_25 = (point_G, point_J)
  segment_26 = (point_J, point_M)
  segment_27 = (point_M, point_P)
  segment_28 = (point_P, point_G)

  segment_list = [segment_1, segment_2, segment_3, segment_4, segment_5, segment_6, segment_7, segment_8, segment_9, segment_10, segment_11, segment_12, segment_13, segment_14, segment_15, segment_16, segment_17, segment_18, segment_19, segment_20, segment_21, segment_22, segment_23, segment_24, segment_25, segment_26, segment_27, segment_28]

  contour_list = []

  for segment in segment_list:
    x1 = segment[0][0]
    y1 = segment[0][1]

    x2 = segment[1][0]
    y2 = segment[1][1]

    c = fontforge.contour()
    c.moveTo(x1, y1)
    c.lineTo(x2, y2)

    contour_list.append(c)

  return contour_list


def main():
  font = fontforge.activeFont()
  guide = fontforge.layer()

  scale = 128
  offset_min = -5
  offset_max = 15

  for x_offset in range(offset_min, offset_max):
    for y_offset in range(offset_min, offset_max):
      contour_list = get_cell_contour_list(x_offset, y_offset, scale)
      for contour in contour_list:
        guide += contour

  font.guide = guide


if __name__ == "__main__":
  main()
