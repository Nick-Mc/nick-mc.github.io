"""Translation layer between pyproject config and setuptools distribution and
metadata objects.

The distribution and metadata objects are modeled after (an old version of)
core metadata, therefore configs in the format specified for ``pyproject.toml``
need to be processed before being applied.

**PRIVATE MODULE**: API reserved for setuptools internal usage only.
"""
import logging
import os
<<<<<<< HEAD
import warnings
=======
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
from collections.abc import Mapping
from email.headerregistry import Address
from functools import partial, reduce
from itertools import chain
from types import MappingProxyType
<<<<<<< HEAD
from typing import (TYPE_CHECKING, Any, Callable, Dict, List, Optional, Set, Tuple,
                    Type, Union, cast)

from setuptools._deprecation_warning import SetuptoolsDeprecationWarning
=======
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

from ..warnings import SetuptoolsWarning, SetuptoolsDeprecationWarning
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)

if TYPE_CHECKING:
    from setuptools._importlib import metadata  # noqa
    from setuptools.dist import Distribution  # noqa

EMPTY: Mapping = MappingProxyType({})  # Immutable dict-like
_Path = Union[os.PathLike, str]
_DictOrStr = Union[dict, str]
_CorrespFn = Callable[["Distribution", Any, _Path], None]
_Correspondence = Union[str, _CorrespFn]

_logger = logging.getLogger(__name__)


def apply(dist: "Distribution", config: dict, filename: _Path) -> "Distribution":
    """Apply configuration dict read with :func:`read_configuration`"""

    if not config:
        return dist  # short-circuit unrelated pyproject.toml file

    root_dir = os.path.dirname(filename) or "."

    _apply_project_table(dist, config, root_dir)
    _apply_tool_table(dist, config, filename)

    current_directory = os.getcwd()
    os.chdir(root_dir)
    try:
        dist._finalize_requires()
        dist._finalize_license_files()
    finally:
        os.chdir(current_directory)

    return dist


def _apply_project_table(dist: "Distribution", config: dict, root_dir: _Path):
    project_table = config.get("project", {}).copy()
    if not project_table:
        return  # short-circuit

    _handle_missing_dynamic(dist, project_table)
    _unify_entry_points(project_table)

    for field, value in project_table.items():
        norm_key = json_compatible_key(field)
        corresp = PYPROJECT_CORRESPONDENCE.get(norm_key, norm_key)
        if callable(corresp):
            corresp(dist, value, root_dir)
        else:
            _set_config(dist, corresp, value)


def _apply_tool_table(dist: "Distribution", config: dict, filename: _Path):
    tool_table = config.get("tool", {}).get("setuptools", {})
    if not tool_table:
        return  # short-circuit

    for field, value in tool_table.items():
        norm_key = json_compatible_key(field)

        if norm_key in TOOL_TABLE_DEPRECATIONS:
<<<<<<< HEAD
            suggestion = TOOL_TABLE_DEPRECATIONS[norm_key]
            msg = f"The parameter `{norm_key}` is deprecated, {suggestion}"
            warnings.warn(msg, SetuptoolsDeprecationWarning)
=======
            suggestion, kwargs = TOOL_TABLE_DEPRECATIONS[norm_key]
            msg = f"The parameter `{norm_key}` is deprecated, {suggestion}"
            SetuptoolsDeprecationWarning.emit(
                "Deprecated config", msg, **kwargs  # type: ignore
            )
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)

        norm_key = TOOL_TABLE_RENAMES.get(norm_key, norm_key)
        _set_config(dist, norm_key, value)

    _copy_command_options(config, dist, filename)


def _handle_missing_dynamic(dist: "Distribution", project_table: dict):
    """Be temporarily forgiving with ``dynamic`` fields not listed in ``dynamic``"""
    # TODO: Set fields back to `None` once the feature stabilizes
    dynamic = set(project_table.get("dynamic", []))
    for field, getter in _PREVIOUSLY_DEFINED.items():
        if not (field in project_table or field in dynamic):
            value = getter(dist)
            if value:
