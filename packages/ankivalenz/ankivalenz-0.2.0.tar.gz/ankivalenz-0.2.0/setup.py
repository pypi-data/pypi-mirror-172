# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ankivalenz']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'genanki>=0.13.0,<0.14.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ankivalenz = ankivalenz.main:app']}

setup_kwargs = {
    'name': 'ankivalenz',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Ankivalenz\n\nAnkivalenz is a tool for generating Anki notes from HTML files.\n\n## Tutorial\n\nIn this walk-through we will write our notes as Markdown files, use\npandoc[^pandoc] to convert them to HTML, and finally use Ankivalenz to\ngenerate an Anki deck with Anki notes extracted from our Markdown files.\n\n### Installation\n\nAnkivalenz is distributed as a Python package, and requires Python 3.10+. To install:\n\n```\n$ pip3 install ankivalenz\n```\n\n### Initialize project\n\nCreate a folder for your notes:\n\n```\n$ mkdir Notes\n$ cd Notes\n```\n\nAnkivalenz needs a configuration file, containing the name and ID of the\nAnki deck. This can be generated with `ankivalenz init`:\n\n```\n$ ankivalenz init .\n```\n\n### Write a note\n\nAdd the following to a file named `Cell.md`:\n\n```markdown\n# Cell\n\n## Types\n\n- Prokaryotic ?:: does not contain a nucleus\n- Eukaryotic ?:: contains a nucleus\n```\n\n### Generate Anki deck\n\nConvert it to HTML:\n\n```\n$ pandoc Cell.md > Cell.html\n```\n\nAnd run Ankivalenz:\n\n```\n$ ankivalenz run .\n```\n\nThis generates a file `Notes.apkg` that can be imported to Anki. Open\nAnki and go to File -> Import, and find `Notes.apkg`.\n\n### Review\n\nThe new Anki deck will have two notes:\n\n| Question    | Answer                     | Path         |\n| ----------- | -------------------------- | ------------ |\n| Prokaryotic | does not contain a nucleus | Cell > Types |\n| Eukaryotic  | contains a nucleus         | Cell > Types |\n\nThis is what the first note looks like in Anki:\n\n![Anki review](images/anki-review.png)\n\n## Syntax\n\n### Front/back cards\n\nAnkivalenz supports front/back cards, where the front is the question\nand the back is the answer. To create a front/back card, add a new list item\nwith the question, followed by `?::` and the answer:\n\n```markdown\n- Color of the sun ?:: Yellow\n```\n\nYou can flip the order of the question and answer by using `::?` instead:\n\n```markdown\n- Anwer ::? Question\n```\n\n#### Two-way notes\n\nTwo-way notes can be created with `::`:\n\n```markdown\n- Side 1 :: Side 2\n```\n\nThis will create two cards in Anki:\n\n| Front  | Back   |\n| ------ | ------ |\n| Side 1 | Side 2 |\n| Side 2 | Side 1 |\n\n#### Standalone questions/answers\n\nSometimes you want to create a note refering to the parent heading.\nThis can be done with standalone questions/answers:\n\n```markdown\n- Sun\n  - ::? The star in our solar system\n```\n\nThis will create a note with the answer "Sun" and the question "The star\nin our solar system". The other types of delimeters ("::" and "?::") can\nbe used in the same way.\n\n### Cloze cards\n\nAnkivalenz supports cloze deletion[^cloze], where the answer is hidden in the\nquestion. To create a cloze card, add a new list item with the question,\nusing Anki\'s cloze syntax:\n\n```markdown\n- The {{c1::sun}} is {{c2::yellow}}.\n```\n\n### Nested lists\n\nLists can be nested:\n\n```markdown\n- Solar System\n  - Star ?:: Sun\n  - Planet\n    - Earth ?:: Blue\n    - Mars ?:: Red\n```\n\nThe headings for the nested lists become a part of the notes\' paths:\n\n| Question | Answer | Path                  |\n| -------- | ------ | --------------------- |\n| Star     | Sun    | Solar System          |\n| Earth    | Blue   | Solar System > Planet |\n| Mars     | Red    | Solar System > Planet |\n\n### Math\n\nIf you are writing Markdown files, and use pandoc to convert them,\nthe following syntax for math is supported:\n\n```markdown\n- Inline math: $1 + 2$\n- Display math: $$1 + 2$$\n```\n\nWith the `--mathjax` flag, pandoc will generate the correct markup,\nusing `\\( ... \\)` as delimeters for inline math, and `\\[ ... \\]` as\ndelimeters for display math:\n\n```\n$ pandoc --mathjax Note.md > Note.html\n```\n\n[^pandoc]: https://pandoc.org/\n[^cloze]: https://docs.ankiweb.net/editing.html#cloze-deletion\n',
    'author': 'Harry Vangberg',
    'author_email': 'harry@vangberg.name',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
