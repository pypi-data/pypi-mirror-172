# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dtyper']
install_requires = \
['typer']

setup_kwargs = {
    'name': 'dtyper',
    'version': '1.2.1',
    'description': '⌨️dtyper: Call typer commands or make dataclasses from them ⌨',
    'long_description': "# ⌨️dtyper: Call `typer` commands, or make a `dataclass` from them  ⌨️\n\n`typer` is a famously easy and useful system for writing Python CLIs but it has\ntwo issues.\n\nYou cannot quite call the functions it creates directly.\n\nAnd as you add more and more functionality into your CLI, there is no obvious\nway to break up the code sitting in one file.\n\n -----------------------------------------------\n\n`dtyper` is a drop-in replacement for `typer`, so you can write:\n\n    import dtyper as typer\n\nIt adds just two members, and overrides a third:\n\n* `dtyper.dataclass` is a decorator that takes an existing `typer` command\n  and makes a dataclass from it.\n\n* `dtyper.function` is a decorator that takes a new `typer` command and returns\n  a callable function with the correct defaults.\n\n* `dtyper.Typer`is identical to typer.Typer, except that the `command()`\n   decorator method wraps its functions with `dtyper.function`\n   above so they can be called from regular Python code.  You can think of it as\n   as a fix to a bug in `typer.Typer.command`, if you like. :-)\n\n`dtyper.function` filled a need several people had mentioned online, but I\nthink developing with `dtyper.dataclass` is the way to go, particularly if you\nexpect the code to grow medium-sized or beyond.\n\n## Installation\n\n    pip install dtyper\n\n## Examples\n\n### `dtyper.dataclass`: simple\n\n    @command(help='test')\n    def get_keys(\n        bucket: str = Argument(\n            ..., help='The bucket to use'\n        ),\n\n        keys: str = Argument(\n            'keys', help='The keys to download'\n        ),\n\n        pid: Optional[int] = Option(\n            None, help='pid'\n        ),\n    ):\n        return GetKeys(**locals())()\n\n    @dtyper.dataclass(get_keys)\n    class GetKeys:\n        site = 'https://www.some-websijt.nl'\n\n        def __post_init(self):\n            self.pid = self.pid or os.getpid()\n\n        def __call__(self):\n            return self.url, self.keys, self.pid\n\n        def url(self):\n           return f'{self.site}/{self.url}/{self.pid}'\n\n\n### `dtyper.dataclass`: A pattern for larger CLIs\n\n    # In interface.py\n\n    @command(help='test')\n    def compute_everything(\n        bucket: str = Argument(\n            ..., help='The bucket to use'\n        ),\n        # dozens of parameters here\n    ):\n        d = dict(locals())\n\n        from .compute import ComputeEverything\n\n        return ComputeEverything(**d)()\n\n    # In compute.py\n\n    from .interface import compute_everything\n\n    @dtyper.dataclass(compute_everything)\n    class ComputeEverything:\n        def __call__(self):\n           if self.huge_thing() and self.etc():\n              self.more_stuff()\n\n           # Dozens of methods here\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rec/dtyper',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
