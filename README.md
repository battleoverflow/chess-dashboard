# Chess.com Dashboard

Monitor your chess.com information locally in a Flask dashboard

The design isn't too great, but it should pull some interesting information. I've only spent about an hour on this so far, but I may revisit it in the future

## Usage

Make sure you have all the proper tools installed:

```bash
pip install flask
```

Now just run the following command to start the dashboard on port `localhost:5000`:

```bash
flask run
```

### How do I change to my username?

I may eventually include a form on the front end to allow users to input their usernames, but for now, it's just an environment variable to make everything easier

```
username=<YOUR_USERNAME>
```

## Why?

I recently learned that chess.com has an API and wanted to mess around with it. Feel free to open a PR if you have improvements or submit an issue if something is broken
