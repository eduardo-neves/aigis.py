import os
import asyncio
import json
from random import randint
import requests

import discord
from discord.ext import commands
import pymongo
from dotenv import load_dotenv

from hentai import Hentai, Format, Utils, Option, Tag, Sort
import hmtai

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ATLAS = os.getenv('ATLAS_TOKEN')
MYID = os.getenv('MYID')

client = pymongo.MongoClient(ATLAS)
db = client.quotesAigis

headers = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

prefix = '&'
bot = discord.Client()
bot = commands.Bot(command_prefix=prefix)
activity = discord.Activity(type=discord.ActivityType.listening, name=prefix + 'help')
# activity = discord.Activity(type=discord.ActivityType.listening, name='Development mode')
bot.remove_command('help')

##Event listeners below
@bot.event
async def on_message(message):
    await bot.process_commands(message)
        
    if message.author == bot.user:
        return

    if message.content == ('$im Catra') or message.content == ('$im catra'):
        await message.add_reaction('😍')
        await message.channel.send("Gasosa certificada.", tts=True) 
    if message.content == ('$im aigis') or message.content == ('$im aegis'):
        await message.add_reaction('🤔')
        await message.channel.send("Pera, sou eu.", tts=True)
    
    if message.content == ("aga eme") or message.content == ("Aga eme"):
        await message.add_reaction('🤔')

    if message.content == (prefix + 'quote'):
        await message.add_reaction('🤔')
        guild = str(message.guild.id)
        print(guild)
        for doc in db[guild].aggregate([ { '$sample': { 'size': 1 } } ]):
            frase = doc['text']
            autor = doc['author']
            output = '*' + frase + '*' + ' - ' + '**' + autor + '**'            
        await message.channel.send(output)

    if message.content == (prefix + 'quotetts'):
        await message.add_reaction('🤔')
        guild = str(message.guild.id)
        for doc in db[guild].aggregate([ { '$sample': { 'size': 1 } } ]):
            frase = doc['text']
            autor = doc['author']
            output = frase + ' - ' + autor
        await message.channel.send(output, tts=True) 

    if message.content == (prefix + 'quoteall'):
        await message.add_reaction('🤔')
        guild = str(message.guild.id)
        i = 0
        for doc in db[guild].find():
            i += 1
            frases = doc['text']
            autores = doc['author']
            output = str(i) + '. '+ '*' + frases + '*' + ' - ' + '**' + autores + '**'
            await message.channel.send(output)

    

    if message.content == (prefix + 'gay'):
        await message.add_reaction('👌')
        await message.channel.send('Não você.', tts=True)

    ##Comando para chamar a Hanna de gay
    if (message.content != ''):
        if (message.author.id == 277911113985949696):
            if (randint(0,100) == 69):
                await message.channel.send('A Hanna é gay.')

    if message.content == (prefix + 'hanna'):
        await message.add_reaction('👌')
        await message.channel.send('Não quero dar trabai')
        await asyncio.sleep(3)
        await message.channel.send('Also Gay')

    if message.content == (prefix + 'help'):
        await message.add_reaction('👿')
        embedVar = discord.Embed(title='Aigis', description='Zoas. Comandos disponíveis:', color=0x00a1ff)
        embedVar.set_thumbnail(url="https://preview.redd.it/6kbe384aie651.png?width=960&crop=smart&auto=webp&s=a529546a8e3465396463576d041448a4172b2505")
        embedVar.add_field(name="quote", value="Puxa uma frase aleatória.", inline=False)
        embedVar.add_field(name="quotetts", value="Puxa uma frase aleatória, só que em tts.", inline=False)
        embedVar.add_field(name="quotea", value="Puxa uma ou todas as frases de algum autor. Use o comando para detalhes.", inline=False)
        embedVar.add_field(name="quoteall", value="Puxa todas as frases registradas.", inline=False)
        embedVar.add_field(name="add", value="Adiciona uma nova frase. Use o comando para detalhes.", inline=False)
        embedVar.add_field(name="dol", value="Puxa o valor do dólar em real.", inline=False)
        embedVar.add_field(name="doge", value="Puxa o valor do doge em real.", inline=False)
        embedVar.add_field(name="Outros", value="%shelp18 = ???" %prefix, inline=False)
        embedVar.add_field(name="Mais ajuda?", value="Se precisar manda mensagem para o %s." % MYID, inline=False)
        await message.channel.send('Tem nada aqui otário.')
        await asyncio.sleep(3)
        await message.channel.send(embed=embedVar)
    
    if message.content == (prefix + 'help18'):
        await message.add_reaction('😩')
        embedVar = discord.Embed(title='Aigis', description='Comandos +18 disponíveis (ainda em desenvolvimento):', color=0xf274bd)
        embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/770948564947304448/771374855333085194/418-WVRNSuH_xb0.jpg")
        embedVar.add_field(name="nh", value="Permite pesquisar um doujin do nhentai.net por número", inline=False)
        embedVar.add_field(name="nhr", value="Responde com um doujin aleatório do nhentai.net (*agora suporta tags!* Use **%snhr h/-h/help/help** para detalhes)" %prefix, inline=False)
        embedVar.add_field(name="r34", value="Traz um NSFW. Aceita tag (use rule34 tags para ver as disponíveis)", inline=False)
        embedVar.add_field(name="doll", value="Traz uma bonequinha", inline=False)
        embedVar.add_field(name="Outros",value="Se precisar manda mensagem para o %s." % MYID, inline=False)
        await message.channel.send(embed=embedVar)
    
