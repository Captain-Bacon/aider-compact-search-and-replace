# Aider

Aider is a command-line tool that allows you to chat with GPT-4 about your code.
Aider will directly edit your source files as directed by the GPT-4 chat, and commit those changes to your local git repo.
Each change is automatically committed to git with a sensible commit message.
This makes it easy and safe for aider to help you code.

[![asciicast](https://asciinema.org/a/eDDqO3PlqH4lUBBXnLlMG7l2x.svg)](https://asciinema.org/a/eDDqO3PlqH4lUBBXnLlMG7l2x)

## Features

* Chat with GPT-4 about your code by launching aider with set of source files to discuss and edit together.
* Request changes, improvements, and bug fixes to your code.
* Aider will apply the edits suggested by GPT-4 directly to your source files.
* Aider will automatically commit each changeset to your local git repo with a sensible commit message. These frequent, automatic commits provide a safety net. It's easy to undo aider's changes or use standard git workflows to manage longer sequences of changes.
* Aider can review multiple source files at once and make coordinated code changes across all of them in a single changeset/commit.
* Aider knows about all the files in your repo, so it can ask for permission to review whichever files seem relevant to your requests.
* You can also edit the files in your editor while chatting with aider.
  * Aider will notice if you edit the files outside the chat.
  * It will help you commit these out-of-band changes, if you'd like.
  * It will bring the updated file contents into the chat.
  * You can bounce back and forth between the aider chat and your editor, to fluidly collaborate.
* Live, colorized, human friendly output.
* Readline style chat input history, with autocompletion of code tokens found in the source files being discussed (via `prompt_toolkit` and `pygments` lexers)

## Installation

1. Install the package: `pip install git+https://github.com/paul-gauthier/aider.git`
2. Set up your OpenAI API key as an environment variable `OPENAI_API_KEY` or by including it in a `.env` file.

## Usage

Run the aider tool by executing the following command:

```
aider <file1> <file2> ...
```

Replace `<file1>`, `<file2>`, etc., with the paths to the source code files you want to work on. These files will be added to the chat session.

You can also just launch `aider` anywhere in a git repo without naming files on the command line.
It will discover all the files in the repo.
You can then add and remove individual files in the chat session with the `/add` and `/drop` chat commands described below.

You can also use additional command-line options to customize the behavior of the tool. The following options are available, along with their corresponding environment variable overrides:

- `--history-file HISTORY_FILE`: Specify the chat input history file (default: .aider.history). Override the default with the environment variable `AIDER_HISTORY_FILE`.
- `--model MODEL`: Specify the model to use for the main chat (default: gpt-4). Override the default with the environment variable `AIDER_MODEL`.
- `-3`: Use gpt-3.5-turbo model for the main chat (basically won't work). No environment variable override.
- `--no-pretty`: Disable pretty, colorized output. Override the default with the environment variable `AIDER_PRETTY` (default: 1 for enabled, 0 for disabled).
- `--show-diffs`: Show diffs when committing changes (default: False). Override the default with the environment variable `AIDER_SHOW_DIFFS` (default: 0 for False, 1 for True).

For more information, run `aider --help`.

## Chat commands

Aider supports the following commands from within the chat:

* `/add <file>`: Add matching files to the chat session.
* `/drop <file>`: Remove matching files from the chat session.
* `/ls`: List all known files and those included in the chat session.
* `/commit [message]`: Commit outstanding changes to the chat session files. Use this to commit edits you made outside the chat, with your editor or git commands. Aider will provide a commit message if you don't.
* `/undo`: Undo the last git commit if it was done by aider.
* `/diff`: Display the diff of the last aider commit.

To use a command, simply type it in the chat input followed by any required arguments.

## Tips

* Large changes are best performed as a sequence of bite sized steps. Same as if you were undertaking them by yourself.
* Use Control-C to safely interrupt aider if it isn't providing a useful response. The partial response remains in the conversation, so you can refer to it when you reply with more information or direction.
* Enter a multiline chat message by entering `{` alone on the first line. End the multiline message with `}` alone on the last line.
* If your code is throwing an error, paste the error message and stack trace into aider as a multiline `{}` message and let aider fix the bug.
* GPT-4 knows about a lot of standard tools and libraries, but may get some of the fine details wrong about APIs and function arguments. You can paste doc snippets into the chat with the  multiline `{}` syntax.
* Aider will notice if you launch it on files with uncommitted changes and offer to commit them before proceeding.
* Aider can only see the content of the files you specify, but it also gets a list of all the files in the repo. It may ask to see additional files if it feels that's needed for your requests.

## Limitations

Aider basically requires GPT-4.
You can invoke it with `aider -3` to try using gpt-3.5-turbo, but it will almost certainly fail to function correctly.
GPT-3.5 is unable to consistently follow directions to generate concise code edits in a stable, parsable format.

Aider can only edit code that fits in the GPT context window.
For GPT-4 that is 8k tokens.
It helps to be selective about which of your source files you discuss with aider at the same time.
It can also help to refactor your code into more, smaller files.
Aider can help perform such refactorings, if you start before the files get too large.

If you have access to gpt-4-32k, I would be curious to hear how it works with aider.
