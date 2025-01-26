__version__ = "0.1.0"

def prompt_openai(message: str, model="gpt-4o-2024-08-06", image=None):
    """A prompt helper function that sends a message to openAI
    and returns only the text response.
    """
    # convert message in the right format if necessary
    import openai
    import warnings

    client = openai.OpenAI()

    if image is not None:
        warnings.warn("Images are not supported and thus, ignored.")

    message = [{"role": "user", "content": message}]

    print("model", model[1:])

    # submit prompt
    response = client.chat.completions.create(
        model=model,
        messages=message
    )

    return response.choices[0].message.content


def answer_issue(repository, issue, prompt_function, **kwargs):
    """Answer an issue on GitHub."""
    from github import Github
    import os
    access_token = os.getenv('GITHUB_API_KEY')

    # Create a PyGithub instance using the access token
    g = Github(access_token)

    # Get the repository object
    repo = g.get_repo(repository)
    issue_obj = repo.get_issue(issue)

    # Get all comments on the issue
    comments = list(issue_obj.get_comments())

    # return last comment
    if len(comments) > 0:
        comment = comments[-1]
        text = comment.body
    else:
        text = issue_obj.body

    if text is None:
        raise("Issue/comment didn't contain any text.")

    response = prompt_function(f"""
Answer to the following message:
    
{text}
""")

    issue_obj.create_comment(response)

