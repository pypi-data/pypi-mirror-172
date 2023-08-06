import urllib.parse
from .config import config

lowQuality = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,"
htags=["nsfw","nude"]
basetag = "{masterpiece}, extremely detailed 8k wallpaper, best quality, an extremely delicate and beautiful,"
token = config.novelai_token
header = {
    "authorization": "Bearer " + token,
    ":authority": urllib.parse.urlparse(config.novelai_api_domain).hostname,
    ":path": "/ai/generate-image",
    "content-type": "application/json",
    "referer": config.novelai_site_domain,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}

def txt2img_body(seed, input, map):
    if config.novelai_h:
        uc=lowQuality
    else:
        htagstr=""
        for i in htags:
            htagstr=htagstr+i+","
        uc=lowQuality+htagstr
    return {
        "input": input + basetag + config.novelai_tag,
        "model": "safe-diffusion",
        "parameters": {
            "width": map[1],
            "height": map[0],
            "scale": 11,
            "sampler": "k_euler_ancestral",
            "qualityToggle":True,
            "steps": 28,
            "seed": seed,
            "n_samples": 1,
            "ucPreset": 0,
            "uc": uc,
        },
    }
from PIL import Image
from io import BytesIO
import base64
from nonebot.log import logger
def img2img_body(seed, input,img_b64):
    tmpfile=BytesIO(img_b64)
    image = Image.open(tmpfile)
    width,height=image.size
    if width>=height:
        width=round(width/height*8)*64
        height=512
    else:
        height=round(height/width*8)*64
        width=512
    if config.novelai_h:
        uc=lowQuality
    else:
        htagstr=""
        for i in htags:
            htagstr=htagstr+i+","
        uc=lowQuality+htagstr
    image=str(base64.b64encode(img_b64),"utf-8")
    logger.debug(image)
    return {
        "input": input + basetag + config.novelai_tag,
        "model": "safe-diffusion",
        "parameters": {
            "width": width,
            "image": image,
            "noise":0.2,
            "strength":0.7,
            "height": height,
            "qualityToggle":True,
            "scale": 11,
            "sampler": "k_euler_ancestral",
            "steps": 50,
            "seed": seed,
            "n_samples": 1,
            "ucPreset": 0,
            "uc": uc,
        },
    }

def check_anias(width,height,img_b64,strength=0.7,count=1):
    #计算需要消耗的点数
    tmpfile=BytesIO(img_b64)
    image = Image.open(tmpfile)
    width,height=image.size
    if width>=height:
        width=round(width/height*8)*64
        height=512
    else:
        height=round(height/width*8)*64
        width=512
    return round(width*height*strength*count/45875)