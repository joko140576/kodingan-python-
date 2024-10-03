import random

# Contoh respons sederhana
responses = {
    "assalamualaikum": ["walaikumusalam Wr Wb !", "Salam damai untukmu!", "semoga Tuhan memberkatimu!"],
    "terima kasih": ["baik, sama-sama", "terima kasih kembali", "terima kasih kembali"],
    "sampai jumpa": ["terima kasih, sampai bertemu kembali di lain kesempatan", "baik, hati-hati di jalan", "tetap semangat dan sehat selalu"],
}

def chatbot_response(user_input):
    for key in responses:
        if key in user_input.lower():
            return random.choice(responses[key])
    return "maaf saya tidak tahu apa yang kamu maksud?"

# Simulasi interaksi
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Bye!")
        break
    print("Chatbot:", chatbot_response(user_input))
