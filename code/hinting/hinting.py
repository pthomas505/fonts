import argparse
import fontforge


header = '''<?xml version="1.0" encoding="UTF-8"?>
<xgridfit xmlns="http://xgridfit.sourceforge.net/Xgridfit2">
  <control-value name="font-units-per-square-cv" value="{int_scale}" />

  <constant name="font-units-per-square" value="{float_scale}" />
  <constant name="font-units-per-em" value="{units_per_em}" />

  <variable name="design-x-coord" value="0" />
  <variable name="design-y-coord" value="0" />

  <variable name="squares-per-em" value="0" />
  <variable name="pixels-per-square" value="0" />
  <variable name="scale" value="0" />

  <macro name="scale-point">
    <param name="point" />

    <set-equal target="design-x-coord"
      source="initial-x-coord(point) / control-value(font-units-per-square-cv)" />

    <set-equal target="design-y-coord"
      source="initial-y-coord(point) / control-value(font-units-per-square-cv)" />

    <with-vectors axis="x">
      <move pixel-distance="design-x-coord * scale">
        <point num="point" />
      </move>
    </with-vectors>

    <with-vectors axis="y">
      <move pixel-distance="design-y-coord * scale">
        <point num="point" />
      </move>
    </with-vectors>
  </macro>

  <pre-program>
    <!-- Set to a large enough value to ensure that the control values are used at all sizes. -->
    <set-control-value-cut-in value="2.0" />

    <!-- Turns off drop-out-control -->
    <set-dropout-control flags="0" threshold="0" />

    <set-dropout-type value="2" />


    <set-equal target="squares-per-em" source="font-units-per-em / font-units-per-square" />
    <set-equal target="pixels-per-square" source="pixels-per-em / squares-per-em" />
    <set-equal target="scale" source="floor(pixels-per-square)" />
  </pre-program>
'''

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('file', type=str, help='The path to a vector font that can be opened in FontForge.')

  parser.add_argument('--units_per_em', type=int, default=2048, help='The units per em of the font to be hinted.')
  parser.add_argument('--scale', type=int, default=128, help='The length of the sides of the vector squares in the font to be hinted.')

  args = parser.parse_args()

  font = fontforge.open(args.file)

  print(header.format(int_scale=args.scale, float_scale=float(args.scale), units_per_em=args.units_per_em))
  for glyph in font.glyphs():
    print('''  <glyph ps-name="{}">'''.format(glyph.glyphname))
    layer = glyph.foreground
    point_count = 0
    for contour in layer:
      for point in contour:
        point_count += 1
    for point_num in range(point_count + 4):
      print('''    <call-macro name="scale-point">
      <with-param name="point" value="{}" />
    </call-macro>'''.format(point_num))
    print('''  </glyph>
''')
  print('''</xgridfit>''')


main()
