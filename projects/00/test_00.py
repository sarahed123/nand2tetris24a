# usage: python test_00.py
#        python -m pytest -xv test_00.py
#        python -m pytest -xv test_00.py::unit_test_func
#        python -m pytest -qrfsp test_00.py
import os
import sys
import subprocess
import pytest

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def test_mark_github_settings():
    '''Testing activating actions and removal of class access on github, see submission instructions.'''
    main_readme_file = '../../README.md'
    with open(main_readme_file, 'r') as f:
        readme_content = f.read()
        required_text1 = '[x] Creation changes'
        required_text2 = '[x] Settings -> Access'
        assert required_text1 in readme_content and required_text2 in readme_content, \
            'You need to mark with [x] setting your github repository according to submission instructions.'


def test_first_use_of_course_tool():
    '''Testing first use of course tools, you need to complete Xor.hdl, see chapter 1, slides #56-65.'''

    TOOLS_DIR = '../../tools'
    # some test runners (like the VScode testing test) need full path to find the tools, you can try instead:
    # TOOLS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'tools')
    extention = 'bat' if os.name == 'nt' else 'sh'
    HWSimulator = os.path.join(os.path.abspath(TOOLS_DIR), f'HardwareSimulator.{extention}')

    success_msg = b"End of script - Comparison ended successfully" + os.linesep.encode('ascii')
    assert subprocess.check_output([HWSimulator, "Xor.tst"]) == success_msg, 'Hardware simulator failure'


def test_taking_github_introduction_course():
    '''Testing taking github course by having a pull request url.'''

    ex0_pr_filename = "github-pr-url.txt"
    with open(ex0_pr_filename, 'r') as f:
        content = f.read()
        assert "/pull/1" in content, 'wrong url for github introduction pull request'


def test_taking_git_it_course():
    '''Testing git-it snapshot.'''

    ex0_gitit_snapshot_filename = "git-it-snapshot.png"
    assert os.path.exists(ex0_gitit_snapshot_filename), 'missing snapshot of git-it excercise'


def test_having_at_leaset_3_commits_by_now():
    os.system("git log --oneline > git.log")
    num_commits = sum(1 for line in open('git.log'))
    assert num_commits >= 3, 'By now you need to have at least 3 commits!'


if __name__ == "__main__":
    result = pytest.main(['-x', '-v', __file__])  # -x to stop on first failure, -v verbose output
    sys.exit(result)
