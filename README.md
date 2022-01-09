# SocialCreditDiscordBot
Invite bot: https://discord.com/api/oauth2/authorize?client_id=929366527352905768&permissions=8&scope=bot
# Usage
"::sc (name)": check someone social credit (Ex: ::sc @user)<br>
"::sc (name) (point) reason:(reason)": add or reduce social credit (Ex: ::sc @user +10 reason:test)<br>
"::muterole (role's name)": set muted role (Ex: ::muterole Muted)<br>
# How it works
When someone's social credit is below 0, the user will be muted for abs(credit) minute(s) (Ex: @user has -10 credit so @user will be muted for 10 minutes)<br>
When muted time is over, the user's social credit is not reset
