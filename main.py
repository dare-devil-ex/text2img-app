import requests
import time
from io import BytesIO
from PIL import Image as PilImage
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
import os

API_URL = "https://ai-api.magicstudio.com/api/ai-art-generator"
HEADERS = {
    "sec-ch-ua-platform": "\"Android\"",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua": "\"Android WebView\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "origin": "https://magicstudio.com",
    "x-requested-with": "mark.via.gq",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://magicstudio.com/ai-art-generator/",
    "accept-language": "en-US,en;q=0.9",
}

def Ai(prompt):
    data = {
        "prompt": prompt,
        "output_format": "bytes",
        "user_profile_id": "null",
        "anonymous_user_id": "12392865-ff1f-4ef7-a67d-00f058fbe6cf",
        "request_timestamp": "1734701568.295",
        "user_is_subscribed": "false",
        "client_id": "pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o",
    }
    for attempt in range(3):
        try:
            response = requests.post(API_URL, headers=HEADERS, data=data, timeout=10)
            if response.status_code == 200:
                return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Attempt {attempt + 1} of 3.")
            time.sleep(5)
    return None

# Begin
class MyApp(App):
    def build(self):
        Window.size = (360, 640)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.image_widget = Image(size_hint=(1, 0.5))
        self.label = Label(text="Enter a prompt to generate AI art:", size_hint_y=None, height=40)
        self.input_box = TextInput(hint_text="Type your prompt here...", multiline=False, size_hint_y=None, height=40)

        generate_button = Button(text="Generate Image", size_hint_y=None, height=60)
        generate_button.bind(on_press=self.on_generate_button_click)

        save_button = Button(text="Save Image", size_hint_y=None, height=60)
        save_button.bind(on_press=self.on_save_button_click)

        layout.add_widget(self.image_widget)
        layout.add_widget(self.label)
        layout.add_widget(self.input_box)
        layout.add_widget(generate_button)
        layout.add_widget(save_button)

        return layout

    def on_generate_button_click(self, instance):
        prompt = self.input_box.text
        if prompt:
            self.label.text = "Generating image..."
            image_data = Ai(prompt)

            if image_data:
                image_data = BytesIO(image_data)
                pil_image = PilImage.open(image_data)
                pil_image = pil_image.convert('RGBA')
                byte_arr = BytesIO()
                pil_image.save(byte_arr, format='PNG')
                byte_arr.seek(0)

                kivy_image = CoreImage(byte_arr, ext="png")
                self.image_widget.texture = kivy_image.texture

                self.label.text = "Image generated successfully!"
                self.generated_image = pil_image
            else:
                self.label.text = "Failed to generate image. Try again."
        else:
            self.label.text = "Please enter a prompt."
            image_data = Ai(prompt)
            image_data = BytesIO(image_data)
            pil_image = PilImage.open(image_data)
            pil_image = pil_image.convert('RGBA')
            byte_arr = BytesIO()
            pil_image.save(byte_arr, format='PNG')
            byte_arr.seek(0)
            kivy_image = CoreImage(byte_arr, ext="png")
            self.image_widget.texture = kivy_image.texture
            self.generated_image = pil_image

    def on_save_button_click(self, instance):
        if hasattr(self, 'generated_image') and self.generated_image:
            nameWkaie = int(time.time())
            save_path = os.path.join(os.getcwd(), "{}.png".format(nameWkaie))
            self.generated_image.save(save_path)
            self.label.text = f"Image saved as {save_path}"
        else:
            self.label.text = "No image to save."
            
if __name__ == "__main__":
    MyApp().run()
