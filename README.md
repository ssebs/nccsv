# nccsv

nccsv - Ncurses CSV Editor written in Python

## Install Dev (on windows)
- $ python3 -m venv venv
- $ . venv/bin/activate
- (venv) $ pip install -r windows-curses

## Install Prod
- tbd

## Usage
- Dev:
  - (venv) $ python run.py [Filename]
- Prod:
  - tbd

## TODO:
- [ ] Architecture
  - [x] Wireframes
    - [x] Home / Menu
    - [ ] File selector
      - [ ] Open
      - [ ] Close
    - [ ] Editor
      - [ ] Layout Grid
      - [ ] Entry
- [ ] Multiple views
  - [ ] Home / Menu
  - [ ] File selector
  - [ ] Editor
- [ ] Custom widgets
  - [ ] Layout Grid
  - [x] Entry (text editor with box)
- [ ] Scroll down / right
- [.] Delete contents of cell when you hit "DEL"
- [ ] Row / Col bars (A,B,C, 1,2,3)
- [.] Actually handle CSVs
- [ ] Color
- [ ] Documentation
- [ ] Publish to pip
- [ ] Tests

> Misc folder is for miscellaneous test files to add features (pad scrolling, etc)

## Notes

How the Textbox should work:
- Is an Object
- Constr:
  - Has x, y coord on the master screen?
    - Do we want this?
    - Can we make it have it's own coordinates, so we don't have to worry about the master screen?
  - Has size definition
  - Custom callback if wanted
  - Default text (to load in)
- Props:
  - Text to display
  - Is it highlighted
- Input:
  - When calling edit_text(), it will edit the text and return it back on Enter
  - When calling clear_text(), it will remove the text that is rendered + saved
- Features:
  - Editable text field
  - Box surrounding text field so we can see it
  - Highlight-able (on hover)
  - Easy to get the text programmatically

How the grid should work:
- Is an Object
- Constr:
  - Has x, y coord on the master screen
  - Has rows / cols
- Props:
  - 2D Matrix of Textboxes
  - Keeps track of which box is selected
- Input:
  - Can scroll up/down/left/right
  - On Enter, send input to Textbox object to handle
  - On Del, clear the input of the Textbox
  - On Ctrl + S, it saves
  - On Q, it quits
- Features:
  - Load a 2D matrix from a file (csv)
  - Save a 2D matrix from a file (csv)
  - Add rows and columns if user scrolls past what currently exists

## LICENSE
[MIT](./LICENSE) &copy; 2020 Sebastian Safari
