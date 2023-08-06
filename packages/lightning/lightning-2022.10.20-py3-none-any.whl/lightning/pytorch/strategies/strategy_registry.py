try:

    from pytorch_lightning.strategies.strategy_registry import _StrategyRegistry  # noqa: F401
    from pytorch_lightning.strategies.strategy_registry import StrategyRegistry  # noqa: F401
    from pytorch_lightning.strategies.strategy_registry import call_register_strategies  # noqa: F401

except ImportError as err:

    from os import linesep
    from pytorch_lightning import __version__
    msg = f'Your `lightning` package was built for `pytorch_lightning==1.7.7`, but you are running {__version__}'
    raise type(err)(str(err) + linesep + msg)
