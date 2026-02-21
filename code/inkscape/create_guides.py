import inkex

import math


def create_guide(position, orientation, parent):
  # Creates a sodipodi:guide node
  # (look into inkex's namespaces to find 'sodipodi' value in order to make a "sodipodi:guide" tag)
  inkex.etree.SubElement(parent, '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide', {'position':position, 'orientation':orientation})


class CreateGuidesExtension(inkex.EffectExtension):
  def add_arguments(self, pars):
    pars.add_argument("--scale", type=int)
    pars.add_argument("--x_min", type=int)
    pars.add_argument("--x_max", type=int)
    pars.add_argument("--y_min", type=int)
    pars.add_argument("--y_max", type=int)


  def effect(self):
    scale = self.options.scale

    x_min = self.options.x_min * scale
    x_max = self.options.x_max * scale
    y_min = self.options.y_min * scale
    y_max = self.options.y_max * scale

    sqrt2 = math.sqrt(2.0)


    # Removes any existing guides.

    nv = self.document.xpath('/svg:svg/sodipodi:namedview', namespaces = inkex.NSS)[0]

    # Gets all of the guides.
    children = self.document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide', namespaces = inkex.NSS)

    # Removes each guide.
    for element in children:
      nv.remove(element)


    # Adds the new guides.

    for x in range(x_min, x_max + 1, scale):
      # vertical guides spaced along the bottom X axis
      position = (x, y_min) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '1,0' # guide angle: 90 degrees
      create_guide(position_str, orientation_str, nv)

    for y in range(y_min, y_max + 1, scale):
      # horizontal guides spaced along the left Y axis
      position = (x_min, y) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '0,1' # guide angle: 0 degrees
      create_guide(position_str, orientation_str, nv)


    for x in range(x_min, x_max, scale):
      # 45 degree guides spaced along the bottom X axis
      position = (x + scale * (1.0 / sqrt2), y_min) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '-1,1' # guide angle: 45 degrees
      create_guide(position_str, orientation_str, nv)

      position = (x + scale * (1.0 - 1.0 / sqrt2), y_min) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '-1,1' # guide angle: 45 degrees
      create_guide(position_str, orientation_str, nv)


      # 135 degree guides spaced along the bottom X axis
      position = (x + scale * (1.0 / sqrt2), y_min) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '1,1' # guide angle: 135 degrees
      create_guide(position_str, orientation_str, nv)

      position = (x + scale * (1.0 - 1.0 / sqrt2), y_min) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '1,1' # guide angle: 135 degrees
      create_guide(position_str, orientation_str, nv)


    for y in range(y_min, y_max, scale):
      # 45 degree guides spaced along the left Y axis
      position = (x_min, y + scale * (1.0 / sqrt2)) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '-1,1' # guide angle: 45 degrees
      create_guide(position_str, orientation_str, nv)

      position = (x_min, y + scale * (1.0 - 1.0 / sqrt2)) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '-1,1' # guide angle: 45 degrees
      create_guide(position_str, orientation_str, nv)


      # 135 degree guides spaced along the right Y axis
      position = (x_max, y + scale * (1.0 / sqrt2)) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '1,1' # guide angle: 135 degrees
      create_guide(position_str, orientation_str, nv)

      position = (x_max, y + scale * (1.0 - 1.0 / sqrt2)) # guide origin
      position = (round(position[0]), round(position[1])) # round guide origin
      position_str = str(position[0]) + ',' + str(position[1])
      orientation_str = '1,1' # guide angle: 135 degrees
      create_guide(position_str, orientation_str, nv)


if __name__ == '__main__':
  CreateGuidesExtension().run()
