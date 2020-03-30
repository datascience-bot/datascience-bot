"""Copied with permission from surlyengineer/rules_aws_lambda
"""

def _lambda_python_pkg_impl(ctx):
    inputs = ctx.attr.src.default_runfiles.files.to_list()
    extras = []
    paths = []
    for i in inputs:
        paths.append(i.dirname)
        if "dist-info" in i.dirname:
            # we're at a python package, so add the prior
            paths.append("/".join(i.dirname.split("/")[0:-1]))
    dirs = ",".join(extras)
    paths = ",".join(paths)
    args = ctx.actions.args()
    args.add("-o", ctx.outputs.out.path)
    f = ctx.attr.main.files.to_list()[0]
    args.add("-e", f)
    strip_prefix = f.dirname
    args.add("-D", dirs)
    args.add("-P", paths)
    args.add("-s", strip_prefix)
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
        "deps": attr.label_list(),
        "src": attr.label(mandatory = True),
        "out": attr.output(),
        "main": attr.label(mandatory = True, allow_files = True),
        "zipper": attr.label(
            default = Label("//tools/zipper:bin"),
            cfg = "host",
            executable = True,
            allow_files = True,
        ),
    },
)
