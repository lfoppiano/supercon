import argparse
import csv
import json
import os
from pathlib import Path

import requests
from pymatgen.core import Composition

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Cleanup SuperCon 2 extracted CSV")

    parser.add_argument("--input", help="Input CSV file", required=True)
    parser.add_argument("--output", help="Output directory", required=True)

    args = parser.parse_args()

    input_file = args.input
    output = args.output

    # formula_parser_url = "https://lfoppiano-grobid-superconductors-tools.hf.space/convert/formula/composition"
    formula_parser_url = "http://falcon.nims.go.jp/material/nlp/stable/convert/formula/composition"


    output_path = Path(output)
    if os.path.isdir(str(output)):
        output_path = os.path.join(output, Path(input_file).stem, "csv")

    with open(output_path, encoding="utf-8", mode='w') as fo:
        fw = csv.writer(fo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        with open(input_file, encoding="utf-8-sig") as f:
            first = True
            csvreader = csv.reader(f, delimiter=",")
            for line in csvreader:
                if len(line) == 0:
                    continue
                if first:
                    header = line
                    header.insert(5, "parsed_formula")
                    header.insert(6, "formatted_formula")
                    fw.writerow(header)
                    first = False
                    continue

                # Check formulas
                formula = line[header.index("formula")]

                if formula:
                    data = {'input': formula}
                    response = requests.post(formula_parser_url, data=data)

                    if response.status_code != 200:
                        if response.status_code == 400:
                            print("Invalid formula")
                        else:
                            print("Other errors")
                    else:
                        if response.text == "{}":
                            print("Invalid formula")
                            continue

                        print("OK")
                        comp = json.loads(response.text)['composition']

                        result = ''
                        for key, value in comp.items():
                            if value == '1':
                                result += key + ' '
                            else:
                                result += key + value + ' '

                        line.insert(header.index("parsed_formula"), comp)
                        line.insert(header.index("formatted_formula"), result)
                        # Composition(formula).get_reduced_formula_and_factor()
                        fw.writerow(line)
                else:
                    print("No formula - forward to output")
                    line.insert(header.index("parsed_formula"), "")
                    line.insert(header.index("formatted_formula"), "")
                    fw.writerow(line)

                # TBD: Check Tc < room temperature
