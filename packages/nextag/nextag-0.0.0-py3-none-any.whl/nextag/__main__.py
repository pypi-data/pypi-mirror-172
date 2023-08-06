import os
import re

_REF_FMT = '%(*committerdate:raw)%(committerdate:raw) %(refname) %(*objectname) %(objectname)'
_GET_TAGS = f"git for-each-ref --format='{_REF_FMT}' refs/tags"
_BEFORE_LAST = 'tail -n 2 | head -n 1'
_LAST = 'tail -n 1'
_SORT = 'sort -n | awk \'{ print $3; }\''
_NAME = 'sed \'s/refs\\/tags\\///g\''
GET_TAGS = ' | '.join([_GET_TAGS, _SORT, _NAME])
LAST_REV_CMD = ' | '.join([_GET_TAGS, _SORT, _LAST, _NAME])
PREV_REV_CMD = ' | '.join([_GET_TAGS, _SORT, _BEFORE_LAST, _NAME])

def main():
    fetch_tags()
    if not is_minor_semver(): return # guard pylint: disable=multiple-statements
    if head_is_tagged(): return # guard pylint: disable=multiple-statements

    print('.'.join([
        branch_name(),
        str(max(
            (int(tag.split('.')[2]) + 1
            for tag in tags()
            if tag.startswith(branch_name())),
            default=0
        ))
    ]))

def is_minor_semver():
    return re.match(r'\d+\.\d+', branch_name())

def fetch_tags():
    rsh('git fetch --tags')

def tags():
    return rsh(GET_TAGS).strip().split('\n')

def head_is_tagged():
    return bool(rsh("git tag --list '*.*.*' --points-at HEAD"))

def branch_name():
    return rsh('git branch --show-current').strip()

def rsh(cmd):
    return os.popen(cmd).read()


if __name__ == '__main__':
    main()
