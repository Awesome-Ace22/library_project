from flask import Flask, request, jsonify, send_file
import subprocess
import asyncio
import os
from datetime import datetime
from books import read_all, read_one
from io import BytesIO
import requests
from PIL import Image

async def fetch_image(isbn):
    # Call your Python script here to get the image URL
    #image_url = subprocess.check_output(['python', 'your_script.py', isbn]).decode('utf-8').strip()
    book = read_one(isbn)
    image_url = (book['thumbnail']).decode('utf-8').strip()
    response = requests.get(image_url)
    if response.status_code == 200:
        image = BytesIO(response.content)
        return image #.seek(0)
    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")
        return None


async def download_image(url, filename):
    # Download image and save it locally
    # You can use requests library or any other method
    # Ensure to handle exceptions and return appropriate responses
    pass

async def get_image(isbn):
    try:
        image_url = await fetch_image(isbn)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{isbn}_{timestamp}.jpg"

        await asyncio.gather(
            download_image(image_url, filename)
        )

        return jsonify({'filename': filename, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False})


