# 5D Take Home Technical Test

## Specification

Your task is to build a simple web application to do text classification using a large language model. `gpt-3.5-turbo` will be sufficient for the task and should incur minimal cost. The main endpoint for your classification will be a POST request to `/classify`. The JSON payload will have the following structure:

```json
{
    "query": "the text to be classified",
    "options": {
      "multilabel": true,
      "show_reasoning": true
    },
    "classes": [
        {
            "class_id": "C1",
            "class_name": "Class 1",
            "class_description": "Description of class 1"
        },
        {
            "class_id": "C2",
            "class_name": "Class 2",
            "class_description": "Description of class 2"
        }
    ]
}

```

Your web app should return a JSON dictionary with the following structure:

```json
{
    "result": ["{THE CLASSIFICATION RESULT CLASS ID}"],
    "reasoning": "The reasoning behind the classification"
}
```

If `multilabel` is `true`, then the "result" field can have more than one option. If "show_reasoning" is `true`, then the "reasoning" field should be included in the response. If "show_reasoning" is `false` or not included, then the "reasoning" field should be `null`.

## Evaluation

Included in the repo alongside this README is the script we will run to evaluate your web app (`evaluate.py`). Some example test data is also included - we will run this and a held out test set through your app and compare it to our own implementation. Our implementation uses `gpt-3.5-turbo`, and you should too. Using a more powerful model for better results will count against you - **we are much more interested in the approach you take with your code than the actual results.**

Feel free to include anything else in the deliverable that could help us approach it as a newbie, much like how you’d do it in a usual work setting.

## Submission

Please submit your code as a zip file or a link to a private repository. If you choose to submit a zip file, please ensure that it is named `5D_Take_Home_Technical_Test.zip`.

## What We Like To See

- Clean, well-structured code
- Tests! We love tests
- Your own flair - if you want to add extra features or functionality, feel free to do so, and see the stretch goals for inspiration

## Stretch Goals

If you have time or would like to, here are some stretch goals you could consider:

- Dockerize your app
- Deploy it somewhere and send us the link
- Add security measures of some kind
- Write a simple client library which can extract text from PDFs and send it to your app
- Add a function to the client library which opens URLs, scrapes the text from them, and sends it to your app
- Add extra optional metadata such as `temperature` and `model_name`
- Other common sense API goodies
- Other endpoints to accomplish different tasks with LLMs
- Add caching
- Make a simple frontend