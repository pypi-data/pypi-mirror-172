"""Schema.

.. autosummary::
   :toctree: .

   bfx_pipeline
   bfx_run
   bfxmeta
   dobject_bfxmeta

Versions & migrations:

.. autosummary::
   :toctree: .

   version_tsds
   migration_tsds

"""
from .. import __version__ as _version

_schema_id = "tsds"
_migration = None
__version__ = _version

from . import id
from ._core import (  # noqa
    bfx_pipeline,
    bfx_run,
    bfxmeta,
    dobject_bfxmeta,
    migration_tsds,
    version_tsds,
)
