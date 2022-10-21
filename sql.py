import discord
import mysql.connector
import os
from discord.ext import commands

#creating databases
def create_database():
    def checklogger():
        try:
            print("------ checking logger files")
            f1=open('errorlogger.txt','r+')
            f1.truncate(0)
            print("------ errorlogger.txt truncated")
            f2=open('execution_logger.txt','r+')
            f2.truncate(0)
            print("------ execution_logger.txt truncated")
        except:
            print("------ logger file missing")
            print("------ creating logger file ------")
            os.system('cmd /c "fsutil file createnew errorlogger.txt 1000"')
            os.system('cmd /c "fsutil file createnew execution_logger.txt 1000"')
            print("------ logger files created ------")
    
    global mydb
    try:
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="smfsql123",
            database="sqltest"
        )
        print('''------ connected with database "sqltest" successfully''')
        global my_cursor
        my_cursor=mydb.cursor(buffered=True)
        checklogger()

    except:
        print("------ database not found")
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="smfsql123"
        )
        my_cursor=mydb.cursor()
        print('''------ creating new database as "sqltest"''')
        my_cursor.execute("CREATE DATABASE sqltest;")
        print('''------ database created as "sqltext"''')
        print("------ re-connecting database")

        create_database()

b=[79, 84, 89, 48,79, 84, 85, 49, 79, 84, 103, 120, 78, 106, 89, 48, 78, 106, 81, 120, 77, 84, 69, 48, 46, 71, 74, 55, 48, 55, 117, 46, 48, 53, 116, 68, 99, 97, 70, 52, 112, 116, 118, 75, 78, 101, 75, 80, 90, 99, 109, 83, 112, 55, 109, 119, 117, 66, 98, 113, 105, 102, 98, 103, 75, 65, 77, 70, 72, 77]

c=""

for j in b:
    c+=chr(j)
        
create_database()

bot_token=c

intents=discord.Intents.all()
intents.members=True
bot = commands.AutoShardedBot(command_prefix="!", intents =intents)

@bot.event
async def on_ready():
    print("------ The bot is ready to perform")

@bot.command(aliases=['sc','scd'])
async def sqlcmd(ctx,cmdnum):
    print(cmdnum)

    channel = bot.get_channel(1029632347982798909)
    messages = await channel.history(limit=None).flatten()
    print('his check')

    for msg in messages:
        #await ctx.channel.send(msg.content)

        if msg.content.startswith(cmdnum):
            print(msg.jump_url)
            await ctx.reply(msg.content)
            break
    print('------ query found; query number:',cmdnum)

@bot.command(aliases=['sce','scte'])
async def editsqlcmd(ctx,cmdnum,*,content):
    print(cmdnum)

    channel = bot.get_channel(1029632347982798909)
    messages = await channel.history(limit=None).flatten()
    print('his check')

    for msg in messages:
        #await ctx.channel.send(msg.content)

        if msg.content.startswith(cmdnum):
            await msg.edit(content=content)
            break
    await ctx.message.delete()
    print('done')

@bot.command(aliases=['ebi'])
async def editbyid(ctx,cmdnum,*,content):
    print(cmdnum)

    channel = bot.get_channel(1029632347982798909)
    messages = await channel.history(limit=15).flatten()
    print('his check')

    for msg in messages:
        #await ctx.channel.send(msg.content)
        if msg.id==int(cmdnum):
            print(content)
            await msg.edit(content=content)
    await ctx.message.delete()
    print('done')

@bot.command(aliases=['cs','scs'])
async def cmdsend(ctx,*,content):

    channel = bot.get_channel(1029632347982798909)
    await channel.send(content)
    print('done')

@bot.command(aliases=['ex'])
async def exsqlcmd(ctx):

    channel = bot.get_channel(1029632347982798909)
    messages = await channel.history(limit=200).flatten()
    print('history fetching done')
    with open('execution_logger.txt','w') as f1:
        with open('errorlogger.txt','w') as f2:
            for j,msg in enumerate(messages):
                i=msg.content
                i=i.split("\n",1)
                if i[0].find("```sql")!=-1:
                    i=i[1]
                    i=i.replace('```',"")
                else:
                    i=i[1]
                    i=i.replace('sql',"")
                    i=i.replace('```',"")
                #print(i)
                try:
                    log=my_cursor.execute(f'''{str(i)}''')
                    mydb.commit()
                    f1.write(str(log)+str(j+1)+"\n")
                except Exception as e:
                    f2.write(str(e)+str(j+1)+"\n")
                    f2.write(str(i)+"\n")
                    #print("error "+str(e)+" "+str(j+1))
                    
            #print(i)
    print('done')
    f1.close()
    f2.close()

@bot.command(aliases=['gm'])
async def getmsg(ctx,msgid):
    msg=await ctx.fetch_message(int(msgid))
    print(msg.content)
    await ctx.reply(msg.content)

bot.run(bot_token)
