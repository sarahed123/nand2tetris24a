# The Elements of Computing Systems (Nand to Tetris)
A **private** repository for course work and submissions - Azrieli/JCE version.
See also the course syllabus, submission instructions, and [wiki](https://github.com/jce-il/nand2tetris-jce/wiki).

### Developers Details
Please keep exact template of rows below, including the comma separating the items.
- Names: Sarah Edery, 
- ID#s: 325031029, 
- Github usernames: sarahed123,

### Tools Setup
- [x] Install course tools (see list and links in the course instructions document), and have a github user name with course team aceess
- [x] `Fork` (actually `Create`) the [course repository](https://github.com/jce-il/nand2tetris24a) to your account
  - [x] Creation changes: make sure to keep the original repository name and also to make it private
- [x] Apply other repository settings:
  - [x] Settings -> Access: Collaborators and Teams -> Manage Access -> add your collaborator
- [x] `Clone` the repository to your machine, and:
  - Open the repository folder with your IDE (in VSCode, allow installing the suggested course extentions, and examine the suggested `./vscode/settings.json`)
  - Install needed python packages, e.g., run in the repository folder: `python -m pip install -r requirements.txt`

 ### Project 00 - Get to know the basic course tools and submission system
  - Here you hava a checklist of the various project tasks. See more details in the course instructions (also explained at [Project 00 folder](./projects/00/), in the html file that contains instructions, opened locally at your browser)
  - As you progress with these tasks, mark completion by adding `x` to the starting `[ ]`, like this `[x]`
  - Start running the project tests, by the Testing Activity Bar of VSCode, or the Run Activity/Menu (`Ctrl+F5`)->"Run Auto Tester" (while a file from the 00 project is in focus) or with the (internal) terminal: `python ./projects/00/test_00.py`
  - [x] The first test, ensures that you marked applying the above necessary repository settings after forking
  - [x] 1. Run the first course tool (HardwareSimulator on the Xor chip), and make its test pass
  - [x] 2. Complete the [github introduction](https://github.com/skills/introduction-to-github) course, and update your course pull request url in the included .txt file
  - [x] 3. Complete the [git-it](https://github.com/jlord/git-it-electron/releases) course, and add the screen capture to the project folder
  - [x] 4. Create a new branch named: 00, and commit your work for every valuable step
    - Test that by now your local git history continas at leaset 3 commits (`git log`).
- [x] Make sure you also updated the [Developer details](#developer-details) section above (and commit this change too!)

- [ ] Push your work to your remote github repository (`git push -u origin 00`), and watch the auto tester action results
- [ ] Submit your work by openning a pull request to *your* `main` branch, update there, the submission details (ids, effort, comments to tester), and watch for the automatic grader reaction and notifications
- [ ] Move to the next project by marging the last commits into `main` and opening a new branch `git switch -c 01`
- [ ] Optional: if you want an automated email reminder for the course submissions, make also a change in the file `github\workflow\submit-reminder.yaml`

### General Projects Task List
- Start a project branch 'xx'
- Follow project instructions, at book site (or internal html file) + course specific project instructions
- Commit your work for every valuable increment
- Test and push your work frequently, until completion
- Submit by opening a pull request, fill submission details, and get some atomatic or manual feedback
- Next, are project specific instructions. Some more suggestions and guidance appear in the course presentations and instructions document:

### Specific Poject Task List

#### Project 01
 - Save each implemented chip in it's own commit
 - Run the test script `cd projects/01; python test_01.py` (and in the same way for all other projects)
 
#### Project 04
 - Add pseudo-high-level-code as comments for every few assembly instructions
 - Commit each program separately
 - For manual testing, change the simulator to "No Animation" state

#### Project py (Python)
 - Complete at least the first 9 notebooks at `./projects/py/notebooks/beginner/exercises/`, See notebook list and order in `./projects/py/README.md` (nicer to view from github) or in the project `tesy_py.py` script
 - Commit each notebook separately
 - Since running the test script chenges the notebooks, from git prespective you might consider running them seperately, e.g., `python test_py.py strings`

#### General Software Pojects Task List
- In case you use the given code skeleton, remove `TODO` comments after implementing
- Code should comply with python's PEP 8 style guide and coding conventions (enforced by the flake8 module)
- Software engineering: code should be well designed, modularized, documented, readable, etc.

#### Project 06
- Develop at least 4 pytest developer tests in the inner `tests` folder (see example there)
- Suggestion: try working in a TDD way, and commit when you have a failing tests and also when it passes
- Tip: to run your programs with the inline VSCode debugger, you can edit the args in `.vscode/launch.json`, e.g. with, `"args": "add"]`

#### Project 07
- You are required to add at least 5 developer tests
- These tests should achieve at least 50% code coverage
- Tip: to see what code is not yet covered by the tests, run: `'python -m pytest ./tests/ --cov=hvmCodeWriter --cov-report term --cov-report html`, this will generate an html report (inside the folder `htmlcov`) which colors in red the non covered lines
- Tip: to run your programs with the inline VSCode debugger, you can edit the args in `.vscode/launch.json`, e.g. with, `"args": ["-t", "-d", "ExpressionLessSquare"]`

#### Project 08
- Copy project `07` python source files to folder `08`, incl. develpoer tests (but without the examples used for system tests), make a commit for this step and then switch to branch 08
- You are required to add 5 more developer tests (10 with project's 07)
- These tests should achieve at least 85% code coverage

#### Project 09
- Develop your own non-trivial Jack application
- Add a `.\projects\09\test.md` file that describes how to test your application
- Add a `README.md` file in your application foler, based on the example in `.\projects\09\MyApp`

#### Project 10
- The skeleton implementation has various flags:
  - `-t`: generate tokens file
  - `-s`: add source line as comments
  - `-d`: do not catch errors (can help debug to break on error)
  - `xml = True`: inline code option for generating xml outputs

#### Project 11
- Copy project `10` python source files to folder `11` (this time the examples from 10 can also be used for testing the SymbolTable), make a commit for this step and then switch to branch 10
- The system tests only verfy .vm files existance, the rest of verification is by manual running of the compilation results


### Some helpful links for working in the course with git/github
We will use the Github pull request mechanism for the course submissions.

1. [**Fork**][fork-a-repo] the course private repository to your github account.
1. [**Clone**][clone-a-repo] the repository to your machine (in case later updates are added: first add a [remote][config-remote] to the upstream repo and [sync][sync-remote] with a [pull][ref-pull]:  ```git pull upstream main```).
1. Start a [**branch**][branch] named `xx` for every sub project `xx`
1. Save and [**commit**][ref-commit] your work regulary
1. Update the README submission table
1. [**Push**][ref-push]/sync the changes up to GitHub.
1. Then, [create a **pull request**][working-with-prs] on the previous branch of **your** repository. 
1. You better [setup ssh][about-ssh] for connecting to github

Good luck!

<!-- Links -->
[fork-a-repo]: https://docs.github.com/en/get-started/quickstart/fork-a-repo
[clone-a-repo]: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
[config-remote]: https://help.github.com/articles/configuring-a-remote-for-a-fork/
[sync-remote]: https://help.github.com/articles/syncing-a-fork/
[ref-pull]: https://git-scm.com/docs/git-pull
[branch]: https://docs.github.com/en/free-pro-team@latest/articles/about-branches
[ref-commit]: https://git-scm.com/docs/git-commit
[ref-push]: https://git-scm.com/docs/git-push
[pull-request]: https://help.github.com/articles/creating-a-pull-request
[working-with-prs]: https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/proposing-changes-to-your-work-with-pull-requests
[about-ssh]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh