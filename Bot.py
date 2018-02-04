import discord
import asyncio
import UCIBestProf

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def ics_processor(message):
    message = message.content.split()

    holder = list()
    new_message = str()
    if len(message) == 5:
        info = UCIBestProf.run(message[1], message[2], message[3], message[4])
    elif len(message) > 5:
        info = UCIBestProf.run(message[1], message[2], message[3], " ".join(message[4:]))
    else:
        info = UCIBestProf.run()
    new_message += "```" + '{:11}|{:28}|{:8}|{:3}\n'.format("CLASS", "PROFESSOR", "QUARTER", "QUALITY")
    new_message += "-"*57+'\n'
    count = 2
    for course, instructor in info.items():
        if count > 10:
            new_message += "```"
            holder.append(new_message)
            new_message = "```"
            count = 0
        new_message += '{:11}|{:28}|{:8}|{:3}\n'.format(course, instructor[1], str(",".join(instructor[2]).replace("Fall", "F").replace("Winter", "W").replace("Spring", "S")), instructor[0])
        count += 1
    new_message += "```"
    holder.append(new_message)
    return holder

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!shutdown'):
        await client.send_message(message.channel, 'Shutting down...')
        await client.close()
    elif message.content.startswith('!delay_check'):
        await client.send_typing(message.channel)
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Shutting down...')
    elif message.content.startswith('!embed_send'):
        await client.send_file(message.channel, 'maxresdefault.jpg')
    elif message.content.startswith('!bestICS'):
        await client.send_typing(message.channel)
        response = ics_processor(message)
        for block in response:
            await client.send_message(message.channel, block)

@client.event
async def on_message_delete(message):
    if message.content.startswith('OIT'):
        await client.send_message(message.channel, 'Why would you delete that D:')


if __name__ == '__main__':
    client.run('NDA5MjA5MzM0NDkzMzQ3ODQx.DVbfKw.CXD05lqTCOdMk8boYR6_SMU15QI')
