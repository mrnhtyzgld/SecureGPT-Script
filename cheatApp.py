import openai
import keyboard

openai.api_key = "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"

state = "waiting"
# waiting   => kullanıcının chat gptye soru sormak için tıklamasını bekliyoruz
# listening => yazılanları okuyoruz
# sending   => chat gpt'nin cevabını bekliyoruz

prompt = ""
log = ""


def callback(event):
    global log
    if state == "listening":
        name = event.name 
        if name == "space":
            name = " "
        elif len(name) > 1:
            name = ""

        log += name
    return

def questionToAi(q):
    global prompt
    prompt += f"You: {q}\nAI: "
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def mainFunc():
    
    global state, prompt, log

    keyboard.write("\n")

    if state == "waiting":
        state = "listening"
    elif state == "listening":
        state = "sending"

    if state == "sending":
        answer = questionToAi(log)
        prompt += answer
        keyboard.write(answer + "\n")

        state = "waiting"
        log = ""





keyboard.on_release(callback=callback)
keyboard.add_hotkey('end', lambda: mainFunc(), suppress=True, timeout=100)
keyboard.wait("page down", suppress=True)
