import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"

files = ['static/', 'templates/', 'gamestate_integration_main.cfg', 'run.py', '__init__.py']

cspy_exe = Executable(script="main.py", base=base, targetName="CS-Py.exe")

setup(name="CS-Py",
      version="0.1",
      author="@Parkkeo1, CS @ UIUC",
      description="testing flask to exe",
      options={
          'build_exe': {
              'packages': ['jinja2.ext', 'jinja2', 'asyncio', 'numpy', 'pandas', 'sqlite3'],
              'include_files': files,
              'include_msvcr': True,
          }},
      executables=[cspy_exe], requires=['flask']
      )