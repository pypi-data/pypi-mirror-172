# object-settings

Simple object-oriented Python config library, where your settings are objects.

Their values get saved to a standard config location, depending on the os (uses `appdirs` package for paths). The file is automatically written and read in the background, so you don't have to worry about it, and it's quick to define and use settings (see examples below)


## Installation

This module is on PyPi, so you can just do
`pip install object-settings`


## Usage

    import settings
    settings.setup("Your app name")
    
    your_option1 = settings.Toggle("Your first option label")
    your_option2 = settings.Number("Your second option label")


## Examples

You can set a font size at the top of your ui file:

    font = settings.Number(default=14)

    ...
    someuilib.Label("Bababooey", size=font.value)
    ...
    someuilib.Textbox("Lorem ipsum dolor...", font_size=font.value)
    ...


Or if a setting is only checked in one place, it can be used without defining a variable:

    if settings.Toggle("Update app automatically", default=True):
        # do update

(though it doesn't matter if the same setting is initialized multiple times)


## Setting types

List of currently available setting types and the variables they use as values:

- Toggle (bool)
- Choice (any)  [from a list of options]
- Multichoice (list)  [of things from a list of options]
- Text (str)
- Path (str)
- Number (int)

