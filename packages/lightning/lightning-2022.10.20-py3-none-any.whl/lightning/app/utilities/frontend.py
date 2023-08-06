try:
    from lightning_app.utilities.frontend import AppInfo  # noqa: F401
    from lightning_app.utilities.frontend import update_index_file  # noqa: F401
    from lightning_app.utilities.frontend import _get_updated_content  # noqa: F401

except ImportError as err:

    from os import linesep
    from lightning_app import __version__
    msg = f'Your `lightning` package was built for `lightning_app==0.7.0`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
