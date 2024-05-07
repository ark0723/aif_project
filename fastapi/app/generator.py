from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
import os
import time

load_dotenv()


def get_community_model_list():
    # https://stablediffusionapi.com/docs/miscs/model-list
    url = "https://stablediffusionapi.com/api/v4/dreambooth/model_list"

    payload = json.dumps({"key": os.getenv("STABLE_DIFFUSION_KEY")})
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def generate_ai_image(keyword: str, style: str):
    # 1. given keyword from user
    # 2. ask chatgpt to complete prompt
    # 3. then ask stable-diffusion to generate the image

    start = time.time()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Given the following keyword: {keyword}, generate a {style} of image. write down prompt with more details within 20 words.",
            },
        ],
        temperature=0.8,
    )

    output = completion.choices[0].message.content.strip("\n")
    output_list = output.split("\n")
    description = output_list[0]
    print(f"prompt : {description}")

    # stable diffusion

    url = "https://stablediffusionapi.com/api/v3/text2img"

    negative_words = ["nsfw", "uncensored", "cleavage", "nude", "nipples"]

    payload = json.dumps(
        {
            "key": os.getenv("STABLE_DIFFUSION_KEY"),
            "prompt": description,
            "negative_prompt": ",".join(negative_words),
            "width": "512",  # max width: 1024
            "height": "512",  # max height: 1024
            "samples": "4",  # max: 4
            "num_inference_steps": "20",
            "seed": None,  # Seed is used to reproduce results, same seed will give you same image in return again. Pass null for a random number.
            "guidance_scale": 7.5,  # Scale for classifier-free guidance (minimum: 1; maximum: 20).
            "enhance_prompot": "yes",  # (())
            "safety_checker": "yes",  # A checker for NSFW images. If such an image is detected, it will be replaced by a blank image.
            "multi_lingual": "no",
            "panorama": "no",
            "self_attention": "no",  # If you want a high quality image, set this parameter to "yes". In this case the image generation will take more time.
            "upscale": "no",  # Set this parameter to "yes" if you want to upscale the given image resolution two times (2x). If the requested resolution is 512 x 512 px, the generated image will be 1024 x 1024 px.
            "embeddings_model": None,
            "webhook": None,
            "track_id": None,
        }
    )

    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload, timeout=100)
    # response.text : str -> json.loads(response.text): dict
    img_urls = json.loads(response.text)["output"]  # "output"/"proxy_links"

    end = time.time()
    print(end - start)  # time in seconds

    return img_urls


def generate_ai_image_community_model(keyword: str, style: str, model_id: str):
    # 1. given keyword from user
    # 2. ask chatgpt to complete prompt
    # 3. then ask stable-diffusion to generate the image

    start = time.time()

    client = OpenAI()

    """
    프롬프트 예시
    (스타일키워드입력:)스타일로 (키워드입력: 멋진 남자배우가 가로등을 기대어 서있는 모습, 빈티지스러운 색상, 스토리가 있어보이는 환경), 
    티셔츠에 넣기 좋은 이미지 키워드를, 
    (이미지 느낌에 따라 완전히 흰 배경 또는 검정 배경에), 
    (사진인지, 그림인지), 
    (동물인지, 사람인지, 풍경인지), 조명 종류, 시점, 배경, 사진기가 광각인지 망원인지를 
    고려해서 스테이블 디퓨전에 적절한 프롬프트를 영어로 적어줘
    """

    # style_codes = ['레트로', '팝아트', '데코', '그라피티', '키덜트', '라인아트', '스테인드글라스', '빈티지 포스터']

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"({style}) 스타일로, ({keyword}), 티셔츠에 넣기 좋은 이미지 키워드를, (이미지 느낌에 따라 완전히 흰 배경 또는 검정 배경에), (사진인지, 그림인지), (동물인지, 사람인지, 풍경인지), 조명 종류, 시점, 배경, 사진기가 광각인지 망원인지를 고려해서 스테이블 디퓨전에 적절한 프롬프트를 영어로 적어줘",
            },
        ],
        temperature=0.8,
    )

    output = completion.choices[0].message.content.strip("\n")
    output_list = output.split("\n")
    description = output_list[0]
    print(f"prompt : {description}")

    # stable diffusion

    url = "https://stablediffusionapi.com/api/v4/dreambooth"

    negative_words = [
        "nsfw",
        "uncensored",
        "cleavage",
        "nude",
        "nipples",
        "painting",
        "extra fingers",
        "mutated hands",
        "poorly drawn hands",
        "poorly drawn face",
        "distorted form",
        "deformed",
        "bad crushed",
        "ugly",
        "blurry",
        "bad anatomy",
        "bad proportions",
        "extra limbs",
        "cloned face",
        "skinny",
        "glitchy",
        "double torso",
        "extra arms",
        "extra hands",
        "mangled fingers",
        "missing lips",
        "ugly face",
        "distorted face",
        "extra legs",
        "truncated image",
        "cropped image",
        "a mock-up image",
        "Images unrelated to the prompt you entered",
        "An image where the main prompt you entered is not the main character",
    ]

    if style in ["그라피티", "그래피티"]:
        negative_words.append("a picture drawn on the street")

    payload = json.dumps(
        {
            "key": os.getenv("STABLE_DIFFUSION_KEY"),
            "prompt": description,
            "negative_prompt": ",".join(negative_words),
            "model_id": model_id,
            "width": "512",
            "height": "512",
            "samples": "4",
            "num_inference_steps": "30",
            "safety_checker": "yes",
            "enhance_prompt": "yes",
            "seed": 9284,
            "guidance_scale": 7.5,
            "multi_lingual": "no",
            "panorama": "no",
            "self_attention": "no",
            "upscale": "no",
            "embeddings_model": None,
            "lora_model": None,
            "tomesd": "yes",
            "use_karras_sigmas": "yes",
            "vae": None,
            "lora_strength": None,
            "scheduler": "UniPCMultistepScheduler",
            "webhook": None,
            "track_id": None,
        }
    )

    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload, timeout=200)
    # response.text : str -> json.loads(response.text): dict
    img_urls = json.loads(response.text)["output"]  # "output"/"proxy_links"

    end = time.time()
    print(end - start)  # time in seconds

    return img_urls


def upscale_from_image(img_url: str):
    start = time.time()

    url = "https://stablediffusionapi.com/api/v3/img2img"

    payload = json.dumps(
        {
            "key": os.getenv("STABLE_DIFFUSION_KEY"),
            "prompt": None,
            "negative_prompt": None,
            "init_image": img_url,
            "width": "1024",
            "height": "1024",
            "samples": "1",
            "num_inference_steps": "30",
            "safety_checker": "no",
            "enhance_prompt": "yes",
            "guidance_scale": 7.5,
            "strength": 0,
            "base64": "no",
            "seed": None,
            "webhook": None,
            "track_id": None,
        }
    )

    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload, timeout=100)
    # response.text : str -> json.loads(response.text): dict
    img_urls = json.loads(response.text)["output"]  # "output"/"proxy_links"

    end = time.time()
    print(end - start)  # time in seconds

    return img_urls
