
import os
from .csv_transform import *
from .sjson_transform import *

class CliCommon:
    def run(src, dest, column_spec):
        _, src_ext = os.path.splitext(src)
        if src_ext == '.csv':
            try:
                tr = CsvTransform(src, dest, column_spec)
                tr.output_reordered()
            except CsvError as e:
                print("Could not perform the csv transform: " + e.message )
            return
        if src_ext == '.sjson':
            try:
                trsj = SJsonTransform(src, dest)
                trsj.output_csv()
            except SjsonError as e:
                print("Could not perform the csv transform: " + e.message )
            return
        # error case, unsupported input format
        print("Error: unsupported input format, can only process files with a "+
              ".csv or .sjson extension")

