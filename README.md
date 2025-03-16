<h1 align="center">Telegram File Stream Bot</h3>
<p align="center">
  <a href="https://github.com/DeekshithSH/FileStreamBot">
    <img src="https://socialify.git.ci/DeekshithSH/FileStreamBot/image?description=1&font=Source%20Code%20Pro&forks=1&issues=1&pattern=Charlie%20Brown&pulls=1&stargazers=1&theme=Dark" alt="FileStreamBot" width="640" height="320" />
  </a>
  <p align="center">
    A Telegram bot to stream files to web<br/>
    <a href="https://telegram.dog/DirectLinkGenerator_Bot"><strong>Demo Bot (Not Available)»</strong></a>
    <br />
    <a href="https://github.com/DeekshithSH/FileStreamBot/issues">Report a Bug</a>
    |
    <a href="https://github.com/DeekshithSH/FileStreamBot/issues">Request Feature</a>
  </p>
</p>

<hr>
Checkout <a href="https://github.com/SpringsFern/TG-FileStreamBot/tree/main">Readme</a> for more information
<hr>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-this-bot">About this Bot</a>
      <ul>
        <li><a href="#original-repository">Original Repository</a></li>
      </ul>
    </li>
    <li>
      <a href="#how-to-make-your-own">How to make your own</a>
      <ul>
        <li><a href="#host-it-on-vps-or-locally">Run it in a VPS / local</a></li>
      </ul>
    </li>
    <li><a href="#setting-up-things">Setting up things</a></li>
    <ul>
      <li><a href="#mandatory-vars">Mandatory Vars</a></li>
      <li><a href="#optional-vars">Optional Vars</a></li>
    </ul>
    <li><a href="#how-to-use-the-bot">How to use the bot</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact-me">Contact me</a></li>
    <li><a href="#credits">Credits</a></li>
  </ol>
</details>

## About This Bot

<p align="center">
    <a herf="https://github.com/DeekshithSH/FileStreamBot">
        <img src="https://telegra.ph/file/a8bb3f6b334ad1200ddb4.png" height="100" width="100" alt="Telegram Logo">
    </a>
</p>
<p align='center'>
    This bot will give you stream links for Telegram files without the need of waiting till the download completes
</p>

