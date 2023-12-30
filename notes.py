@bot.command()
async def check(ctx):
    global model
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url

            await attachment.save(f"./{attachment.filename}")
            await ctx.send(f"Saved the image to ./{attachment.filename}")

            # buraya kodunu ekle 

            await ctx.send(f"Class: {class_name[2:]}")
            await ctx.send(f"Confidence Score: {confidence_score}")

        else:
            await ctx.send("You forgot to upload the image :(")