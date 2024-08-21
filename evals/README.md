Evals:

To turn off evaluations, change the `"evaluation_toggle"` within `eval_config.json` to `false`.  

To add more evaluation metrics, create a Python file within `/metrics`. Ensure it has a `get_scores` method that takes `query`, `context`, and `output` and returns a Python dictionary of score names and their scores.

To change what score names are visible in the UI, add them to `scores` within `eval_config.json`.

Adding or removing scoring files from `/metrics` does not require restarting the server, but editing a file from `/metrics` does.