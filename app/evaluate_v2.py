import json
import os
from typing import List, Union
import requests
from pydantic import BaseModel, Field
from fastapi import FastAPI
import uvicorn
import pandas as pd

class Query(BaseModel):
    query: str
    class_id: List[str]


class Class(BaseModel):
    class_id: str
    class_name: str
    class_description: str


class Options(BaseModel):
    multilabel: bool


class TextClassifierSpec(BaseModel):
    classes: List[Class]
    options: Options
    queries: List[Query]


def load_json_file(path: str) -> list | dict:
    with open(path, "r") as file:
        data = json.load(file)
    return data


def form_request(query: str, classes: List[Class], options: Options) -> dict:
    return {
        "query": query,
        "classes": [x.model_dump() for x in classes],
        "options": options.model_dump(),
    }


def make_request(payload: dict) -> dict:
    url = os.environ.get("SERVER_URL", "http://localhost:8000")
    response = requests.post(f"{url}/classify", json=payload)
    # print(f"response: {response.content}")
    return response.json()


def run_single_case(case: TextClassifierSpec) -> float:
    strict_mode = os.environ.get("STRICT_MODE", False)
    num_correct = 0
    results = []
    for query in case.queries:
        request = form_request(query.query, case.classes, case.options)
        result = make_request(request)
        predicted = result.get("result")
        correct_set = query.class_id
        correct = set(predicted) == set(correct_set)
        results.append(
            {'query':query.query,
             'predicted': predicted, 
             'correct':correct_set,
             'is_correct': correct
             }
             )
        if not correct and strict_mode:
            raise ValueError(f"Expected {query.class_id}, got {predicted}")

        if not correct:
            print(f"[INCORRECT] Expected {query.class_id}, got {predicted}")
        else:
            print(f"[CORRECT] Expected {query.class_id}, got {predicted}")

        num_correct += correct
    
    accuracy_single = num_correct / len(case.queries)
    df_results = pd.DataFrame(results,index=None)
    print(type(df_results),df_results)

    return accuracy_single, df_results


def iterate_test_cases(test_case_paths: list[str],return_results=False,) -> float:
    
    accuracies = []
    for test_case_path in test_case_paths:
        data = load_json_file(test_case_path)
        spec = TextClassifierSpec(**data)
        accuracy, results = run_single_case(spec)
        print(f"{test_case_path} accuracy: {accuracy * 100:.2f}%")
        accuracies.append(accuracy)
    accuracy_batch = sum(accuracies) / len(accuracies)
    if return_results:
        return accuracy_batch, results
    else:
        return accuracy_batch


def main():

    data_dir = "data"
    test_cases = [
        "case_test.json",
        # "case_1.json",
        # "case_2.json",
        # "case_3.json",
    ]
    test_cases = [os.path.join(data_dir, test_case) for test_case in test_cases]
    avg_acc = iterate_test_cases(test_cases)
    print(f"Average accuracy: {avg_acc * 100:.2f}%")


# Example usage:
if __name__ == "__main__":
    main()
