import sys
import requests
from io import BytesIO
from PIL import Image
from ascii_magic import AsciiArt

def get_image(path_or_url):
    if path_or_url.startswith('http://') or path_or_url.startswith('https://'):
        response = requests.get(path_or_url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    else:
        return Image.open(path_or_url)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path_or_url>")
        sys.exit(1)
    image_source = sys.argv[1]
    img = get_image(image_source)
    box = AsciiArt.from_pillow_image(img)
    box.to_html_file('ascii_art.html', columns=500, additional_styles="background:black; color:#0f0;")

    # Amend the HTML file to add custom styles
    with open('ascii_art.html', 'r', encoding='utf-8') as f:
        html = f.read()

    style_block = """
    <style>
    body {
        background: black;
        min-height: 100vh;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """

    if "<head>" in html:
        html = html.replace("<head>", "<head>" + style_block)
    else:
        html = style_block + html

    with open('ascii_art.html', 'w', encoding='utf-8') as f:
        f.write(html)
