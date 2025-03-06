def eval_shell_cmd(
        command: str,
        debug: bool = False,
        assert_retcode: bool = True) -> str:
    """Eval shell command with pipes and return result

    Keyword arguments:
    command          -- shell command string
    debug            -- issue debug prints if True, otherwise no debug prints (default False)
    assert_retcode   -- typically, if a shell command is failing (non-0 return code), we want the
                        to assert and stop the flow (hence, default value True). in some special
                        cases, we expect a "bad" error code but still want to keep going with the
                        flow, so we set @assert_retcode to False

    Return:
    the stdout of the shell command executed

    Side effects:
    The functions may exit on shell command error
    """
    if debug:
        print(f'Full command: -{command}-')

    p = subprocess.run(command, capture_output=True, shell=True)
    if assert_retcode:
        pph_assert(
            p.returncode == 0,
            f'error running -{command}-, STDERR: {p.stderr.decode()}')

    return p.stdout.decode('utf-8')
    
# usgae    
command = f'git diff-tree --no-commit-id --name-only -r {git_sha}'
commit_files = eval_shell_cmd(command, False) 