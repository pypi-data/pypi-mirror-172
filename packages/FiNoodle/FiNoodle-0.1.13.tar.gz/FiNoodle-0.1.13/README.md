<!-- TITLE -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <a href="https://freeimage.host/i/QExVpf"><img src="https://iili.io/QExVpf.md.png" alt="QExVpf.md.png" border="0"></a>
  </a>

  <p align="center">
    Python program that can transform a suite of Moodle Question data 
    <br>
    in a format specified by the client to Moodle XML and back.
  </p>
</div>

<br>

<!-- ABOUT THE PROJECT -->
## About The Project
The process to write CodeRunner questions with Moodle is difficult and the number of options makes question creation long and tedious. This means that teaching staff spend large amounts of time working simply writing out the questions, and the process leads to a high incidence of question errors.

Based on <a href="https://github.com/James-Ansley/moodle-toml">Toodle</a> by <a href="https://github.com/James-Ansley">@James-Ansley</a>, `FiNoodle` by Finale supports various question types (including CodeRunner, short answer, multiple choice, etc.) and provide warnings for common errors in generating questions. FiNoodle also various supports question templates to generate questions in a consistent and precise format.

<br>

<!-- BUILT WITH -->
### Built With

* Python (3.10)
* Moodle
* XML
* Jinja (3.1.2)

<br>
<hr>
<br>

<!-- INSTALLATION -->
## Installation
```
pip install FiNoodle
```
FiNoodle supports installing using pip. Enter the command above in the project folder to install FiNoodle.

<br>
<hr>
<br>

<!-- USAGE -->
## Usage
Place files for questions in `../Finale/questions/` and run `../Finale/src/FiNoodle.py`. An output file called `out.xml` will be generated in the project folder which can be loaded to Moodle directly.

<br>

### Supported File Types
* `.py`: Python programs
* `.md`: Prompt messages
* `.toml`: Test cases
* `Folders`: Supporting files (including images)

<br>

### Supported Question Types
* `.cr`: CodeRunner
* `.mc`: Multiple choice
* `.sa`: Short answer
* `.de`: Description

<br>
python src/FiNoodle/FiNoodle.py new questions/CLIBuilt/Quiz1 blank cr
<hr>
<br>

<!-- REQUIREMENTS -->
## Requirements
* Markdown~=3.3.7
* Jinja2~=3.1.2

<br>
<hr>
<br>

<!-- FUTURE PLAN -->
## Future Plan
* Question repository: Managing and loading questions from external sources.
* More question types: Filling the blanks.
* More error checking: Duplicated questions.

<br>
<hr>
<br>

<!-- THE TEAM -->
## The Team
* Carl Taka
* Mongkulviseth Rithy
* Sam Shoykhet
* Sambav Ravivenkatesh
* Shejie Shuang
* Yunu Choi

<br>

* Trello board: https://trello.com/b/4HmtI49x/399-project-kanban

<br>
<hr>
<br>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* Toodle (<a href="https://github.com/James-Ansley">@James-Ansley</a>): https://github.com/James-Ansley/moodle-toml
* Best-README-Template : https://github.com/othneildrew/Best-README-Template