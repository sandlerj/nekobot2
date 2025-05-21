# Nekobot

## Description
A Discord bot that sends catgirls and anime gifs. The bot will integrate into Discord chat and post anime pictures and gifs in response to keywords and phrases in messages sent by other users in the server. The intent is that the gifs used provide occasional commedic relief and humor in the chat without distracting too much from the topic at hand.

## Requirements
- Discord bot should use Discord's official API for Discord Bot
- Bot should send anime gifs and images in response to configurable keywords which indicate action or emotions.
- The bot will not have its own database or repository for storing images. Images and gifs sent should be pulled from an external repository, API, or the web. 
- Images should not be AI generated.
- The bot should have a configurable cooldown between messages in order to prevent spamming.

## Non-Functional Requirements
- Bot should be written in Python
- Bot should prioritize free APIs and resources in order to reduce costs.
- For development stages, bot can run on a local machine. Deployment to a production environment should be broken into a separate milestone.