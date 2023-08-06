# The `jsonstrip` Python module

The `jsonstrip` removes comments from a JSON document.
It can  be used as a Python module:

```
import jsonstrip

...
with open(filename, 'r', encoding='utf-8') as file:
    data = json.loads(jsonstrip.strip(file.read()))
```

or as a command line filter:

```
python3 -m jsonstrip < commented.json > regular.json
```

What makes `jsonstrip` unique is that it preserves line/column position of text.

#### Why do we need to strip comments from JSON?

The [JSON specification](https://www.json.org/json-en.html) does not allow comments.
A commented JSON is invalid JSON. This limitation does not matter when computer
programs exchange data, but sometimes an admin needs to write a configuration
or a similar file in JSON format and wants to comment the contents. Those comments
need to be removed before the document can be loaded.

#### Which comment types are recognized?

JavaScript (JS) comments - both single line and multi-line -
and since version `22.10.20`
also the widely-used (but not valid in JS) hash sign comments.

## Features

- The **main feature** is that line/column position of text is preserved.
  A hand-edited file may contain mistakes and in case of an error like below,
  the exact position can be easily found in the original document and corrected there.

  ```
  json.decoder.JSONDecodeError: Expecting value: line 15 column 40
  ```

- The input document is properly parsed in order not to modify strings that happen
  to look like comments:

  ```
  [
  /* this is a comment and will be removed */
  "but /* this is a string and it will be left untouched */",
  "this is // not a line comment"   // the real comment is here
  ]
  ```

- It comes with a `jsoncheck` utility described below.

- The `jsonstrip` is short, simple, fast, open-source and free.

### What it doesn't do

The author has decided to keep the `jsonstrip` as simple as possible.

- The `jsonstrip` does not minimize the JSON document.
  It does not strip any unneeded whitespace.

- The `jsonstrip` does not verify the JSON. It is assumed
  that its output will be loaded by a decoder and will be verified there.

- The `jsonstrip` does not even verify the comments. If a comment is open
  with `/*`, but not properly closed with `*/`,  the rest of the document
  becomes a comment and as such it will be removed without a warning.

## Installation

Install with `pip` from the PyPI.

## How it works

### Single line comments

A single line comment starts either with two forward slashes `//` or a single hash sign `#`
and continues until the end of a line. Single line comments are removed.

Input:
```
[10, 20, // this is a comment and will be removed
30, 40]  # this text is also a comment
```

Output:
```
[10, 20, 
30, 40]  
```

### Multi-line comments

A multi-line comment (also called a block comment) starts with `/*` and ends with `*/`.
These comments are removed when occurring at the end of line and replaced
by whitespace elsewhere.

Input:
```
{"name": "foo", "value": 1001 /* comment */, "flag": true }
```

Output; note the unchanged position of the text:
```
{"name": "foo", "value": 1001              , "flag": true }
```

Note that multi-line comments cannot be nested, the `*/` sequence
always terminates a comment:

```
/*
 * text
 * text  /* a comment inside a comment (WRONG!) */
 * BEWARE: no longer a comment
 */
```

## The `jsoncheck` command line utility

This little program reads a commented JSON document, strips the comments
and decodes the resulting JSON to check if there are any errors. JSON objects
(i.e. Python dicts) are checked for duplicate keys. (Note that the standard
Python JSON decoder accepts duplicate keys and each occurrence overwrites
the previous one. That makes some errors difficult to spot.)

The result is printed on the standard output, one line for each input file.

#### Usage

```
# without arguments it reads from the stdin:
some-program | jsoncheck

# with arguments it checks the named files:
jsoncheck filename1 [filename2 ...]
```

#### Exit code

- 0 = all input files are OK
- 1 = invalid JSON in some input file(s)
- 2 = I/O error reading some input file(s)
- 3 = both errors 1 and 2 occurred
