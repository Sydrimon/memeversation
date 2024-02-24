# memeversation
enrich your telegram conversation with gifs
the bot reacts to key words and sends gifs into the chat


## How to add gifs
open python shell in project root
```
from memeversation import Memeversation
m = Memeversation()
m.gif_data['buzzword'] = 'link-to-gif'
m.write_data_file()
```
