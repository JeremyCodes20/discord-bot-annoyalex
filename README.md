# AnnoyAlex Discord Bot

Simple and stupid Discord bot with the initial intention of annoying a friend.

### Features:

* Send an image whenever a particular person sends a message 
* Play an intro/outro sound whenever you enter/exit a voice channel
* Play an additional outro sound by using the command `<command_prefix>outro`

### Config:

Audio/image file paths are specified in `config.json`. Which users the intro/outro/annoying image should apply to are also specified, as well as the discord client token. You can also customize what the prefix for this bot's commands should be.

An example [config.sample.json](config.sample.json) file is provided as a template. 