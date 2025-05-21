# NekoBot2

The following was written/edited using AI

## Overview
NekoBot2 is a Discord bot project. This README provides basic setup instructions to get the bot running locally. For detailed information on deploying a bot to a Discord server (guild), please refer to the [official Discord bot documentation](https://discord.com/developers/docs/intro).

## Prerequisites
- Python 3.8 or higher
- [pip](https://pip.pypa.io/en/stable/)

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd nekobot2
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Create a `.env` file in the root directory of the project.
   - Add your Discord bot token to the `.env` file:
     ```env
     DISCORD_TOKEN=your-bot-token-here
     ```
   - You can find or create your bot token by following the [official Discord bot setup guide](https://discord.com/developers/docs/intro).

4. **Run the bot**
   - Start the bot using the following command:
     ```sh
     python nekobot2/main.py
     ```

## Additional Resources
- [Official Discord Bot Documentation](https://discord.com/developers/docs/intro)

## Notes
- Make sure your bot is invited to your Discord server and has the necessary permissions.
- For advanced configuration, refer to the `config/config.yaml` file.
