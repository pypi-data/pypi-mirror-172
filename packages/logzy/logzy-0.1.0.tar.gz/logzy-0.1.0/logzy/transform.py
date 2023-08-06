import logging
import sys
from contextlib import suppress

import astroid
from libcst import Call, metadata, CSTTransformer, FormattedString
from astroid.exceptions import InferenceError
from libcst._position import CodePosition

from .convert import fstring_to_lazylog

log = logging.getLogger()
log.setLevel(logging.WARNING)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


LOG_FUNCTIONS = {
    "critical",
    "debug",
    "error",
    "info",
    "log",
    "trace",
    "warning",
}

FOUND_LOG_CALLS: set[tuple[int, int]] = set()


def has_fstring_arg(call: astroid.Call) -> bool:
    if not call.func:
        log.debug("No func in call")
        return False

    if not isinstance(call.func, astroid.Attribute):
        log.debug("Func is not an attribute")
        return False

    if not call.args or len(call.args) != 1:
        log.debug("Invalid amount of args")
        return False

    if not isinstance(call.args[0], astroid.JoinedStr):
        log.debug("arg[0] is not a JoinedStr")
        return False

    return True


def clear_cache():
    global FOUND_LOG_CALLS
    FOUND_LOG_CALLS = set()


def get_cache() -> set:
    return FOUND_LOG_CALLS


def handle_call(call: astroid.Call) -> astroid.Call:
    # TODO move checks to filter function

    if not call.func:
        log.debug("func not set in call")
        return call

    if not has_fstring_arg(call):
        log.debug("No fstring in call")
        return call

    with suppress(InferenceError):
        for inf in call.func.infer():
            if isinstance(inf, astroid.BoundMethod):
                if is_instance_function(inf, "Logger", "logging", LOG_FUNCTIONS):
                    log.debug(
                        "Found logging.Logger.<function> call with fstring on (line=%s, col=%s)",
                        call.lineno,
                        call.col_offset,
                    )
                    if call.lineno is not None and call.col_offset is not None:
                        FOUND_LOG_CALLS.add((call.lineno, call.col_offset))
                    # return convert_to_lazy_args(call)
                    # TODO should be using a visitor, not a transformer
                    return call
            if isinstance(inf, astroid.FunctionDef):
                if is_module_function(inf, "logging", LOG_FUNCTIONS):
                    log.debug(
                        "Found logging.<function> call with fstring on (line=%s, col=%s)",
                        call.lineno,
                        call.col_offset,
                    )
                    if call.lineno is not None and call.col_offset is not None:
                        FOUND_LOG_CALLS.add((call.lineno, call.col_offset))
                    return call
    return call


def is_instance_function(func: astroid.BoundMethod, _class: str, module: str, names: set[str]) -> bool:
    """
    Check if this BoundMethod is a function, and does it belong to <module>.<class>
    """

    if func.name not in names:
        log.warning("Function name %s is not in list", func.name)
        return False

    if not isinstance(func.parent, astroid.ClassDef):
        log.debug("Function parent is not a class")
        return False

    if not is_class_named(func, _class):
        log.debug("Class name does not match")
        return False

    if not is_module_named(func.parent, module):
        log.debug("Module name does not match %s", module)
        return False

    return True


def is_module_function(func: astroid.FunctionDef, module: str, names: set[str]) -> bool:
    """
    Check if this BoundMethod is a top level module function, and does it belong to <module>
    """

    if func.name not in names:
        log.debug("Function name %s is not in list", func.name)
        return False

    if not isinstance(func.parent, astroid.Module):
        log.debug("Function parent is not a module")
        return False

    if not is_module_named(func, module):
        log.debug("Module name does not match %s", module)
        return False

    return True


def is_class_named(func: astroid.BoundMethod, name: str) -> bool:
    """
    Check if the function is part of a class, and does the class' name match
    """

    if not isinstance(func.parent, astroid.ClassDef):
        return False

    return func.parent.name == name


def is_module_named(_class: astroid.ClassDef | astroid.FunctionDef, name: str) -> bool:
    """
    Check if the class is part of a module, and does the module's name match
    """

    if not isinstance(_class.parent, astroid.Module):
        log.debug("Class parent is not a module")
        return False

    return _class.parent.name == name


class LazyLogTransformer(CSTTransformer):
    """
    Transforms f-strings in logging functions to lazy log statements
    """

    METADATA_DEPENDENCIES = (metadata.PositionProvider,)  # type: ignore

    def __init__(self):
        self.calls: dict[Call, CodePosition] = {}
        super().__init__()

    def visit_Call(self, node: Call):
        pos = self.get_metadata(metadata.PositionProvider, node).start  # type: ignore
        if (pos.line, pos.column) in FOUND_LOG_CALLS:
            self.calls[node] = pos
            log.debug("Storing node at %s, %s", pos.line, pos.column)

    def leave_Call(self, original_node: Call, updated_node: Call) -> Call:
        if original_node in self.calls:
            pos = self.calls[original_node]
            log.debug("Found node at line=%s, column=%s", pos.line, pos.column)
        else:
            return updated_node

        fstring = get_fstring(updated_node)
        lazy_log = fstring_to_lazylog(fstring)

        return updated_node.with_changes(args=lazy_log)


def get_fstring(call: Call) -> FormattedString:
    """
    Get the fstring from the function call

    This should have already been checked in the inference path, so we expect
    one argument that is a FormattedString
    """

    if len(call.args) != 1:
        raise Exception("Multiple args to function call")

    if not isinstance(call.args[0].value, FormattedString):
        raise Exception("Functions arg is not an f-string")

    return call.args[0].value