<<<<<<< HEAD
                msg = _WouldIgnoreField.message(field, value)
                warnings.warn(msg, _WouldIgnoreField)
=======
                _WouldIgnoreField.emit(field=field, value=value)
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)


def json_compatible_key(key: str) -> str:
    """As defined in :pep:`566#json-compatible-metadata`"""
    return key.lower().replace("-", "_")


def _set_config(dist: "Distribution", field: str, value: Any):
    setter = getattr(dist.metadata, f"set_{field}", None)
    if setter:
        setter(value)
    elif hasattr(dist.metadata, field) or field in SETUPTOOLS_PATCHES:
        setattr(dist.metadata, field, value)
    else:
        setattr(dist, field, value)


_CONTENT_TYPES = {
    ".md": "text/markdown",
    ".rst": "text/x-rst",
    ".txt": "text/plain",
}


def _guess_content_type(file: str) -> Optional[str]:
    _, ext = os.path.splitext(file.lower())
    if not ext:
        return None

    if ext in _CONTENT_TYPES:
        return _CONTENT_TYPES[ext]

    valid = ", ".join(f"{k} ({v})" for k, v in _CONTENT_TYPES.items())
    msg = f"only the following file extensions are recognized: {valid}."
    raise ValueError(f"Undefined content type for {file}, {msg}")


def _long_description(dist: "Distribution", val: _DictOrStr, root_dir: _Path):
    from setuptools.config import expand

    if isinstance(val, str):
        file: Union[str, list] = val
        text = expand.read_files(file, root_dir)
        ctype = _guess_content_type(val)
    else:
        file = val.get("file") or []
        text = val.get("text") or expand.read_files(file, root_dir)
        ctype = val["content-type"]

    _set_config(dist, "long_description", text)

    if ctype:
        _set_config(dist, "long_description_content_type", ctype)

    if file:
        dist._referenced_files.add(cast(str, file))


def _license(dist: "Distribution", val: dict, root_dir: _Path):
    from setuptools.config import expand

    if "file" in val:
        _set_config(dist, "license", expand.read_files([val["file"]], root_dir))
        dist._referenced_files.add(val["file"])
    else:
        _set_config(dist, "license", val["text"])


def _people(dist: "Distribution", val: List[dict], _root_dir: _Path, kind: str):
    field = []
    email_field = []
    for person in val:
        if "name" not in person:
            email_field.append(person["email"])
        elif "email" not in person:
            field.append(person["name"])
        else:
            addr = Address(display_name=person["name"], addr_spec=person["email"])
            email_field.append(str(addr))

    if field:
        _set_config(dist, kind, ", ".join(field))
    if email_field:
        _set_config(dist, f"{kind}_email", ", ".join(email_field))


def _project_urls(dist: "Distribution", val: dict, _root_dir):
    _set_config(dist, "project_urls", val)


def _python_requires(dist: "Distribution", val: dict, _root_dir):
    from setuptools.extern.packaging.specifiers import SpecifierSet

    _set_config(dist, "python_requires", SpecifierSet(val))


def _dependencies(dist: "Distribution", val: list, _root_dir):
    if getattr(dist, "install_requires", []):
        msg = "`install_requires` overwritten in `pyproject.toml` (dependencies)"
<<<<<<< HEAD
        warnings.warn(msg)
=======
        SetuptoolsWarning.emit(msg)
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    _set_config(dist, "install_requires", val)


def _optional_dependencies(dist: "Distribution", val: dict, _root_dir):
    existing = getattr(dist, "extras_require", {})
    _set_config(dist, "extras_require", {**existing, **val})


def _unify_entry_points(project_table: dict):
    project = project_table
    entry_points = project.pop("entry-points", project.pop("entry_points", {}))
    renaming = {"scripts": "console_scripts", "gui_scripts": "gui_scripts"}
    for key, value in list(project.items()):  # eager to allow modifications
        norm_key = json_compatible_key(key)
        if norm_key in renaming and value:
            entry_points[renaming[norm_key]] = project.pop(key)

    if entry_points:
        project["entry-points"] = {
            name: [f"{k} = {v}" for k, v in group.items()]
            for name, group in entry_points.items()
        }


