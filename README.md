PhraseTelebot
=========

PhraseBot is a Telegram Bot that send audio phrases. It's intended for being part of a group.
There are 2 operating modes: you can request a phrase using `/say` and the bot can send by himself a phrase when a mention
word appear on the sentences of other users. In this case, it will send a phrase taking into account the words in that sentence.

Commands supported
------------------
Currently, it supports this commands:
- `/say [ID]`: send the phrase with that id. If not id is provided it will pick a random one
- `/list`: list all the phrases
- `/top`: most popular phrases

Also, the bot will read all the messages sent to a group and if any of the words are in the `mention words`
 list, it will send a phrase related to the words in that sentence. If there are any word in the sentence that appears
 in the keywords of the phrases it will pick one of these. In other case, it will pick a random phrase.

Description file
----------------
The description file describes the dataset and the audio phrases.
- `path`: the folder where are the files.
- `mention_words`: the words to which will respond and will send a phrase
- `data`: the audio phrases. The key is the name of the audio file.
    - `title`: title of the phrase
    - `keywords`: keywords used to select phrase candidates to respond a mention

Configuration
-------------
The first step is to [create a bot](https://core.telegram.org/bots#botfather) using [BotFather](https://telegram.me/botfather).
Then, disable privacy mode (to work looking for mention words) with `/setprivacy` command.
Finally, copy the given token to `config.py`.

Now we need to create the phrase dataset:
1. Put all your audio files in a folder, default folder is `data/`.
Files must be `.ogg` extension (you can use <http://media.io/> to convert them)
2. (Optional) Run script `script_utils/rename_files.py` with the dataset folder as argument to rename files.
3. Run script `script_utils/create_description_file.py` with the dataset folder as argument. It will create in the same
directory the description file template describing the dataset. Put the path of the description file in `config.py`
4. Complete the information in the description file.
5. Start the bot and enjoy. ;)




