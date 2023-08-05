#!/usr/bin/env python3

import pathlib
import os

import exploration


def pickExistingFile(kind: str) -> pathlib.Path:
    """
    Uses `input` to prompt the user to select an existing file in the
    current directory (or a custom path they type in). Continues
    prompting until an existing file is named. The `kind` argument is
    used before the word 'file' to describe what is being requested; it
    should normally include an article, e.g., 'a source' or 'an input'.
    """
    options = os.listdir('.')
    prompt = f"""\
Select {kind} file:
  """ + '\n  '.join(
    f"[{n}] '{options[n]}'"
    for n in range(len(options))
) + f"""[{len(options)}] Other...
Pick a number from the list above (default 0): """
    selection = 'a'
    while selection.strip() and not selection.strip().isdigit():
        selection = input(prompt)

    if selection.strip() == '':
        index = 0
    else:
        index = int(selection.strip())

    if index < len(options):
        return pathlib.Path(options[index])

    path = None
    prompt = "Write the path you want to use as {kind} file: "
    while path is None or not path.isfile():
        if path is not None:
            if path.exists():
                print("You must pick a regular file, not a directory.")
            else:
                print("The file '{path!s}' does not exist.")
        pathStr = input(prompt)
        path = pathlib.Path(pathStr)

    return path


def pickOutputFile(
    purpose: str,
    preferNew: bool = True
) -> pathlib.Path:
    """
    Uses `input` to prompt the user for a filename to be used for the
    given purpose. If `preferNew` is set to `True`, a confirmation
    prompt will be displayed when the user picks a file that already
    exists, which warns that the file may be overwritten. The resulting
    path will not be an existing directory.
    """
    result = None
    prompt = "Write the path to the file you want to use for {purpose}: "
    while result is None or result.isdir():
        if result is not None:
            print(
                f"'{result!s} is a directory, so it can't be used for"
                f" {purpose}."
            )
        result = pathlib.Path(input(prompt))

        if preferNew and result.exists():
            overwrite = input(
                f"File '{result!s}' already exists. Are you sure you"
                f" want to use it for {purpose} (it may be"
                f" overwritten)? [y/N] "
            )
            if overwrite.strip().lower() in ('y', 'yes'):
                print(
                    f"Okay, we will use '{result!s}' for {purpose} even"
                    f" though it already exists."
                )
            else:
                print(f"Okay, pick another file t use for {purpose}...")
                result = None

    return result


if __name__ == "__main__":
    command = input("""\
Choose the command:
  [0] display a decision graph
  [1] analyze an exploration or decision graph
  [2] convert an exploration or decision graph
What would you like to do? (enter a number; default is 0) """)
    if command.strip() == '1':  # analyze
        source = pickExistingFile('a source')
        try:
            sourceType = exploration.main.determineFileType(str(source))
        except ValueError:
            print(
                f"We didn't recognize the file extension of"
                f" '{source!s}' so we assume it's a journal."
            )
            sourceType = "journal"
        exploration.main.analyze(source, formatOverride=sourceType)

    elif command.strip() == '2':  # convert
        source = pickExistingFile('a source')
        try:
            sourceType = exploration.main.determineFileType(str(source))
        except ValueError:
            print(
                f"We didn't recognize the file extension of"
                f" '{source!s}' so we assume it's a journal."
            )
            sourceType = "journal"
        output = pickOutputFile('output')
        try:
            outputType = exploration.main.determineFileType(str(output))
        except ValueError:
            print(
                f"We didn't recognize the file extension of"
                f" '{output!s}'."
            )
            if sourceType == "graph":
                print(
                    "We assume you wanted to convert the input graph"
                    " into GraphViz DOT format."
                )
                outputType = "dot"
            elif sourceType == "dot":
                print(
                    "We assume you wanted to convert the input graph"
                    " into JSON format."
                )
                outputType = "graph"
            elif sourceType == "exploration":
                print(
                    "We assume you wanted to convert the input"
                    " exploration into journal format."
                )
                outputType = "journal"
            else:
                print(
                    "We assume you wanted to convert the input"
                    " exploration into JSON format."
                )
                outputType = "exploration"
        exploration.main.convert(
            source,
            output,
            inputFormatOverride=sourceType,
            outputFormatOverride=outputType
        )

    else:  # show
        if command.strip() not in ('0', ''):
            print(
                f"Invalid command '{command}' assuming you meant 0"
                f" (display a graph)"
            )
        source = pickExistingFile('a source')
        try:
            sourceType = exploration.main.determineFileType(str(source))
        except ValueError:
            print(
                f"We didn't recognize the file extension of"
                f" '{source!s}' so we assume it's a journal."
            )
            sourceType = "journal"
        exploration.main.show(source, formatOverride=sourceType)
