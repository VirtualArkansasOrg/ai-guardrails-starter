"""PreToolUse hook for Claude Code.

Runs before every tool call Claude makes in this repo. It blocks a call that
would write a known secret format into a file, read or change .env, skip
git hooks, force-push, or push straight to main.

Exit code 2 blocks the call, and the message printed to stderr goes back to
Claude so it can explain and try another way. Any other failure also blocks
(this hook fails closed), because a hook that crashes should not let the
call through.

These are simple pattern checks. They catch mistakes. Someone who wants to
get around them can (split a string, encode it, turn the hook off). That is
why gitleaks, push protection and review back this up.
"""
import json
import re
import sys

# Known secret formats. Add your own systems' token formats (LMS, SIS, help
# desk, internal tools) here and in .gitleaks.toml. The Canvas one is an example.
SECRET_PATTERNS = [
    (r"\b(AKIA|ASIA)[0-9A-Z]{16}\b", "an AWS access key"),
    (r"ACOTDEMO-[A-Z0-9]{24}", "the ACOT demo key (fake)"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "a private key"),
    (r"\bgh[pousr]_[A-Za-z0-9]{36}\b", "a GitHub token"),
    (r"\bgithub_pat_[A-Za-z0-9_]{22,}", "a GitHub token"),
    (r"\b\d{1,6}~[A-Za-z0-9]{64}\b", "a Canvas access token"),
    (r"\bsk-ant-[A-Za-z0-9_-]{20,}", "an Anthropic API key"),
    (r"\bsk-(proj-)?[A-Za-z0-9_-]{32,}", "an OpenAI API key"),
    (r"\bAIza[0-9A-Za-z_-]{35}\b", "a Google API key"),
    (r"\bxox[baprs]-[A-Za-z0-9-]{10,}", "a Slack token"),
]

# Shell commands Claude may not run here. Each entry: (pattern, message).
GIT_PUSH = r"\bgit\b[^;&|\n]*\bpush\b[^;&|\n]*"
# Commit messages are free text, so they are removed before the checks below.
# Otherwise "git commit -m 'Ignore .env'" or "-m 'fix -n flag'" would be blocked.
COMMIT_MESSAGE = r"""(\s(-m|--message|--title|--body)(=|\s*))("[^"$`]*"|'[^']*')"""
# Only inside git commit and gh pr/issue commands, so "less -m '.env'" is still checked.
MESSAGE_COMMANDS = r"""\b(git\b[^;&|\n]*\bcommit|gh\s+(pr|issue))\b('[^']*'|"[^"$`]*"|[^;&|\n'"])*"""
# Claude Code writes messages as "$(cat <<'EOF' ... EOF)". With a quoted delimiter
# the text is never run or expanded, so it is removed too.
HEREDOC_MESSAGE = r"""\$\(\s*cat\s+<<-?\s*'(\w+)'\n(?:(?!\t*\1\n)[^\n]*\n)*?\t*\1\n\s*\)"""
# The PowerShell version: a single-quoted here-string, @' ... '@.
HERESTRING_MESSAGE = r"""@'\n.*?\n'@"""
BLOCKED_COMMANDS = [
    (r"--no-veri|\bgit\b[^;&|\n]*\bcommit\b[^;&|\n]*\s-[a-zA-Z]*n[a-zA-Z]*\b"
     r"|(?i:core\.hookspath)|\bSKIP=|\.git[/\\]hooks|pre-commit\s+uninstall|disableAllHooks",
     "Skipping git hooks is not allowed in this repo."),
    (GIT_PUSH + r"(--force|\s-[a-zA-Z]*f\b|\s\+\S|--mirror)",
     "Force-pushing is not allowed in this repo."),
    (GIT_PUSH + r"""(\s|:|refs/heads/)["']?(main|master)(?![\w./-])""",
     "Pushing to main is not allowed. Push a branch and open a pull request."),
    (r"(?<![\w.-])\.env(?!\.example\b)(\.[\w-]+)*(?![\w.-])",
     "Reading or changing .env is not allowed. Use .env.example for variable names, and ask the "
     "person to add the value themselves (.env on their computer, or the cloud environment's settings on the web)."),
]

SHELL_TOOLS = ("Bash", "PowerShell")


def block(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def strings(value):
    """Every string inside the tool input, however deeply nested."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


def find_secret(text):
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, text):
            return label
    return None


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}

    if tool in SHELL_TOOLS:
        command = tool_input.get("command", "")
        checked = re.sub(r"\\\n", " ", command)  # join "\" line continuations
        checked = re.sub(HEREDOC_MESSAGE, "''", checked)
        if tool == "PowerShell":
            checked = re.sub(HERESTRING_MESSAGE, "''", checked, flags=re.S)
        checked = re.sub(MESSAGE_COMMANDS,
                         lambda m: re.sub(COMMIT_MESSAGE, r"\1''", m.group(0)), checked)
        for pattern, message in BLOCKED_COMMANDS:
            if re.search(pattern, checked):
                block(message)
    else:
        path = str(tool_input.get("file_path", "") or tool_input.get("notebook_path", "")
                   or tool_input.get("path", ""))
        name = re.split(r"[/\\]", path)[-1]
        if re.fullmatch(r"\.env(\.[\w-]+)*", name) and name != ".env.example":
            block("Reading or changing .env is not allowed. Use .env.example for variable names.")

    label = find_secret("\n".join(strings(tool_input)))
    if label and tool.startswith("mcp__"):
        block("Blocked: this would send " + label + " to " + tool + ". Don't share keys this way.")
    if label:
        block(
            "Blocked: this would put " + label + " into the repo or a command. "
            "Read it from an environment variable. The person adds the value themselves: in .env "
            "on their own computer, or in the cloud environment's settings in Claude Code on the web."
        )
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as error:  # fail closed
        block("Guardrail hook error (" + str(error) + "). Blocking to be safe.")
