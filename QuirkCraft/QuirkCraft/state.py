import reflex as rx
import requests

class CraftState(rx.State):
    options: list = ["YouTube", "LinkedIn", "X(Twitter)", "Facebook"]
    topic: str = ""
    platform: str = "YouTube"
    images: list[str] = []
    TextualContent: str = ""
    current_status: str = ""

    api_key = "YOUR_API_KEY"

    def send_message(self):
        if self.topic.strip() == "":
            self.current_status = "Please enter a topic!"
            self.alert()
            return
        
        self.images = []
        self.TextualContent = ""        
        
        if self.platform == "YouTube":
            prompt = f"Act as a scriptwriter assistant for the {self.platform} platform and generate a 60-second script on the topic provided below. Divide the script into three distinct parts, ensuring each part is approximately 20 seconds long & make detailed prompt to generate thumbnail image for the given topic and return answer as Answer format.\nCraft engaging and diverse content, capturing the essence of the topic in each segment. Let the narrative flow seamlessly to create a compelling and dynamic video script.\nAnswer format:\n(Add the new line by using '\\n') & strictly follow the answer format\nGive me two sections: 1) Script section, 2) Thumbnail generation prompt section\n\nThumbnail: (Thumbnail prompt)\n\nTopic: {self.topic}"
        else:
            prompt = f"Act as a postwriter assistant for the {self.platform} platform and generate a quality post(caption) on the topic provided below without any character limit & try to include emojis. Divide the script into distinct parts if possible, ensuring each part is upto the point & make prompt to generate a single image, which is relevant with the provided topic and return answer as Answer format.\nCraft engaging and diverse content, capturing the essence of the topic in each segment. Let the narrative flow seamlessly.\nAnswer format:\n(Add the new line by using '\\n') & strictly follow the answer format\nGive me two sections: 1) Post section, 2) Image generation prompt section\n\nImage: (Image prompt)\n\nTopic: {self.topic}"

        self.current_status = "Generating script/post..."
        self.alert()

        endpoint = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "gpt-4-1106-preview", 
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                    ],
                }
            ]
        }
        response = requests.post(endpoint, headers=headers, json=data).json()

        with open("prompt_response.txt", "w") as f:
            f.write(response['choices'][0]['message']['content'])
        
        text = response['choices'][0]['message']['content']

        if self.platform == "YouTube":
            self.TextualContent = text.split("1) Script section:")[1].split("2)")[0]
        else:
            self.TextualContent = text.split("1) Post section:")[1].split("2)")[0]

        return


    def generate_images(self):
        endpoint = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        with open("prompt_response.txt", "r") as f:
            content = f.read()

        if self.platform == "YouTube":
            image = content.split("Thumbnail: ")[1].removeprefix("(").removesuffix(")")
        else:
            image = content.split("Image: ")[1].removeprefix("(").removesuffix(")")

        data = {
            "model": "dall-e-3",
            "n": 1,
            "size": "1024x1024"
        }

        if(self.platform == "YouTube"):
            data['prompt'] = f"I am making an {self.platform} video on {self.topic}. so generate a thumbnail for it with given description.\n\nThumbnail description: {image}"
        else:
            data['prompt'] = f"I am going to make a post on {self.platform}. so generate relevant image for it with given description.\n\nImage description: {image}"

        response = requests.post(endpoint, headers=headers, json=data).json()
        

        with open("genimage_response.txt", "w") as f:
            f.write(response['data'][0]['url'])

        with open("genimage_response.txt", "r") as f:
            for line in f:
                self.images.append(line.strip())

        with open(f".web/public/{1}.jpg", "wb") as f:
            f.write(requests.get(self.images[0]).content)

        return

    def alert(self):
        return rx.window_alert(f"{self.current_status}")
    
    def helper(self):
        self.current_status = "Generating script/post..."
        rx.window_alert(f"{self.current_status}")
        self.send_message()
        self.current_status = "Generating image..."
        self.alert()
        self.generate_images()
        self.current_status = "Done!"