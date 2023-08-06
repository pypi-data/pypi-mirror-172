"""
A Plugin to split tests into equally sized groups
"""
import pytest
import os

def getenv_integer(name: str, default: int) -> int:
    value = os.getenv(name, None)
    if value is not None:
        if str(value).isdigit():
            return int(str(value))
    return default


class PytestDivConfig:
    enabled: bool = False
    enabled_by_env: bool = False
    divide_files: bool = False
    divide_index: int = 1
    divide_total: int = 1

    def __init__(self):
        _index = getenv_integer("CI_NODE_INDEX", 0)
        _total = getenv_integer("CI_NODE_TOTAL", 0)
        if _total > 0:
            if _index > 0:
                self.enabled_by_env = True
                self.divide_total = _total
                self.divide_index = _index
                self.divide_files = True
                self.enabled = True


_pytestdiv_config = PytestDivConfig()


def pytest_addoption(parser, pluginmanager):
    group = parser.getgroup("collect")
    group.addoption("--divide", type=str, metavar="M/N",
                    default=None,
                    help="Split tests into groups of N tests and execute the Mth group")
    group.addoption("--divide-files",
                    action="store_true",
                    default=False,
                    help="Split groups by file instead of by test")


def pytest_report_header(config):
    if _pytestdiv_config.enabled:
        mode = "cases"
        if _pytestdiv_config.divide_files:
            mode = "files"
        return f"pytestdiv: {_pytestdiv_config.divide_index} of {_pytestdiv_config.divide_total}, mode = {mode}"
    else:
        return "pytestdiv: disabled"


def pytest_configure(config):
    if not _pytestdiv_config.enabled:
        if config.option.divide is not None:
            m, n = config.option.divide.split("/", 1)
            m = int(m)
            n = int(n)
            assert n > 0, f"N must be positive"
            assert m > 0, f"M must be positive"
            assert m <= n, f"M must be <= than M for --divide M/N"
            _pytestdiv_config.enabled = True
            _pytestdiv_config.divide_index = m
            _pytestdiv_config.divide_total = n
            if config.option.divide_files:
                _pytestdiv_config.divide_files = True


def pytest_collection_modifyitems(session: pytest.Session, config, items):
    if _pytestdiv_config.enabled:
        new_items = []
        m = _pytestdiv_config.divide_index
        n = _pytestdiv_config.divide_total
        if config.option.divide_files:
            # share out test files
            files = {}
            for item in items:
                filename = str(item.fspath)
                if filename not in files:
                    files[filename] = []
                files[filename].append(item)
            filenames = sorted(files.keys())
            for i in range(len(filenames)):
                if (i % n) == (m - 1):
                    filename = filenames[i]
                    new_items.extend(files[filename])
        else:
            # share out test functions
            for i in range(len(items)):
                if (i % n) == (m - 1):
                    new_items.append(items[i])
        items.clear()
        items.extend(new_items)





