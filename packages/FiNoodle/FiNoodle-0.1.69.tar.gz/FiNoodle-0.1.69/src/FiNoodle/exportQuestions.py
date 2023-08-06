from pathlib import Path
from .moodle_compile.compile import importQuestions
from datetime import datetime

import typer
from typer import Argument, Option

app = typer.Typer(
    add_completion=False,
)

def build(root: Path = Path("questions"), globPattern = {
        "exportGlob": "",
        "blackListGlob": "None",
        "IterateChildren": False
    }):

    print("============")
    print("Finale 0.1.8")
    print("============")
    print()

    print("[{}] Starting Finale".format(datetime.now().strftime("%H:%M:%S")))

    #targeted export by glob & exclusion by glob
    #export Children decides whether or not you want to export 
    #children of glob pattern category
    #make sure blackListGlob isn't accidentally blacklisting everything
    #use Null to match with nothing and "" to match with everything
    xml = importQuestions(root, globPattern)
    with open("out.xml", "w") as f:
        f.write(xml)

@app.command(
    "new",
    help="Generates a blank question template in the current working directory",
)
def new(
        qpath: str = Argument(
            ...,
            help="The question type to generate",
        ),
        name: str = Argument(
            ...,
            help="The name of the question to generate",
        ),
        qtype: str = Argument(
            ...,
            help="The question type to generate",
        ),
):
    createBlankQuestion(qpath, name, qtype)

def createBlankQuestion(qpath, name, qtype):
    qpath = f'{qpath}/{name}.{qtype}'
    qloc = Path('questions').joinpath(qpath)

    #create support files folder
    createPath = qloc.joinpath('Support Files')
    createPath.mkdir(parents=True, exist_ok=True)
    
    #create a prompt.md for all
    qloc.joinpath('prompt.md').touch(exist_ok=True)
    
    #create a Feedback.txt for .sa and .de
    if qtype in ["sa", "de"]:
        qloc.joinpath('Feedback.txt').touch(exist_ok=True)

    #create testcases.toml and answers.py for .cr
    if qtype == "cr":
        qloc.joinpath('testcases.toml').touch(exist_ok=True)
        qloc.joinpath('answers.py').touch(exist_ok=True)

    #create answers.toml for .sa and .mc
    if qtype in ["sa", "mc"]:
        qloc.joinpath('answers.toml').touch(exist_ok=True)
    
    
if __name__ == '__main__':
    app()
