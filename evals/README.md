Evals:

To turn off evaluations, change the `"evaluation_toggle"` within `eval_config.json` to `false`.  

To add more evaluation metrics, create a Python file within `/metrics`. Ensure it has a `get_scores` method that takes `query`, `context`, and `output` and returns a Python dictionary of score names and their scores. Ensure score names do not overlap.

To change what score names are visible in the UI, add them to `scores` within `eval_config.json`. Ensure the names placed in the `scores` list are a perfect match to whatever scores are determined in files within `/metrics`.

Adding or removing scoring files from `/metrics` does not require restarting the server, but editing a file from `/metrics` does.