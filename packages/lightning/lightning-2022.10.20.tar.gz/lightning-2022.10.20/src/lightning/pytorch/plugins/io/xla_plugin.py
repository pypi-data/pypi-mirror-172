try:

    from pytorch_lightning.plugins.io.xla_plugin import XLACheckpointIO  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.7.7`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
