"""Access rasa test results and assign pass/fail based on adjustable threshold."""
import sys
import json
import argparse
import pandas as pd
from typing import Text, Dict, Any

parser = argparse.ArgumentParser()

parser.add_argument("-entity_thresh", type=float, help="Acceptance threshold for entity recognition pass", default=0.80)
parser.add_argument("-intent_thresh", type=float, help="Acceptance threshold for intent classification pass", default=0.80)
parser.add_argument("-response_thresh", type=float, help="Acceptance threshold for response selection pass", default=0.80)
parser.add_argument("-reg_thresh", type=float, help="Acceptance threshold for f1 regression", default=0)

args = parser.parse_args()

entity_path = './results/DIETClassifier_report.json'
entity_gold_path = './tests/DIETClassifier_report_GOLD.json'
intent_path = './results/intent_report.json'
intent_gold_path = './tests/intent_report_GOLD.json'
response_path = './results/response_selection_report.json'
response_gold_path = './tests/response_selection_report_GOLD.json'


def analyze_results(sys: Dict[Text, Any], gold: Dict[Text, Any], thresh: float, test_type: Text, fout: Any) -> int:
    """Gather scores and compare sys to gold results. Output regression table and any failures.

    Args:
        sys: results pulled from rasa report.json file
        gold: results from gold standard rasa report file
        thresh: The passing threshold for each item
        test_type: The name of the type of results {Entity recognition, Intent classification, Response Selection}
        fout: file object to write results to

    Return:
        int: 1 failure; raise exit code one. 0 pass; raise exit code 0

    """
    fails = []
    regression_flag = 0

    sys_scores = []
    counter = 0
    for k, v in sys.items():
        try:
            sys_scores.append((f"{counter}. {k[:20]}", '%.4f' % (v['f1-score']), '%.4f' % (gold[k]['f1-score'])))
            counter += 1
        except Exception:
            pass
    regression_df = pd.DataFrame(index=[x[0] for x in sys_scores], columns=['GOLD', 'SYSTEM', 'RESULT'])
    for s in sys_scores:
        if float(s[1]) < thresh:
            fails.append((str(s[0]), str(s[1])))
        regression_df.at[s[0], 'SYSTEM'] = s[1]
        regression_df.at[s[0], 'GOLD'] = s[2]
        if float(s[2]) - float(s[1]) > args.reg_thresh:
            regression_df.at[s[0], 'RESULT'] = 'FAIL'
            regression_flag = 1
        else:
            regression_df.at[s[0], 'RESULT'] = 'OK'

    if not fails and not regression_flag:
        fout.write(f"{test_type.upper()}: PASS\n")
        print(f"{test_type}: PASS")
        fout.write('Regression check:\n')
        fout.write(regression_df.to_string())
        fout.write('\n\n\n')
        return 0
    else:
        fout.write(f"{test_type.upper()}: FAIL\n\n")
        print(f"{test_type}: FAIL")
        fout.write("Threshold check:\n")
        for f in fails:
            fout.write(f[0] + '\t' + f[1] + '\tFAIL\n\n')
        fout.write('Regression check:\n')
        fout.write(regression_df.to_string())
        fout.write('\n\n\n')
        return 1


def main():
    """Read in gold and sys results files and output summary."""
    with open("./tests/RESULT_SUMMARY.txt", "w") as fout:
        results = []
        try:
            entity = json.load(open(entity_path))
            entity_gold = json.load(open(entity_gold_path))
            results.append(analyze_results(entity, entity_gold, args.entity_thresh, 'Entity Recognition', fout))

            intent = json.load(open(intent_path))
            intent_gold = json.load(open(intent_gold_path))
            results.append(analyze_results(intent, intent_gold, args.intent_thresh, 'Intent Classification', fout))

            response = json.load(open(response_path))
            response_gold = json.load(open(response_gold_path))
            results.append(analyze_results(response, response_gold, args.response_thresh, 'Response Selection', fout))
        except Exception as e:
            print('There was an error opening the files')
            print(e)

        if 1 in results:
            sys.exit(1)
        else:
            sys.exit(0)


if __name__ == '__main__':
    main()
