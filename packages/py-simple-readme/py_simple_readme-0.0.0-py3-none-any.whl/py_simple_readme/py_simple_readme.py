#!/usr/bin/env python
"""
# Main module for py_simple_readme
"""
from inspect import getfullargspec, signature

# This will ignore any class method of a given name
_IGNORED = []


class readme_generator:
    """Simple object to handle the programatic generation of readme.md files"""

    def __init__(
        self,
        title: str = None,
        slogan: str = None,
        footnote_title: str = "Notes:",
        footnote_heading_level: int = 2,
        numbered_toc: bool = False,
    ):

        self.title = title
        self.slogan = slogan
        # Dict to store alt text / image url pairs
        self.images = {}
        self.footnote_title = footnote_title
        self.footnote_heading_level = footnote_heading_level
        # List to hold current footnotes
        self._footnotes = []
        self._footnote_index = 1
        # Value to hold the current assembled body data.
        # It's probably best not to interact with this value directly
        self._body = ""
        # Current blockquote depth
        self.quote_depth = 0
        # Changelog is a dict of version strings mapped to update info strings
        self.changelog = {}

        self.toc_mark = "mark{}"
        self.toc_index = 0
        self.toc_contents = ""
        self.toc_depth = 0
        self.toc_indicies = {}

        self.numbered_toc = numbered_toc

        self.home_mark_name = self.toc_mark.format(self._get_toc_index())
        self.home_mark = f'<a name="{self.home_mark_name}"></a>'
        self.toc_marks = {0: self.home_mark_name, 1: self.home_mark_name}
        self.last_mark = self.home_mark_name

    def set_slogan(self, slogan: str):
        """Set readme slogan. This will appear directly below the readme title if set."""
        self.slogan = str(slogan)

    def _get_toc_index(self):
        """Internal unique toc index function"""
        self.toc_index += 1
        return self.toc_index - 1

    def increase_toc_depth(self):
        """Increase table of contents depth"""
        self.toc_depth += 1
        self.toc_indicies[self.toc_depth] = 0
        self.toc_marks[self.toc_depth] = self.last_mark

    def decrease_toc_depth(self):
        """Decrease table of contents depth"""
        if self.toc_depth == 0:
            raise ValueError("toc depth already at 0.")
        self.toc_depth -= 1

    def insert_footnote(self, text: str):
        """Inserts a footnote at the current point in the readme body."""
        self._body += f"[^{len(self._footnotes)+1}]"
        self._footnotes.append(text)

    def add_toc(self, title: str, end: str = "\n"):
        """Add an entry to the table of contents at the current point in the readme body."""
        mark_name = self.toc_mark.format(self._get_toc_index())
        self.last_mark = mark_name
        self._body += (
            f'<a name="{mark_name}"></a>[^](#{self.toc_marks[self.toc_depth]}){end}'
        )
        if self.toc_depth in self.toc_indicies:
            index = self.toc_indicies[self.toc_depth]
        else:
            self.toc_indicies[self.toc_depth] = index = 0
        val = index if self.numbered_toc else "-"
        self.toc_contents += "\t" * self.toc_depth + f"{val} [{title}](#{mark_name})\n"
        self.toc_indicies[self.toc_depth] = index + 1

    def get_prefix(self):
        """Returns the appropriate blockquote depth indicator"""
        return "> " * self.quote_depth

    def add_bold(self, text: str, end: str = ""):
        """Adds a bold piece of text at the current point in the readme body"""
        self._body += f"**{text.strip()}**{end}"

    def add_italic(self, text: str, end: str = ""):
        """Adds italicized piece of text at the current point in the readme body"""
        self._body += f"*{text.strip()}*{end}"

    def add_horizontal_rule(self):
        """Adds a horizontal rule at the current point in the readme body"""
        self._body += f"{self.get_prefix()}---\n\n"

    def add_link(self, link: str, text: str = None, tooltip: str = None):
        """Adds a link at the current point in the readme body"""
        if not text:
            text = link
        if tooltip:
            self._body += f'[{text}]({link} "{tooltip}")'
        else:
            self._body += f"[{text}]({link})"

    def add_heading(
        self, text: str, level: int = 1, end: str = "\n", add_toc: bool = True
    ):
        """Add a heading, set "add_toc" keyword to add a table of contents entry. Set "end" keyword to change the line ending."""
        if not level or level < 0 or level > 6:
            raise ValueError(
                f"Invalid heading level - {level}, must be in range 0-6. 0 results in regular text."
            )
        self._body += self.get_prefix() + "#" * level + f" {text}"
        if add_toc:
            self.add_toc(text)
        self._body += end

    def add_heading_1(self, text: str, **kwargs):
        """Add a level 1 heading, set "add_toc" keyword to add a table of contents entry."""
        self.add_heading(text, 1, **kwargs)

    def add_heading_2(self, text: str, **kwargs):
        """Add a level 2 heading, set "add_toc" keyword to add a table of contents entry."""
        self.add_heading(text, 2, **kwargs)

    def add_heading_3(self, text: str, **kwargs):
        """Add a level 3 heading, set "add_toc" keyword to add a table of contents entry."""
        self.add_heading(text, 3, **kwargs)

    def add_heading_4(self, text: str, **kwargs):
        """Add a level 4 heading, set "add_toc" keyword to add a table of contents entry."""
        self.add_heading(text, 4, **kwargs)

    def add_heading_5(self, text: str, **kwargs):
        """Add a level 5 heading, set "add_toc" keyword to add a table of contents entry."""
        self.add_heading(text, 5, **kwargs)

    def add_heading_6(self, text: str, **kwargs):
        """Add a level 6 heading, set "add_toc" keyword to add a table of contents entry."""
        self.add_heading(text, 6, **kwargs)

    def add_paragraph(self, text: str, end: str = "\n\n"):
        """Add a paragraph to the current point in the readme body"""
        self._body += f"{self.get_prefix()}{text}{end}"

    def add_blockquote(self, text: str, end: str = "\n\n"):
        """Add a blockquoted paragraph at the current point in the readme body"""
        self.quote_depth += 1
        self.add_paragraph(f"{text}", end)
        self.quote_depth -= 1

    def add_multi_blockquote(self, texts: list):
        """Add multiple blockquoted paragraphs at the current point in the readme body"""
        i = 0
        end = len(texts) - 1
        for t in texts:
            self.add_blockquote(t, end="\n")
            if not i == end:
                self._body += ">\n"
            i += 1

    def add_unordered_list(self, texts: list, indent: int = 0):
        """Add an unordered (non-numbered) list as the current point in the readme body"""
        for t in texts:
            self._body += f"{self.get_prefix()}" + "\t" * indent + f"{t}\n"

    def add_ordered_list(self, texts: list, indent: int = 0):
        """Add an ordered (numbered) list as the current point in the readme body"""
        i = 1
        for t in texts:
            self._body += f"{self.get_prefix()}" + "\t" * indent + f"- {i}. {t}"
            i += 1

    def add_code_block(
        self,
        code: str,
        lang: str = "python",
        end: str = "\n",
        disable_prefix: bool = False,
    ):
        """Add a block of code at the current point in the readme body"""
        p = self.get_prefix()
        self._body += f"{p}```{lang}\n{code}\n{p}```{end}"

    def add_header_image(self, alt_text: str, url: str, replace_ok: bool = False):
        """Adds an image to the images placed under the project title / slogan"""
        if alt_text in self.images and not replace_ok:
            raise ValueError(
                f"Image with {alt_text} already exists. Use add_image(..., replace_ok=True) to disable this error."
            )
        self.images[alt_text] = url

    def set_header_images(self, images: dict, replace_ok: bool = False):
        """Sets a list of header images from a dict that maps image_alt texts to image urls."""
        for i in images:
            self.add_header_image(i, images[i], replace_ok=replace_ok)

    def set_changelog(self, changelog: dict):
        """Set the changelog with a dictionary of version strings mapped to update info strings."""
        # Makes it ok to set self.changelog back to None without an error
        if not changelog is None and not isinstance(changelog, dict):
            raise ValueError("Invalid changelog type set.")
        self.changelog = changelog

    def handle_class_list(self, classes: list):
        """Adds documentation for a list of classes at the current point in the readme body."""
        self.increase_toc_depth()
        for c in classes:
            self.add_heading_3(c.__name__, end="", add_toc=True)
            # self.add_toc(c.__name__)
            self.quote_depth += 1
            if c.__doc__:  # Add docstring
                self.add_paragraph(f"**{c.__doc__}**", end=f"\n{self.get_prefix()}\n")
            if hasattr(c, "__desc__"):  # Only print desc if it isn't inherited
                desc_inherited = False
                for b in c.__bases__:
                    if hasattr(b, "__desc__"):
                        if b.__desc__ == c.__desc__:
                            desc_inherited = True
                            break
                if not desc_inherited:
                    self.add_paragraph(c.__desc__, end="\n")

            classstring = f"class {c.__name__}("
            if len(c.__bases__) == 1:
                b = c.__bases__[0]
                classstring += b.__name__
            else:
                last = len(c.__bases__) - 1
                i = 0
                for b in c.__bases__:
                    classstring += b.__name__
                    if not i == last:
                        classstring += ", "
                    i += 1
            classstring += "):\n"
            sig = str(signature(c)).strip('"')
            sig = sig[:1] + "self, " + sig[1:]
            classstring = classstring + "\tdef __init__" + sig + ":\n\t\t...\n"
            methods = [
                m
                for m in dir(c)
                if (m.startswith("_") is False)
                and callable(getattr(c, m))
                and (not m in _IGNORED)
            ]
            if methods:
                for m in methods:
                    meth = getattr(c, m)
                    val = "..."
                    if hasattr(meth, "__doc__"):
                        if meth.__doc__:
                            val = f'"""{meth.__doc__}"""'
                    classstring += f"\tdef {m}{str(signature(meth))}:\n\t\t{val}\n"

            formatted_classstring = ""
            for l in classstring.splitlines():
                formatted_classstring += self.get_prefix() + l + "\n"
            self.add_code_block(formatted_classstring.strip(), lang="py")
            self.quote_depth -= 1
        self.decrease_toc_depth()

    def handle_function_list(self, functions: list):
        """Adds documentation for a list of functions at the current point in the readme body."""
        self.increase_toc_depth()
        for f in functions:
            self.add_heading_3(f.__name__, end="", add_toc=False)
            self.add_toc(f.__name__)
            self.quote_depth += 1
            self.add_paragraph(f"**{f.__doc__}**", end=f"\n{self.get_prefix()}\n")
            name = f.__name__
            funcstring = f"def {name}{str(signature(f))}:\n{self.get_prefix()}\t..."
            self.add_code_block(funcstring)
            self.quote_depth -= 1
        self.decrease_toc_depth()

    def assemble(self):
        """Generate the readme and return as a string."""
        out = ""
        if self.title:
            out = f"# {self.title}"
        out += f"{self.home_mark}\n\n"
        if self.slogan:
            out += f"***{self.slogan}***\n\n"
        if self.images:
            for k in self.images:
                out += f"![{k}]({self.images[k]})\n\n"

        if self.changelog:
            self.toc_depth = 0
            self.add_heading_1("Changelog")
            self.increase_toc_depth()
            for k in self.changelog:
                self.add_heading_2(k)
                self.add_paragraph(self.changelog[k])
            self.decrease_toc_depth()

        if self.toc_contents:
            out += self.toc_contents + "\n"
        out += "---\n\n"
        out += self._body
        if self._footnotes:
            for i in range(len(self._footnotes)):
                out += f"[^{i+1}]: {self._footnotes[i]}."
        return out

    def save(self, path):
        """Generate readme and save to a given location."""
        with open(path, "w+") as f:
            f.write(self.assemble())

    def id(self):
        """Alias for increase_toc_depth"""
        self.increase_toc_depth()

    def dd(self):
        """Alias for decrease_toc_depth"""
        self.decrease_toc_depth()

    def fn(self, text: str):
        """Alias for insert_footnote"""
        self.insert_footnote(*text)

    def toc(self, *args, **kwargs):
        """Alias for add_toc"""
        self.add_toc(*args, **kwargs)

    def b(self, *args, **kwargs):
        """Alias for add_bold"""
        self.add_bold(*args, **kwargs)

    def i(self, *args, **kwargs):
        """Alias for add_italic"""
        self.add_italic(*args, **kwargs)

    def hr(self):
        """Alias for add_horizontal_rule"""
        self.add_horizontal_rule()

    def l(self, *args, **kwargs):
        """Alias for add_link"""
        self.add_link(*args, **kwargs)

    def h1(self, *args, **kwargs):
        """Alias for add_heading_1"""
        self.add_heading_1(*args, **kwargs)

    def h2(self, *args, **kwargs):
        """Alias for add_heading_2"""
        self.add_heading_2(*args, **kwargs)

    def h3(self, *args, **kwargs):
        """Alias for add_heading_3"""
        self.add_heading_3(*args, **kwargs)

    def h4(self, *args, **kwargs):
        """Alias for add_heading_4"""
        self.add_heading_4(*args, **kwargs)

    def h5(self, *args, **kwargs):
        """Alias for add_heading_5"""
        self.add_heading_5(*args, **kwargs)

    def h6(self, *args, **kwargs):
        """Alias for add_heading_6"""
        self.add_heading_6(*args, **kwargs)

    def p(self, *args, **kwargs):
        """Alias for add_paragraph"""
        self.add_paragraph(*args, **kwargs)

    def q(self, *args, **kwargs):
        """Alias for add_blockquote"""
        self.add_blockquote(*args, **kwargs)

    def ul(self, *args, **kwargs):
        """Alias for add_unordered_list"""
        self.add_unordered_list(*args, **kwargs)

    def ol(self, *args, **kwargs):
        """Alias for add_ordered_list"""
        self.add_ordered_list(*args, **kwargs)

    def cb(self, *args, **kwargs):
        """Alias for add_code_block"""
        self.add_code_block(*args, **kwargs)
