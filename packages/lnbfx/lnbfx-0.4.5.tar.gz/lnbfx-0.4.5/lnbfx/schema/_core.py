from datetime import datetime
from typing import Optional

from lnschema_core._timestamps import CreatedAt

# import lnschema_core  # noqa
from sqlmodel import Field, ForeignKeyConstraint, SQLModel

from . import id as idg


class bfx_pipeline(SQLModel, table=True):  # type: ignore
    """Bioinformatics pipeline metadata."""

    __table_args__ = (
        ForeignKeyConstraint(
            ["id", "v"],
            ["pipeline.id", "pipeline.v"],
            name="bfx_pipeline_pipeline",
        ),
    )
    id: str = Field(primary_key=True, index=True)
    v: str = Field(primary_key=True, index=True)


class bfx_run(SQLModel, table=True):  # type: ignore
    """Bioinformatics pipeline run metadata."""

    __table_args__ = (
        ForeignKeyConstraint(
            ["bfx_pipeline_id", "bfx_pipeline_v"],
            ["bfx_pipeline.id", "bfx_pipeline.v"],
            name="bfx_run_bfx_pipeline",
        ),
    )
    id: str = Field(primary_key=True, foreign_key="pipeline_run.id", index=True)
    dir: Optional[str] = None
    bfx_pipeline_id: str = Field(index=True)
    bfx_pipeline_v: str = Field(index=True)


class bfxmeta(SQLModel, table=True):  # type: ignore
    """Metadata for files associated with bioinformatics pipelines."""

    id: Optional[str] = Field(default_factory=idg.bfxmeta, primary_key=True)
    file_type: Optional[str] = None
    dir: Optional[str] = None


class dobject_bfxmeta(SQLModel, table=True):  # type: ignore
    """Link table between dobject and bfxmeta tables."""

    dobject_id: str = Field(primary_key=True, foreign_key="dobject.id")
    bfxmeta_id: str = Field(primary_key=True, foreign_key="bfxmeta.id")


class version_tsds(SQLModel, table=True):  # type: ignore
    """Schema module versions deployed in a given instance.

    Migrations of the schema module add rows to this table, storing the schema
    module version to which we migrated along with the user who performed the
    migration.
    """

    v: Optional[str] = Field(primary_key=True)
    """Python package version of `lnschema_core`."""
    migration: Optional[str] = None
    """Migration script reference of the latest migration leading up to the Python package version."""  # noqa
    user_id: str = Field(foreign_key="user.id")
    """Link to user."""
    created_at: datetime = CreatedAt
    """Time of creation."""


class migration_tsds(SQLModel, table=True):  # type: ignore
    """Latest migration.

    This stores the reference to the latest migration script deployed.
    """

    version_num: Optional[str] = Field(primary_key=True)
    """Reference to the last-run migration script."""
