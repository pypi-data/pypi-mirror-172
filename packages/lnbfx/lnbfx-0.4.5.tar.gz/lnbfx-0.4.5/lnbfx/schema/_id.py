from lnschema_core.id import base62, pipeline, pipeline_run


def bfx_pipeline() -> str:
    """Data object: 9 base62."""
    return pipeline()


def bfx_run() -> str:
    """Data object: 20 base62."""
    return pipeline_run()


def bfxmeta() -> str:
    """Data object: 21 base62."""
    return base62(n_char=21)