def _copy_command_options(pyproject: dict, dist: "Distribution", filename: _Path):
    tool_table = pyproject.get("tool", {})
    cmdclass = tool_table.get("setuptools", {}).get("cmdclass", {})
    valid_options = _valid_command_options(cmdclass)

    cmd_opts = dist.command_options
    for cmd, config in pyproject.get("tool", {}).get("distutils", {}).items():
        cmd = json_compatible_key(cmd)
        valid = valid_options.get(cmd, set())
        cmd_opts.setdefault(cmd, {})
        for key, value in config.items():
            key = json_compatible_key(key)
            cmd_opts[cmd][key] = (str(filename), value)
            if key not in valid:
                # To avoid removing options that are specified dynamically we
                # just log a warn...
                _logger.warning(f"Command option {cmd}.{key} is not defined")


def _valid_command_options(cmdclass: Mapping = EMPTY) -> Dict[str, Set[str]]:
    from .._importlib import metadata
    from setuptools.dist import Distribution

    valid_options = {"global": _normalise_cmd_options(Distribution.global_options)}

    unloaded_entry_points = metadata.entry_points(group='distutils.commands')
    loaded_entry_points = (_load_ep(ep) for ep in unloaded_entry_points)
    entry_points = (ep for ep in loaded_entry_points if ep)
    for cmd, cmd_class in chain(entry_points, cmdclass.items()):
        opts = valid_options.get(cmd, set())
        opts = opts | _normalise_cmd_options(getattr(cmd_class, "user_options", []))
        valid_options[cmd] = opts

    return valid_options


def _load_ep(ep: "metadata.EntryPoint") -> Optional[Tuple[str, Type]]:
    # Ignore all the errors
    try:
        return (ep.name, ep.load())
    except Exception as ex:
        msg = f"{ex.__class__.__name__} while trying to load entry-point {ep.name}"
        _logger.warning(f"{msg}: {ex}")
        return None


def _normalise_cmd_option_key(name: str) -> str:
    return json_compatible_key(name).strip("_=")


def _normalise_cmd_options(desc: List[Tuple[str, Optional[str], str]]) -> Set[str]:
    return {_normalise_cmd_option_key(fancy_option[0]) for fancy_option in desc}


<<<<<<< HEAD
=======
def _get_previous_entrypoints(dist: "Distribution") -> Dict[str, list]:
    ignore = ("console_scripts", "gui_scripts")
    value = getattr(dist, "entry_points", None) or {}
    return {k: v for k, v in value.items() if k not in ignore}


def _get_previous_scripts(dist: "Distribution") -> Optional[list]:
    value = getattr(dist, "entry_points", None) or {}
    return value.get("console_scripts")


def _get_previous_gui_scripts(dist: "Distribution") -> Optional[list]:
    value = getattr(dist, "entry_points", None) or {}
    return value.get("gui_scripts")


>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
def _attrgetter(attr):
    """
    Similar to ``operator.attrgetter`` but returns None if ``attr`` is not found
    >>> from types import SimpleNamespace
    >>> obj = SimpleNamespace(a=42, b=SimpleNamespace(c=13))
    >>> _attrgetter("a")(obj)
    42
    >>> _attrgetter("b.c")(obj)
    13
    >>> _attrgetter("d")(obj) is None
    True
    """
    return partial(reduce, lambda acc, x: getattr(acc, x, None), attr.split("."))


def _some_attrgetter(*items):
    """
    Return the first "truth-y" attribute or None
    >>> from types import SimpleNamespace
    >>> obj = SimpleNamespace(a=42, b=SimpleNamespace(c=13))
    >>> _some_attrgetter("d", "a", "b.c")(obj)
    42
    >>> _some_attrgetter("d", "e", "b.c", "a")(obj)
    13
    >>> _some_attrgetter("d", "e", "f")(obj) is None
    True
    """
<<<<<<< HEAD
    def _acessor(obj):
        values = (_attrgetter(i)(obj) for i in items)
        return next((i for i in values if i is not None), None)
=======

    def _acessor(obj):
        values = (_attrgetter(i)(obj) for i in items)
        return next((i for i in values if i is not None), None)

