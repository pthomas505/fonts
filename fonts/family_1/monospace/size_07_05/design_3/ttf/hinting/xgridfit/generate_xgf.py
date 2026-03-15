from jinja2 import Environment, FileSystemLoader


env = Environment(
  loader = FileSystemLoader('.'),
  trim_blocks = True,
  lstrip_blocks = True,
)


print(env.get_template('hinting.template').render())

# python3 generate_xgf.py > hinting.xgf
# xgridfit -i ../../Untitled.ttf -o ../../Untitled-hinted.ttf hinting.xgf
# ftgrid -d 1280x1024 16 ../../Untitled-hinted.ttf