##Explicit bot commands below
@bot.command()
async def add(message, frase=None, nome=None):
    if nome is not None and frase is not None:
        newquote = {"author": nome,
            "text": frase}
        guild = str(message.guild.id)
        db[guild].insert_one(newquote).inserted_id
        await message.channel.send("Adicionado.")
    else:
        await message.channel.send('Erro ao adicionar. Tente &add "Frase entre aspas duplas" autor')
    
@bot.command()
async def quotea(message, nome=None, allopc=None):
    if nome is not None:
        guild = str(message.guild.id)
        if allopc == 'all':
            i = 0
            for doc in db[guild].find({"author": nome}):
                i += 1
                frase = doc['text']
                autor = doc['author']
                output = str(i) + '. '+ '*' + frase + '*' + ' - ' + '**' + autor + '**'
                await message.channel.send(output)
        elif allopc == 'tts':
            for doc in db[guild].aggregate([ {'$match': {'author': nome} }, { '$sample': { 'size': 1 } }]):
                frase = doc['text']
                autor = doc['author']
                output = frase + ' - ' + autor
                await message.channel.send(output, tts=True)
        elif allopc is None:
            for doc in db[guild].aggregate([ {'$match': {'author': nome} }, { '$sample': { 'size': 1 } }]):
                frase = doc['text']
                autor = doc['author']
                output = '*' + frase + '*' + ' - ' + '**' + autor + '**'            
                await message.channel.send(output)
    else:
        await message.channel.send('Esse autor não existe, parça. Tente &quotea Autor')
        await message.channel.send('*Você sabia? Pode puxar todas as frases com o sufixo all (**%squotea Autor all**)*' %prefix)

@bot.command()
async def dol(message):
    pedido = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
    retorno = pedido.json()
    dol = float(retorno['USD']['high'])
    dol = round(dol, 2)
    await message.channel.send("O valor do dol é %s reaus." % dol, tts=True)

@bot.command()
async def doge(message):
    pedido = requests.get('https://economia.awesomeapi.com.br/all/DOGE-BRL', headers=headers)
    retorno = pedido.json()
    dol = float(retorno['DOGE']['bid'])
    variacao = float(retorno['DOGE']['pctChange'])
    await message.channel.send("O valor do doggo é %s reaus com variação de %s." % (dol, variacao), tts=False)

@bot.command()
async def kek(message):
    if (randint(0,1) > 0):
        imageURL = "https://i.kym-cdn.com/photos/images/newsfeed/001/564/945/0cd.png"
        await message.channel.send(imageURL)
    else:
        imageURL = "https://i.kym-cdn.com/photos/images/newsfeed/000/652/412/2f8.png"
        await message.channel.send(imageURL)

@bot.command()
async def r34(message, tag="hentai"):
    if (tag == "tags"):
        tags = "ass, bdsm, cum, manga, femdom, hentai(tag padrão), masturbation, ero, orgy, yuri, pantsu, glasses, cuckold, blowjob, foot, thighs, vagina, ahegao, uniform, gangbang, tentacles, wallpaper, mobileWallpaper, neko, jahy, nsfwNeko, nsfwMobileWallpaper, zettaiRyouiki, Vein05"
        await message.channel.send(tags)
    elif (tag != "hentai"):
        imagelink = hmtai.useHM('v2', tag)
        await message.channel.send(imagelink)
    else:
        imagelink = hmtai.useHM('v2', tag)
        await message.channel.send(imagelink)

@bot.command()
async def nh(message, sauce):
    try:
        doujin = Hentai(sauce)
        if (Hentai.exists(doujin.id) == True):
            base_url = 'https://nhentai.net/g/'
            final_url = base_url + sauce + "/"
            await message.channel.send(final_url)
    except:
        await message.channel.send("Esse sauce não existe parça.")

@bot.command()
async def nhr(message, *tags):
    if not tags:
        random = str(Utils.get_random_id())
        base_url = 'https://nhentai.net/g/'
        final_url = base_url + random + "/"
        await message.channel.send(final_url)
    else:
        print("Entered else statement")
        query_tags = ""
        fTags = ""
        n = 0
        language = "language:english"
        commandHelp = ""
        for tag in tags:
            if (tag == "-help") or (tag == "-h") or (tag == "h") or (tag == "help"):
                commandHelp = "Use quaisquer combinação de tags. Ex: *%snhr yuri pantyhose*\nTambém pode usar - para remover uma tag. Ex: *%snhr glasses -netorare*" %(prefix, prefix)
                await message.channel.send(commandHelp)
                break
            #enables multiple language support (to be defined in if statement)
            # if tag == "translated" or tag == "english":
            #     language = "language:" + tag
            # else:
            query_tags += tag + " "
            if query_tags != "":
                fTags = "tag:" + query_tags
        query = fTags + language
        doujins = Utils.search_by_query(query, sort=Sort.PopularToday)
        selected = randint(0, len(doujins))
        
        for doujin in doujins:
            if (commandHelp != ""):
                break
            if (n == selected):
                base_url = 'https://nhentai.net/g/'
                final_url = base_url + str(doujin.id) + "/"
                print(doujin.title(Format.Pretty))
                print(final_url)
                await message.channel.send(final_url)
            n += 1

@bot.command()
async def doll(message):
    await message.channel.send("Lolicon.")

@bot.command()
async def gostosa(message):
    await message.channel.send("Sim")

@bot.command()
async def gasosa(message):
    await message.channel.send("*Y E S*")

@bot.command()
async def f(message):
    imageURL = "https://i.kym-cdn.com/entries/icons/original/000/017/039/pressf.jpg"
    embed = discord.Embed(title="F", color=0x00a1ff)
    embed.set_image(url=imageURL)
    await message.channel.send(embed = embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=activity)
    os.system('cls')
    print(bot.user.name, 'is running (%s)' % bot.user.id)
    print('---------------------------------------')

bot.run(TOKEN)
