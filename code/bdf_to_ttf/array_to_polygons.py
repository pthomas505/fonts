import argparse
import matplotlib.pyplot as plt
import numpy as np
import PIL
import shapely


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

# Translates the given x and y graph coordinates to row and column indices.
def xy_to_rc(array, x, y):
  r_max = array.shape[0] - 1
  r = r_max - y
  c = x
  return (r, c)

# Returns the largest x graph coordinate in the array.
def get_x_max(array):
  return array.shape[1] - 1

# Returns the largest y graph coordinate in the array.
def get_y_max(array):
  return array.shape[0] - 1

# Returns the value in the array at the given x and y graph coordinates.
def get_at_xy(array, x, y):
  r, c = xy_to_rc(array, x, y)
  return array[r][c]


def get_border_line_list(array, x, y):
  center_pixel = get_at_xy(array, x, y)

  x_max = get_x_max(array)
  y_max = get_y_max(array)

  # Locations outside of the array are treated as having a value of 0.

  if x == 0:
    # The center pixel is at the left side of the array. Hence the pixel to the left of it is outside of the array.
    left_pixel = 0
  else:
    left_pixel = get_at_xy(array, x - 1, y)

  if x == x_max:
    # The center pixel is at the right side of the array. Hence the pixel to the right of it is outside of the array.
    right_pixel = 0
  else:
    right_pixel = get_at_xy(array, x + 1, y)

  if y == 0:
    # The center pixel is at the bottom of the array. Hence the pixel at the bottom of it is outside of the array.
    bottom_pixel = 0
  else:
    bottom_pixel = get_at_xy(array, x, y - 1)

  if y == y_max:
    # The center pixel is at the top of the array. Hence the pixel at the top of it is outside of the array.
    top_pixel = 0
  else:
    top_pixel = get_at_xy(array, x, y + 1)


  line_list = []
  # Checks if the center pixel is a border pixel.
  if center_pixel == 1 and (left_pixel == 0 or top_pixel == 0 or right_pixel == 0 or bottom_pixel == 0):
    # The center pixel is a border pixel.

    # These are the directed lines to place at each edge of the center pixel that borders a zero valued pixel.
    left_line = shapely.LineString([[0, 0], [0, 1]])
    top_line = shapely.LineString([[0, 1], [1, 1]])
    right_line = shapely.LineString([[1, 1], [1, 0]])
    bottom_line = shapely.LineString([[1, 0], [0, 0]])

    if left_pixel == 0:
      line_list.append(left_line)
    if top_pixel == 0:
      line_list.append(top_line)
    if right_pixel == 0:
      line_list.append(right_line)
    if bottom_pixel == 0:
      line_list.append(bottom_line)

    # Puts the lines in the line list into a multi line list.
    multi_line_list = shapely.multilinestrings(line_list)

    # Translates the lines in the multi line list to the location of the center pixel.
    multi_line_list = shapely.affinity.translate(multi_line_list, xoff=x, yoff=y)

    # Joins together any lines that share a point.
    merged_line_list = shapely.line_merge(multi_line_list, directed=True)

    # Splits any multi line lists back into line lists.
    merged_line_list = shapely.get_parts(merged_line_list)

    return merged_line_list
  else:
    # The center pixel is not a border pixel.
    return []


def array_to_multi_polygon_list(array):
  border_line_list = []
  for r in range(0, array.shape[0]):
    for c in range(0, array.shape[1]):
      x, y = rc_to_xy(array, r, c)
      border_line_list.extend(get_border_line_list(array, x, y))

  # Joins the border lines returned for all of the pixels into polygons that trace each group of four connected pixels.
  if len(border_line_list) > 0:
    multi_line_list = shapely.multilinestrings(border_line_list)
    merged_line_list = shapely.line_merge(multi_line_list, directed=True)
    merged_line_list = shapely.get_parts(merged_line_list)
    polygon_list = []
    for merged_line in merged_line_list:
      polygon = shapely.Polygon(merged_line)
      polygon = shapely.simplify(polygon, tolerance=0, preserve_topology=True)
      polygon_list.append(polygon)

    return shapely.MultiPolygon(polygon_list)
  else:
    return shapely.MultiPolygon([])


def plot_multi_polygon_list(multi_polygon_list):
  for polygon in shapely.get_parts(multi_polygon_list):
    plt.plot(*polygon.exterior.xy)
  plt.show()


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('image_file_path', type=str)
  args = parser.parse_args()

  image = PIL.Image.open(args.image_file_path)
  image = image.convert('1')

  array = np.logical_not(np.asarray(image))

  multi_polygon_list = array_to_multi_polygon_list(array)

  plot_multi_polygon_list(multi_polygon_list)


#main()
