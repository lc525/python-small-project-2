This tool is published as a supervision solution sample for an introductory
CLI python project which applies simple transforms to csv files.
Do not use the code in production or in performance sensitive contexts; instead,
please use mature csv or json parsing libraries.

run from the directory containing this file (README.md) like this:

$ python -m csvtr in.csv out.csv 2,1,1
or
$ python -m csvtr in.sjson out.csv

The supervision task definition given to students is reproduced below:

This supervised small project is a continuation of the previous python project
which dealt with simple csv transformations.

1. High-level goals

You will use the knowledge and python coding skills accumulated in small project
1 to write a slightly more complex piece of code, starting from the definition
of the extension in small project 1.

This means you will likely not need to learn new syntactical elements in Python
and can focus on:
  * learning how to write code to achieve a particular goal
  * holding in your mind the context of a larger piece of code, with an
    increased number of code paths and interracting parts of code
  * learning how to collaborate / write code starting from a code base which you
    haven't written yourself

You will build a fairly fully-fledged parser for the simple-json (sjson) data
format, starting from a given code skeleton.

2. Structure

You will write most of your code in csvtr/sjson_transform.py
That file already contains a skeleton towards parsing the sjson format,
you need to add code so that the parser is complete and can parse
arbitrarily-nested sjson elements, while converting them "on-the-fly" to csv.

3. .sjson file format definition:

- The top level element is always an array, but if the file contains something
  else an error must be shown, together with the line where the parsing error
  occured
- The top-level array contains dictionaries delimited by curly braces ({ and })
- A dictionary is formed of key-value pairs delimited by :
- A dictionary KEY is always a quoted string, and the presence of anything else
  should trigger a parsing error identifing the line where the error occured.
- A dictionary VALUE can be:
    - another dictionary
    - an array
    - a quoted string
    - a number (integer or floating-point)
- Dictionary key-value pairs are separated between them with commas (but the
  last key-value pair in the dictionary is not followed by a comma)
- Array elements may be:
    - other arrays
    - dictionaries
    - quoted strings
    - numbers (integers or floating-point numbers)
- The elements of an array need NOT all be of the same type. For example, the
  following array is considered valid:

  [1, "hello", { "day": 20 }, 5]
- Array elements are separated by commas, but there is no comma after the last
  element
- Dictionaries and arrays may nest to arbitrary depth
- Line breaks may appear pretty much anywhere in the file, with the following
  exceptions:
    - a quoted string needs to both begin and end on the same line (multi-line
      strings just need to add \n inside the string)
    - a number needs to end on the same line it started
- Whitespace (space, tab) can appear anywhere throughout the file, without changing the
  parsed structure

4. .csv conversion rules:

- assume that all the dictionaries which are part of the top-level
  array have essentially the same structure, although the order in which the
  keys appear is not fixed
- each nesting level adds a segment into the resulting csv column name, with
  arrays adding the index of the current element and dictionaries adding the key
  name. An example will clarify this rule:

  Say we have the following file:

  [
    { "file": "test.dat"
      "segments":
        [ {"id": 1,
           "use": "symbols",
           "elements": [ "init", "__main__", "__exit__", "square_root" ],
           "owner": "lc525"
          },
          {"id: 2,
           "use": "const",
           "elements": ["hello world", "supervision", "small project 2"],
           "owner": "lc525"
          }
        ]
    }
  ]

 the columns of the generated csv file will be:
 file,
 segments/0/id, segments/0/use,
 segments/0/elements/0, segments/0/elements/1, segments/0/elements/2, segments/0/elements/3,
 segments/0/owner,
 segments/1/id, segments/1/use,
 segments/1/elements/0, segments/1/elements/1, segments/1/elements/2, segments/1/elements/3,

 A column name like:

 segments/1/elements/0

 translates in: the values from this column were part of the "segments" subtree,
 in the second element of the array, at the elements key and in the first
 element of the array in elements


You need to devise a strategy for parsing this input in a way which also gives
proper errors and error line numbers when a parsed file deviates from the spec.

You do not need to use all the utility functions already provided in the
csvtr/sjson_transform.py file, as slightly different code approaches can also
work. However, it is strongly recommended you keep the basic structure of a
state-machine-based parser: it develops your experience in constructing fairly
complex state machines.

5. Questions in top-file comment of sjson_transform.py file

Those are food-for-thought while constructing the parser and are subject to
discussion during face-to-face meetings
