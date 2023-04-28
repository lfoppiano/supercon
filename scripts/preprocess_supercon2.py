import argparse
import csv
import json
import os
import re
from pathlib import Path

import requests
from pymatgen.core import Composition

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Preprocess SuperCon 2 extracted CSV")

    parser.add_argument("--input", help="Input SuperCon 2 CSV file", required=True)
    parser.add_argument("--output", help="Output directory", required=True)

    args = parser.parse_args()

    input_file = args.input
    output = args.output

    # formula_parser_url = "https://lfoppiano-grobid-superconductors-tools.hf.space/convert/formula/composition"
    # formula_parser_url = "http://falcon.nims.go.jp/material/nlp/stable/convert/formula/composition"
    normalisation_url = "http://localhost:8060/service/parseMeasure"
    quantity_text_url = "http://localhost:8060/service/processQuantityText"

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
                    header.insert(header.index("criticalTemperature")+1, "criticalTemperatureUnit")
                    header.insert(header.index("appliedPressure")+1, "appliedPressureUnit")
                    fw.writerow(header)
                    first = False
                    continue

                # Check formulas
                formula = line[header.index("formula")]

                if formula:
                    try:
                        line[header.index("formula")] = str(Composition(formula).get_reduced_formula_and_factor()[0])
                    except:
                        continue
                else:
                    continue


                tc = line[header.index("criticalTemperature")]

                if tc:
                    temp_regex = re.compile(r"^([0-9.]+) ?(m?K{1})$")
                    found = temp_regex.search(tc)
                    if found:
                        value = found.groups()[0]
                        unit = found.groups()[1]

                        data = json.dumps({'from': value, 'type': "temperature", 'unit': unit})
                        response = requests.post(quantity_text_url, data=data)

                        if response.status_code == 200:
                            parsed_response = json.loads(response.text)

                            normalized_quantity = parsed_response['measurements'][0]['quantity']['normalizedQuantity']
                            normalized_unit = parsed_response['measurements'][0]['quantity']['normalizedUnit']['name']


                            try:
                                float_value = float(normalized_quantity)
                            except:
                                continue

                            if float_value > 300 and float_value < 500:
                                print("Tc value", float_value, "between 300 and 500 K, we report and skip. ")
                                continue
                            elif float_value >= 500.0:
                                # print("Tc value", float_value, "above 500 K, we report and skip. ")
                                continue
                            elif value.startswith("-"):
                                continue

                            line[header.index("criticalTemperature")] = float_value
                            line.insert(header.index("criticalTemperature")+1, normalized_unit)
                        else:
                            continue

                    else:
                        continue

                else:
                    continue

                applied_pressure = line[header.index("appliedPressure")]

                if applied_pressure:
                    temp_regex = re.compile(r"^([0-9.]+) ?(.?(Pa){1})$")
                    found = temp_regex.search(tc)
                    if found:
                        value = found.groups()[0]
                        unit = found.groups()[1]

                        data = json.dumps({'from': value, 'type': "pressure]", 'unit': unit})
                        response = requests.post(normalisation_url, data=data)

                        if response.status_code == 200:
                            parsed_response = json.loads(response.text)

                            normalized_quantity = parsed_response['measurements'][0]['quantity']['normalizedQuantity']
                            normalized_unit = parsed_response['measurements'][0]['quantity']['normalizedUnit']['name']


                            try:
                                float_value = float(normalized_quantity)
                            except:
                                continue

                            if value.startswith("-"):
                                continue

                            line[header.index("appliedPressure")] = float_value
                            line.insert(header.index("appliedPressureUnit"), normalized_unit)

                    else:
                        line.insert(header.index("appliedPressureUnit"), "")

                else:
                    line.insert(header.index("appliedPressureUnit"), "")


                fw.writerow(line)