"""For backward compatibility, expose main functions from
``setuptools.config.setupcfg``
"""
<<<<<<< HEAD
import warnings
from functools import wraps
from textwrap import dedent
from typing import Callable, TypeVar, cast

from .._deprecation_warning import SetuptoolsDeprecationWarning
=======
from functools import wraps
from typing import Callable, TypeVar, cast

from ..warnings import SetuptoolsDeprecationWarning
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
from . import setupcfg

Fn = TypeVar("Fn", bound=Callable)

__all__ = ('parse_configuration', 'read_configuration')


def _deprecation_notice(fn: Fn) -> Fn:
    @wraps(fn)
    def _wrapper(*args, **kwargs):
<<<<<<< HEAD
        msg = f"""\
        As setuptools moves its configuration towards `pyproject.toml`,
        `{__name__}.{fn.__name__}` became deprecated.

        For the time being, you can use the `{setupcfg.__name__}` module
        to access a backward compatible API, but this module is provisional
        and might be removed in the future.
        """
        warnings.warn(dedent(msg), SetuptoolsDeprecationWarning, stacklevel=2)
=======
        SetuptoolsDeprecationWarning.emit(
            "Deprecated API usage.",
            f"""
            As setuptools moves its configuration towards `pyproject.toml`,
            `{__name__}.{fn.__name__}` became deprecated.

            For the time being, you can use the `{setupcfg.__name__}` module
            to access a backward compatible API, but this module is provisional
            and might be removed in the future.

            To read project metadata, consider using
            ``build.util.project_wheel_metadata`` (https://pypi.org/project/build/).
            For simple scenarios, you can also try parsing the file directly
            with the help of ``configparser``.
            """,
            # due_date not defined yet, because the community still heavily relies on it
            # Warning introduced in 24 Mar 2022
        )
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
        return fn(*args, **kwargs)

    return cast(Fn, _wrapper)


read_configuration = _deprecation_notice(setupcfg.read_configuration)
parse_configuration = _deprecation_notice(setupcfg.parse_configuration)
