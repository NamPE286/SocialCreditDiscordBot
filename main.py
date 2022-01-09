import discord
import os
import asyncio
from replit import db
from keep_alive import keep_alive

keep_alive()
client = discord.Client()
global i2
global muterole
i2 = 0
print(db.keys())

def getUID(s):
  global i2
  i1 = 0
  i2 = 0
  for i in range(len(s)):
    if s[i] == '<':
      if s[i + 2] == '!' or s[i + 2] == '&':
        i1 = i + 3
        i1 = i + 3
      else:
        i1 = i + 2
    elif s[i] == '>':
      i2 = i
  uid = int(s[i1:i2])
  return uid

@client.event
async def on_ready():
  print('Logged in')
@client.event
async def on_message(message):
  global muterole
  socialCredit = 0
  sid = message.guild.id
  channel = client.get_channel(message.channel.id)
  #check if user is a mod
  isAdmin = False
  if message.author.guild_permissions.kick_members:
    isAdmin = True
  #get info
  userId = message.author.id
  #get user uid
  uid = 0
  #check if muterole exist
  if len(message.content) >= 6:
    if message.content[0:2] == '::':
      if str(sid) + 'muterole' not in db.keys() and message.author.bot == False:
        print('Warning: Muted role is not set. Please set muted role with ```::muterole role\'s name```')
        await channel.send('Warning: Muted role is not set. Please set muted role with ```::muterole role\'s name```')
  #main
  #non mod user can only check sc
  if len(message.content) >= 6 and isAdmin == False:
    if message.content[0:4] == '::sc':
      commandContent = message.content[5:len(message.content)]
      if commandContent.count('<@') > 1:
        print('Invalid syntax')
      else:
        uid = getUID(commandContent)
      #check if user exist in database
      if str(sid)+str(userId) not in db.keys():
        db[str(sid)+str(userId)] = 1000
        print('Added one entry to database:')
        print(str(sid)+str(userId))
      if str(sid)+str(uid) not in db.keys():
        db[str(sid)+str(uid)] = 1000
        print('Added one entry to database:')
        print(str(sid)+str(uid))
      #check user sc
      if i2 + 1 == len(commandContent) or i2 == len(commandContent):
        username = await client.fetch_user(int(uid))
        rep = str(username) + '\'s social credit is: ' + str(db[str(sid)+str(uid)])
        await channel.send(rep)
        print(rep)
  #mod command
  elif len(message.content) >= 6 and isAdmin == True:
    #set muted role
    if message.content[0:10] == '::muterole' and len(message.content) > 11:
      muterole = message.content[11:len(message.content)]
      try:
        member = message.author
        role = discord.utils.get(message.guild.roles, name=muterole)
        await member.add_roles(role)
        await member.remove_roles(role)
        rep = 'Set muted role to: ' + muterole
        db[str(sid) + 'muterole'] = muterole
        await channel.send(rep)
        print(rep)
      except:
        rep = 'Role did not exist'
        muterole = db[str(sid) + 'muterole']
        await channel.send(rep)
        print(rep)
    #command
    elif message.content[0:4] == '::sc':
      commandContent = message.content[5:len(message.content)]
      if commandContent.count('<@') > 1:
        print('Invalid syntax')
      else:
        uid = getUID(commandContent)
      #check if user exist in database
      if str(sid)+str(userId) not in db.keys():
        db[str(sid)+str(userId)] = 1000
        print('Added one entry to database:')
        print(str(sid)+str(userId))
      if str(sid)+str(uid) not in db.keys():
        db[str(sid)+str(uid)] = 1000
        print('Added one entry to database:')
        print(str(sid)+str(uid))
      #check user sc
      if i2 + 1 == len(commandContent) or i2 == len(commandContent):
        username = await client.fetch_user(int(uid))
        rep = str(username) + '\'s social credit is: ' + str(db[str(sid)+str(uid)])
        await channel.send(rep)
        print(rep)
      #check if input value is pos or neg
      else:
        k = 1
        commandContent = commandContent[i2 + 2:len(commandContent)]
        if commandContent[0] == '-':
          k = -1
        elif commandContent[0] == '+':
          k = 1
        else:
          commandContent = '+' + commandContent
          k = 1
        #add or reduce sc
        commandContent = commandContent[1:len(commandContent)]
        socialCredit = 0
        reason = 'none'
        try:
          socialCredit = int(commandContent)*k
          #update sc in database
          value = db[str(sid)+str(uid)]
          value = value + socialCredit
          db[str(sid)+str(uid)] = value
        except:
          i = 0
          while True:
            if commandContent[i] == ' ':
              break
            else:
              i = i + 1
          temp = commandContent[0:i]
          socialCredit = int(temp)*k
          #update sc in database
          value = db[str(sid)+str(uid)]
          value = value + socialCredit
          db[str(sid)+str(uid)] = value
          #reduce commandContent
          commandContent = commandContent[i + 1:len(commandContent)]
          #check reason
          if len(commandContent) == 7 and commandContent[0:7] == 'reason:':
            reason = ""
          elif len(commandContent) > 7 and commandContent[0:7] == 'reason:':
            reason = commandContent[7:len(commandContent)]
        #check exec
        execMsg = "none"
        exec = False
        time = 0
        if value < 0:
          time = abs(value)
          execMsg = "muted for " + str(time) + ' minutes'
          exec = True
        #print output
        pos = ''
        if k == 1:
          pos = '+'
        username = await client.fetch_user(int(uid))
        rep = str(username) + '\'s social credit is: ' + str(value) + '(' + pos + str(socialCredit) + ')' + '\nReason: ' + reason + '\nExecution: ' + str(execMsg)
        await channel.send(rep)
        print(rep)
        #mute member
        if exec == True:
          member = await message.guild.query_members(user_ids=[uid])
          member = member[0]
          try:
            role = discord.utils.get(message.guild.roles, name=db[str(sid) + 'muterole'])
            await member.add_roles(role)
            print('Muted')
            await asyncio.sleep(time*60)
            #unmute member
            await member.remove_roles(role)
            print('timeup')
          except:
            print('Warning: Muted role is not set. Please set muted role with ```::muterole role\'s name```')
            await channel.send('Warning: Muted role is not set. Please set muted role with ```::muterole role\'s name```')
client.run(os.environ['DISCORD_TOKEN'])