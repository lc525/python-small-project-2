import os.path

class CsvTransform:
    def __init__(self, src, dest, column_spec):
        if os.path.isfile(src):
            self.src = src
        else:
            raise CsvError("file given as input does not exist")
        self.dest = dest
        # filter column_spec so it contains only valid values
        with open(self.src, 'r') as in_file:
            header = in_file.readline()
            header_elem = header.split(",")
            self.column_spec = [ix for ix in column_spec if ix > 0 and ix <= len(header_elem)]

    def output_reordered(self):
        with open(self.src, 'r') as in_file:
            with open(self.dest, 'w') as out_file:
                for line in in_file:
                    out_line = ""
                    line_elem = line.rstrip('\n').split(',')
                    for cs_pos, ix in enumerate(self.column_spec):
                        out_line += line_elem[ix-1]
                        if cs_pos < len(self.column_spec) - 1 :
                            out_line += ","
                    out_file.write(out_line + '\n')

class CsvError(Exception):
    def __init__(self, message):
        self.message = message