### Original Repository
[TG-FileStreamBot](https://github.com/SpringsFern/TG-FileStreamBot) is a Modified Version of [TG-FileStreamBot](https://github.com/EverythingSuckz/TG-FileStreamBot) by [EverythingSuckz](https://github.com/EverythingSuckz/)

The main working part was taken from [Tulir Asokan's](https://github.com/tulir) [tg filestream](https://bit.ly/tg-stream). Thanks to them for their awesome projects

## How to make your own

<!-- Host the bot on VPS or Locally -->

### Deploy on Heroku

Press the below button to fast deploy to Heroku

- [![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

then goto the <a href="#mandatory-vars">variables tab</a> for more info on setting up environmental variables.

### Host it on VPS or Locally

```sh
git clone https://github.com/SpringsFern/TG-FileStreamBot
cd TG-FileStreamBot
python3 -m venv ./venv
. ./venv/bin/activate
pip3 install -r requirements.txt
python3 -m WebStreamer
```

and to stop the whole bot,
 do <kbd>CTRL</kbd>+<kbd>C</kbd>

- **If you wanna run this bot 24/7 on the VPS, follow these steps.**
```sh
sudo apt install tmux -y
tmux
python3 -m WebStreamer
```

now you can close the VPS and the bot will run on it.

## Setting up things

If you're on Heroku, just add these in the Environmental Variables
or if you're Locally hosting, create a file named `.env` in the root directory and add all the variables there.
An example of `.env` file:

```sh
API_ID=452525
API_HASH=esx576f8738x883f3sfzx83
BOT_TOKEN=55838383:yourtbottokenhere
BIN_CHANNEL=-100
FQDN=192.168.27.1
HAS_SSL=False
MULTI_TOKEN1=55838383:yourfirstmulticlientbottokenhere
MULTI_TOKEN2=55838383:yoursecondmulticlientbottokenhere
MULTI_TOKEN3=55838383:yourthirdmulticlientbottokenhere
PORT=8080
```

### Mandatory Vars

`API_ID` : Goto [my.telegram.org](https://my.telegram.org) to obtain this.

`API_HASH` : Goto [my.telegram.org](https://my.telegram.org) to obtain this.

`BOT_TOKEN` : Get the bot token from [@BotFather](https://telegram.dog/BotFather)

`BIN_CHANNEL` : Create a new channel (private/public), post something in your channel. Forward that post to [@missrose_bot](https://telegram.dog/MissRose_bot) and **reply** `/id`. Now copy paste the forwarded channel ID in this field. 

### For MultiClient

`MULTI_TOKEN1`: Add your first bot token here.

`MULTI_TOKEN2`: Add your second bot token here.

you may also add as many as bots you want. (max limit is not tested yet)
`MULTI_TOKEN3`, `MULTI_TOKEN4`, etc.



### Optional Vars

`ALLOWED_USERS`:  A list of user IDs separated by comma (,). If this is set, only the users in this list will be able to use the bot.

> **Note**
> Leave this field empty and anyone will be able to use your bot instance.

`CHUNK_SIZE`: Size of the chunk to request from Telegram server when streaming a file [See more](https://core.telegram.org/api/files#downloading-files)

`CONNECTION_LIMIT`:  (default 20) - The maximum number of connections to a single Telegram datacenter.

`CUSTOM_URL`: Only set this true if you set `LINK_TEMPLATE` field

`FQDN` :  A Fully Qualified Domain Name if present. Defaults to `WEB_SERVER_BIND_ADDRESS`

`HAS_SSL` : (can be either `True` or `False`) If you want the generated links in https format.

`KEEP_ALIVE` : If you want to make the server ping itself every

> [!WARNING]
> `LINK_TEMPLATE`: Modify format in which download links are generated
> **Ignore this field**
> <details>
> <summary>[Expand]</summary>
>   This setting allows customization of how the download link is displayed to users. It does **not** affect the actual link used by the bot to fetch the file—only the visible link format changes.  
> 
> You can customize the link format using placeholders that will be replaced with actual values when generating the link. Available placeholders:  
> - `{url}` – The base URL (`CUSTOM_URL`) where the file is hosted.  
> - `{name}` – The file name (URL-encoded).  
> - `{size}` – The file size in human-readable format.  
> - `{id}` – The unique ID of the file message.  
> - `{mime}` – The file's MIME type (URL-encoded).  
> - `{time}` – The Unix timestamp when the link is generated.  
> 
> Example customization:  
> ```
> LINK_TEMPLATE = "{url}/download/{id}/{name}?size={size}&type={mime}"
> ```
> This will generate a link like:  
> ```
> https://yourdomain.com/download/12345/sample.pdf?size=2MB&type=application/pdf
> ```
> </details>
<br>

`NO_PORT` : (can be either `True` or `False`) If you don't want your port to be displayed. You should point your `PORT` to `80` (http) or `443` (https) for the links to work. Ignore this if you're on Heroku.

`NO_UPDATE` if set to `true` bot won't respond to any messages

`PING_INTERVAL` : The time in seconds you want the servers to be pinged each time to avoid sleeping (Only for Heroku). Defaults to `600` or 10 minutes.

`PORT` : The port that you want your webapp to be listened to. Defaults to `8080`

`REQUEST_LIMIT`: (default 5) - The maximum number of requests a single IP can have active at a time

`SLEEP_THRESHOLD` : Set a sleep threshold for flood wait exceptions happening globally in this telegram bot instance, below which any request that raises a flood wait will be automatically invoked again after sleeping for the required amount of time. Flood wait exceptions requiring higher waiting times will be raised. Defaults to 60 seconds.

`TRUST_HEADERS`: (defaults to true) - Whether or not to trust X-Forwarded-For headers when logging requests.

`UPDATES_CHANNEL` : Your Telegram Channel Username without @

`WEB_SERVER_BIND_ADDRESS` : Your server bind address. Defauls to `0.0.0.0`

## How to use the bot

:warning: **Before using the  bot, don't forget to add all the bots (multi-client ones too) to the `BIN_CHANNEL` as an admin**
 
`/start` : To check if the bot is alive or not.

To get an instant stream link, just forward any media to the bot and boom, its fast af.

## faQ

- How long the links will remain valid or is there any expiration time for the links generated by the bot?
> The links will will be valid as longs as your bot is alive and you haven't deleted the log channel.

## Contributing

Feel free to contribute to this project if you have any further ideas

## Contact me

[![Telegram Channel](https://img.shields.io/static/v1?label=Join&message=Telegram%20Channel&color=blueviolet&style=for-the-badge&logo=telegram&logoColor=violet)](https://xn--r1a.click/SpringsFern)
[![Telegram Group](https://img.shields.io/static/v1?label=Join&message=Telegram%20Group&color=blueviolet&style=for-the-badge&logo=telegram&logoColor=violet)](https://xn--r1a.click/AWeirdString)

You can contact either via my [Telegram Group](https://xn--r1a.click/AWeirdString)


## Credits

- [Me](https://github.com/DeekshithSH)
- [EverythingSuckz](https://github.com/EverythingSuckz) for his [TG-FileStreamBot](https://github.com/EverythingSuckz/TG-FileStreamBot)
- [Tulir Asokan](https://github.com/tulir) for his [tg filestream](bit.ly/tg-stream)
- [eyaadh](https://github.com/eyaadh) for his awesome [Megatron Bot](https://github.com/eyaadh/megadlbot_oss).
- [BlackStone](https://github.com/eyMarv) for adding multi-client support.
- [Lonami](https://github.com/Lonami) for his [Telethon Library](https://github.com/LonamiWebs/Telethon)
- [TheHamkerCat](https://github.com/TheHamkerCat) for helping me with my common doubts.
