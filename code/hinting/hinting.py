import argparse
import fontforge


header = '''<?xml version="1.0" encoding="UTF-8"?>
<xgridfit xmlns="http://xgridfit.sourceforge.net/Xgridfit2">
  <control-value name="font-units-per-square-cv" value="128" />

  <constant name="font-units-per-square" value="128.0" />
  <constant name="font-units-per-em" value="2048" />

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
  args = parser.parse_args()

  font = fontforge.open(args.file)

  print(header)
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
