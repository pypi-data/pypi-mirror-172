import libcst as cst


def map_fstring_variable_to_string_replacement(
    fstring_var: cst.FormattedStringExpression,
) -> str:

    base = ""
    if fstring_var.equal and isinstance(fstring_var.equal, cst.AssignEqual):
        if isinstance(fstring_var.expression, cst.Call):
            base = cst.Module([]).code_for_node(fstring_var.expression)
        else:
            base = fstring_var.expression.value

        base += "="

    format_spec = ""
    if fstring_var.format_spec:
        if len(fstring_var.format_spec) != 1:
            raise Exception("Unable to handle format_spec: {fstring_var.format_spec}")
        if not isinstance(fstring_var.format_spec[0], cst.FormattedStringText):
            raise Exception("Unable to handle format_spec: {fstring_var.format_spec}")

        format_spec = fstring_var.format_spec[0].value

    if fstring_var.conversion:
        return base + f"%{format_spec}{fstring_var.conversion}"

    if fstring_var.equal:
        return base + f"%{format_spec}r"

    if len(format_spec) > 0 and format_spec[-1] in {"d", "f", "s", "r"}:
        return base + f"%{format_spec}"

    return base + f"%{format_spec}s"


def extract_fstring_variable(fstring_var: cst.FormattedStringExpression) -> cst.Arg:
    return cst.Arg(value=fstring_var.expression)


def fstring_to_lazylog(arg: cst.FormattedString) -> list[cst.Arg]:
    string_arg = '"'
    variable_args = []

    for part in arg.parts:
        if isinstance(part, cst.FormattedStringText):
            string_arg += part.value
            continue

        assert isinstance(part, cst.FormattedStringExpression)

        string_arg += map_fstring_variable_to_string_replacement(part)
        variable_args.append(extract_fstring_variable(part))

    string_arg += '"'

    return [cst.Arg(value=cst.SimpleString(value=string_arg))] + variable_args
