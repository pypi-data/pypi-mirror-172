import os
import unicodedata
from IPython.display import display, Javascript, clear_output
from ipywidgets import widgets


def js_rename_save_notebook(prefix):
    """
    creates javascript to rename, save and opens a new tab to download a jupyter notebook

    :param prefix: Prefix od the new name of the notebook
    """
    return """
function save_me() {

    var baseurl = location.protocol+"//"+location.host;
    var path = location.pathname.replace('/notebooks/', '/nbconvert/notebook/', 1)+"?download=true";
    var url = baseurl + path;
    var w = window.open('', IPython._target);
    if (Jupyter.notebook.dirty && Jupyter.notebook.writable) {
        Jupyter.notebook.save_notebook().then(function() {
            w.location = url;
        });
    } else {
        w.location = url;
    }
};

function rename_save(prefix) {
    var current_name = Jupyter.notebook.notebook_name;
    let base_name = Jupyter.notebook.metadata.savedownload.base_name || "Exam";
    let new_name = prefix + "_" + base_name;
    
    if (current_name.substring(0, current_name.length - 6) != new_name) {
        Jupyter.notebook.rename(new_name).then(function() {
            save_me();}
        );
    } else {
        save_me();
    }
};

rename_save('%s');
""" % (
        prefix
    )


def strip_accents(s):
    """remove accents from string"""
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


class SaveDownloadExam:
    def __init__(self, globals, student_name_var="NAME"):
        self.globals = globals
        try:
            self.login_name = os.getlogin()
        except OSError:
            if "JUPYTERHUB_USER" in os.environ and os.environ["JUPYTERHUB_USER"]:
                self.login_name = os.environ["JUPYTERHUB_USER"]
            elif "USER" in os.environ and os.environ["USER"]:
                self.login_name = os.environ["USER"]
            else:
                self.login_name = "user"

        self.student_name_var = student_name_var
        self.js = ""

    def _display_js(self, _=None):
        clear_output()
        display(Javascript(self.js))

    def check_name(self, name):
        """Check if the variable `name` is set, a string and not empty"""
        return (
            name in self.globals
            and self.globals[name]
            and isinstance(self.globals[name], str)
        )

    def build_notebook_prefix(self):
        student_name = (
            self.globals[self.student_name_var]
            .title()
            .replace(" ", "")
            .replace("_", "")
        )
        return "_".join(
            ("Submission", self.login_name, strip_accents(student_name))
        )

    def run(self):
        if not self.check_name(self.student_name_var):
            label = widgets.HTML(
                value=(
                    '<h3 style="color: rgb(244,67,54)">You didn\'t put your name in the variable '
                    f"<code>{self.student_name_var}</code> or you forgot to run that cell.</h3>"
                    "<ol><li>Please go back to the top of this notebook and add your name to the variable "
                    f"<code>{self.student_name_var}</code> and run the cell.</li>"
                    "<li>Go back to this cell and run it again.</li>"
                    "</ol>"
                )
            )
            clear_output()
            display(label)
            return
        notebook_name = self.build_notebook_prefix()
        self.js = js_rename_save_notebook(notebook_name)
        layout = widgets.Layout(width="auto", height="40px")  # set width and height
        button = widgets.Button(
            description="Save and Download Exam",
            icon="fa-download",
            button_style="success",
            display="flex",
            flex_flow="column",
            align_items="stretch",
            layout=layout,
        )
        button.on_click(self._display_js)
        label = widgets.HTML(
            value=(
                "<h3>Are you ready to download this notebook for submission?</h3>"
                f"<p>You have set the variable <code>{self.student_name_var}</code> to "
                f"<b>{self.globals[self.student_name_var]}</b>.</p>"
                "<p>If this is correct and you want to download this notebook for submission, "
                "then press the button below.</p>"
            )
        )
        clear_output()
        display(label)
        display(button)
