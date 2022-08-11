# Discord Follow Bot
<div align="center">
    <a href="https://youtu.be/gkTb9GP9lVI"><img src="https://upload.wikimedia.org/wikipedia/en/9/9a/Trollface_non-free.png" width=128px alt="Discord Follow Bot" />
    <p><strong>We do a little trolling!</strong></p></a>
    <img src="https://github.com/gingerchicken/discfollow/actions/workflows/docker-image.yml/badge.svg" />
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT">
    <br>
    <img src="https://img.shields.io/badge/-Python-3776AB?style=flat&logo=Python&logoColor=white" />
    <ing src="https://img.shields.io/badge/-Docker-3776AB?style=flat&logo=Docker&logoColor=white" />
    <p><i>Automatically follow a specific user around every voice channel that they join</i></p>
</div>

## Disclaimer
> This bot is configured as a self-bot and is against the [Discord ToS](https://support.discord.com/hc/en-us/articles/115002192352-Automated-user-accounts-self-bots-).

## Usage

### Build
Firstly, you will need to build the docker image.

```bash
$ docker build . -t discfollow
```

### Get a token
> You will need to get your Discord Authentication Token, you shouldn't share this with anyone as this grants access to your entire account, this is why I recommend you read the source code of this application to ensure I am not stealing your token.

> In addition, please read the source code of [discord-py-self](https://github.com/dolfies/discord.py-self) to ensure they're not doing anything malicious either.

Now that the disclaimer is out of the way, you can get your token by following this [guide](https://discordpy-self.readthedocs.io/en/latest/token.html), or by putting the following JavaScript in your discord's console, ~~remember you should make sure what I am giving you here isn't malicious~~:

```javascript
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m => m?.exports?.default?.getToken).exports.default.getToken()
```

### Run
Finally you can run the bot using the following command:

```bash
$ docker run \
    -e TOKEN=blahblahblah \
    -e TARGET_ID=123456789012345678 \
    -e JOIN_DELAY=5 \
    -e LEAVE_DELAY=3 \
    discfollow
```

## Environment Variables
| Variable Name | Description |
| --------- | ----------- |
| `TOKEN` | Your [Discord Authentication Token](#get-a-token) |
| `TARGET_ID` | The Discord user ID of the user you want to follow, you can find those [here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-). |
| `JOIN_DELAY` | Delay (in seconds) before joining a chat |
| `LEAVE_DELAY` | Delay (in seconds) before leaving a chat |