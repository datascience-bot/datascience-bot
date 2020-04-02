"""Based on work by surlyengineer/rules_aws_lambda
"""

def _lambda_python_pkg_impl(ctx):
    inputs = ctx.attr.src.default_runfiles.files.to_list()
    paths = []
    for i in inputs:
        paths.append(i.dirname)
        if "dist-info" in i.dirname:
            # we're at a python package, so add the prior
            paths.append("/".join(i.dirname.split("/")[0:-1]))
    paths = ",".join(paths)

    args = ctx.actions.args()
    args.add("--output_file", ctx.outputs.out.path)
    f = ctx.attr.main.files.to_list()[0]
    args.add("--entrypoint", f)
    strip_prefix = f.dirname
    args.add("--path_vars", paths)
    args.add("--strip_prefix", strip_prefix)
    args.add_all(inputs)
    ctx.actions.run(
        inputs = inputs,
        progress_message = "Building lambda executable %s" % ctx.label,
        arguments = [args],
        executable = ctx.executable.zipper,
        outputs = [ctx.outputs.out],
        mnemonic = "LambdaPackagePython",
    )
    return []

# This API is a little clumsy; we should have a default output
lambda_python_pkg = rule(
    implementation = _lambda_python_pkg_impl,
    attrs = {
        "src": attr.label(mandatory = True),
        "out": attr.output(),
        "main": attr.label(mandatory = True, allow_files = True),
        "zipper": attr.label(
            default = Label("//libs/shared/zipper:bin"),
            cfg = "host",
            executable = True,
            allow_files = True,
        ),
    },
)
