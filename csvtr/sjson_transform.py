# This is an educational sample. The code parses a very specific type of
# simplified json (sjson) and converts it into csv; Not the most efficient
# parser possible, but characteristic of a state-machine based parser and
# written for legibility;
#
# Questions/Tasks:
#  - describe how the parser works
#  - identify if there are any input cases not covered by the parser, and if you
#    find any, change the parser to deal with them
#  - identify pieces of code that could be candidates for extracting in their
#    own function. how would you make this parser more modular and reduce code 
#    duplication?
#  - how would you refactor the code to make it more robust in reporting errors 
#    and identifying edge-cases?
#  - what trade-offs would be involved of choosing a parsing approach which
#    builds a tree representation of the data instead of the state machine here?
import os.path
import re
from enum import Enum

class ParseState(Enum):
    PARSE_TOP_ELEM = 1      # start state
    PARSE_ARRAY_ITEMS = 2
    PARSE_DICT_ITEMS = 3
    PARSE_END = 4           # stop state (success)
    MALFORMED = 6           # stop state (failure)

class DictParsing(Enum):
    KEY = 1,
    COLON = 2,
    VALUE = 3

class SJsonTransform:
    def __init__(self, src, dest):
        if os.path.isfile(src):
            self.src = src
        else:
            raise CsvError("file given as input does not exist")
        self.dest = dest
        self.state_stack = [ParseState.PARSE_TOP_ELEM]
        self.column_names = {}
        self.file_header = []
        self.last_col_ix = 0
        self.nest_level = 0
        self.out_line_list = [] # array used to re-order columns of
                                # output lines

    def parse_quoted_string(self, text):
        r = re.search('"(.*?[^\\\\])"', text)
        if r != None:
            array_elem = r.group(1)
            _, s_to = r.span()
            left = text[s_to:]
            return (array_elem, left)
        else:
            return (None, None)

    def parse_number(self, end_ix, text):
        value = None
        if end_ix == -1: #if delimiter_ix == -1 (not found) parse until end of line
            end_ix = len(text)
        try: # try parsing int
            value = int(text[:end_ix])
        except ValueError:
            try:
                value = float(text[:end_ix])
            except ValueError:
                pass
        if value == None:
            return (None, None)
        else:
            return (value, text[end_ix:])

    def parse_terminal(self, text, column_name, parsed_flag_stack, end_delim):
        # parse quoted string
        if text[0] == '"':
            elem, left_in_line = self.parse_quoted_string(text)
            if elem != None:
                self.set_column(column_name, elem)
                parsed_flag_stack[-1] = True
                return (left_in_line.strip(), "")
            else:
                err_msg = "scanning for end of string"
                self.state_stack[self.nest_level] = ParseState.MALFORMED
                return ("", err_msg)
        else: # parse number
            # perhaps comma is on the current line
            ix = text.find(",")
            if ix == -1: # if not comma, we could be at the end of array or dict
                ix = text.find(end_delim)
            value, left_in_line = self.parse_number(ix, text)
            if value != None:
                self.set_column(column_name, value)
                parsed_flag_stack[-1] = True # searching for comma
                return (left_in_line.strip(), "")
            else:
                err_msg = "parsing unquoted string or number"
                self.state_stack[self.nest_level] = ParseState.MALFORMED
                return ("", err_msg)


    def set_column(self, col_name, value):
        value_ix = self.column_names.get(col_name)

        if value_ix == None:
            self.column_names[col_name] = self.last_col_ix
            self.file_header.append(col_name)
            self.out_line_list.append(str(value))
            self.last_col_ix += 1
        else:
            self.out_line_list[value_ix] = str(value)

    def output_csv(self):
        with open(self.src, 'r') as in_file:
            with open(self.dest, 'w') as out_file:
                header_printed = False
                line_no = 0  # used in printing approximate line number for
                             # parsing errors
                last_col_ix = 0

                # parser state, all lists used as stacks
                current_key = []
                dict_parse_next = []
                dict_elem_parsed = []
                array_elem_parsed = []
                array_ix = []
                top_level_start = False
                # first loop takes care of providing the parser with text to
                # parse irrespective of line breaks in the input file
                for line in in_file:
                    line_no += 1
                    line = line.strip()
                    err_msg = ""
                    # second loop manages the actual parsing depending on the
                    # current state and the next characters; each character in
                    # the input is processed once
                    while line != "":
                        next_chr = line[0]

                        # Start state and output nesting level
                        if self.state_stack[self.nest_level] == ParseState.PARSE_TOP_ELEM:
                            if next_chr == '[':
                                self.state_stack.append(ParseState.PARSE_ARRAY_ITEMS)
                                array_elem_parsed.append(False)
                                array_ix.append(0)
                                top_level_start = True
                                self.nest_level += 1
                                line = line[1:] # consume start token
                            elif top_level_start == True:
                                if next_chr == ']':
                                    self.state_stack[self.nest_level] = ParseState.PARSE_END
                                    array_elem_parsed.pop()
                                    array_ix.pop()
                                    line = line[1:]
                                    # any further characters are considered spurious
                                else:
                                    self.state_stack[self.nest_level] = ParseState.MALFORMED
                                    err_msg = "Top-level array parsing error, expected comma or end-of-array"
                                    continue
                            else:
                                self.state_stack[self.nest_level] = ParseState.MALFORMED
                                err_msg = "Sjson files need to start with an array"
                                continue

                        # Parse Arrays
                        elif self.state_stack[self.nest_level] == ParseState.PARSE_ARRAY_ITEMS:
                            #TODO as part of project
                            pass

                        # Parse Dictionaries
                        elif self.state_stack[self.nest_level] == ParseState.PARSE_DICT_ITEMS:
                            #TODO as part of project
                            pass

                        # End States
                        elif self.state_stack[self.nest_level] == ParseState.MALFORMED:
                            raise SjsonError("Error when parsing line {} : {}".format(line_no, err_msg))
                        elif self.state_stack[self.nest_level] == ParseState.PARSE_END:
                            print("Spurious characters after end of top-line array, line {}".format(line_no))
                            break
                        line = line.strip()
                    if self.state_stack[self.nest_level] == ParseState.PARSE_END:
                        break

class SjsonError(Exception):
    def __init__(self, message):
        self.message = message

