import discord
from discord.ext import commands
from keras.models import load_model #keras kullanabimek için gerekli kütüphane
from PIL import Image , ImageOps #resim tanıtımı için gerekli kütüphaneler 
import numpy as np # ver işleme için gerekli kütüphaneler





#keras ile modeli hazırlamak 
model = load_model('keras_model.h5')
class_names = open("labels.txt", "r").readlines()



#botumuzu hazırlamak 
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')



@bot.command()
async def check(ctx):
    global model
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url

            await attachment.save(f"./{attachment.filename}")
            await ctx.send(f"Saved the image to ./{attachment.filename}")

            # resmi kaydetmek için bir np arrayi oluşturduk
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            # pil ile resmi açtık
            image = Image.open(f"./{attachment.filename}").convert("RGB")

            # modelimiz 224*224 fotoğraflar için eğitildi bu yüzden 224*224 boyuta getirdik
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

            # boyuttu düzelttikten sonra resimi nparray çevirdik
            image_array = np.asarray(image)

            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

            # np arrayı normal aray attık
            data[0] = normalized_image_array

            # Predicts the model
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            
            # Print prediction and confidence score
            await ctx.send(f"Class: {class_name[2:]}")
            await ctx.send(f"Confidence Score: {confidence_score}")


            
    else:
        await ctx.send("You forgot to upload the image :(")



bot.run("Token")