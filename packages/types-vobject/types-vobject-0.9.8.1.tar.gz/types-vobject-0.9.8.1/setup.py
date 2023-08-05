from setuptools import setup

name = "types-vobject"
description = "Typing stubs for vobject"
long_description = '''
## Typing stubs for vobject

This is a PEP 561 type stub package for the `vobject` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `vobject`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/vobject. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `3e828bd307ad13cfa36573f861ad88373bef7963`.
'''.lstrip()

setup(name=name,
      version="0.9.8.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/vobject.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['vobject-stubs'],
      package_data={'vobject-stubs': ['__init__.pyi', 'base.pyi', 'behavior.pyi', 'change_tz.pyi', 'hcalendar.pyi', 'icalendar.pyi', 'ics_diff.pyi', 'vcard.pyi', 'win32tz.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
