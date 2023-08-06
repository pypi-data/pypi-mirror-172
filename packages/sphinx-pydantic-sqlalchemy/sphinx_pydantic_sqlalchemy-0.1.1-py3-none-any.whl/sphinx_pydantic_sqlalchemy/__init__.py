"""Wrapper over sphinx-pydantic with pydantic_sqlalchemy"""
from contextlib import suppress
import json
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import importlib
from docutils.parsers.rst import Directive
from sqlalchemy.orm import declarative_base

WideFormat = __import__('sphinx-jsonschema').wide_format.WideFormat


class SphinxSQLA(Directive):
    """SQLA wrapper over sphin-pydantic.

    Transforms either declarative-base or direct Table objects to pydantic
    models, extracts the jsonschema from the pydantic model, then uses
    sphinx-jsonschema to render a nice RST table from it.
    """
    has_content = True
    optional_arguments = 1
    option_spec = {}

    def __init__(self, directive, arguments, *args, **kwargs):
        # Get content source.
        self.obj = self.from_import(arguments[0])
        super().__init__(directive, arguments, *args, **kwargs)

    def from_import(self, loc):
        """Import module."""
        pkg_items = loc.split('.')

        try:
            mod = importlib.import_module('.'.join(pkg_items[:-1]))
            obj = getattr(mod, pkg_items[-1])
        except ImportError as e:
            raise e

        return obj

    def run(self):
        """Run the directive.

        Try to convert the object to pydantic model, if it doesn't have attrs
        it will try to transform it to declarative.

        It asks-for-forgiveness in case it's a normal pydantic model
        """
        obj = self.obj
        with suppress(Exception):
            if not hasattr(obj, 'attrs'):
                Base = declarative_base()
                obj = type(
                    str(obj.name).capitalize(), (Base, ), {'__table__': obj})
            obj = sqlalchemy_to_pydantic(obj)

        with suppress(Exception):

            return WideFormat(self.state, self.lineno, '', self.options,
                              self.state.document.settings.env.app).run(
                                  json.loads(obj.schema_json(indent=2)), '')
        return []


def setup(app):
    """Setup directive."""
    app.add_directive("sqla-pydantic", SphinxSQLA)
    app.add_config_value('jsonschema_options', {}, 'env')
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
