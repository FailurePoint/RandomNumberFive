pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'random_number_five')
gnome = import('gnome')

gnome.compile_resources('random-number-five',
  'random-number-five.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'random-number-five.in',
  output: 'random-number-five',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

random_number_five_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'metadata.py',
]

install_data(random_number_five_sources, install_dir: moduledir)