>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    return _acessor


PYPROJECT_CORRESPONDENCE: Dict[str, _Correspondence] = {
    "readme": _long_description,
    "license": _license,
    "authors": partial(_people, kind="author"),
    "maintainers": partial(_people, kind="maintainer"),
    "urls": _project_urls,
    "dependencies": _dependencies,
    "optional_dependencies": _optional_dependencies,
    "requires_python": _python_requires,
}

TOOL_TABLE_RENAMES = {"script_files": "scripts"}
TOOL_TABLE_DEPRECATIONS = {
<<<<<<< HEAD
    "namespace_packages": "consider using implicit namespaces instead (PEP 420)."
}

SETUPTOOLS_PATCHES = {"long_description_content_type", "project_urls",
                      "provides_extras", "license_file", "license_files"}
=======
    "namespace_packages": (
        "consider using implicit namespaces instead (PEP 420).",
        {"due_date": (2023, 10, 30)},  # warning introduced in May 2022
    )
}

SETUPTOOLS_PATCHES = {
    "long_description_content_type",
    "project_urls",
    "provides_extras",
    "license_file",
    "license_files",
}
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)

_PREVIOUSLY_DEFINED = {
    "name": _attrgetter("metadata.name"),
    "version": _attrgetter("metadata.version"),
    "description": _attrgetter("metadata.description"),
    "readme": _attrgetter("metadata.long_description"),
    "requires-python": _some_attrgetter("python_requires", "metadata.python_requires"),
    "license": _attrgetter("metadata.license"),
    "authors": _some_attrgetter("metadata.author", "metadata.author_email"),
    "maintainers": _some_attrgetter("metadata.maintainer", "metadata.maintainer_email"),
    "keywords": _attrgetter("metadata.keywords"),
    "classifiers": _attrgetter("metadata.classifiers"),
    "urls": _attrgetter("metadata.project_urls"),
<<<<<<< HEAD
    "entry-points": _attrgetter("entry_points"),
=======
    "entry-points": _get_previous_entrypoints,
    "scripts": _get_previous_scripts,
    "gui-scripts": _get_previous_gui_scripts,
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    "dependencies": _some_attrgetter("_orig_install_requires", "install_requires"),
    "optional-dependencies": _some_attrgetter("_orig_extras_require", "extras_require"),
}


<<<<<<< HEAD
class _WouldIgnoreField(UserWarning):
    """Inform users that ``pyproject.toml`` would overwrite previous metadata."""

    MESSAGE = """\
    {field!r} defined outside of `pyproject.toml` would be ignored.
    !!\n\n
=======
class _WouldIgnoreField(SetuptoolsDeprecationWarning):
    _SUMMARY = "`{field}` defined outside of `pyproject.toml` would be ignored."

    _DETAILS = """
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    ##########################################################################
    # configuration would be ignored/result in error due to `pyproject.toml` #
    ##########################################################################

    The following seems to be defined outside of `pyproject.toml`:

    `{field} = {value!r}`

    According to the spec (see the link below), however, setuptools CANNOT
<<<<<<< HEAD
    consider this value unless {field!r} is listed as `dynamic`.
=======
    consider this value unless `{field}` is listed as `dynamic`.
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)

    https://packaging.python.org/en/latest/specifications/declaring-project-metadata/

    For the time being, `setuptools` will still consider the given value (as a
    **transitional** measure), but please note that future releases of setuptools will
    follow strictly the standard.

<<<<<<< HEAD
    To prevent this warning, you can list {field!r} under `dynamic` or alternatively
    remove the `[project]` table from your file and rely entirely on other means of
    configuration.
    \n\n!!
    """

    @classmethod
    def message(cls, field, value):
        from inspect import cleandoc
        return cleandoc(cls.MESSAGE.format(field=field, value=value))
=======
    To prevent this warning, you can list `{field}` under `dynamic` or alternatively
    remove the `[project]` table from your file and rely entirely on other means of
    configuration.
    """
    _DUE_DATE = (2023, 10, 30)  # Initially introduced in 27 May 2022
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
