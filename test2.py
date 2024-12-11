import os
from openai import OpenAI
from pathlib import Path

client = OpenAI(
    api_key='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',
)
#
# prompt = """
# Act as a fluent English speaker. Engage in a natural, conversational exchange with me, responding thoughtfully to my questions or comments. Use everyday vocabulary, idiomatic expressions, and proper grammar to make the conversation immersive and realistic. Adapt your tone and style based on the topic or context, and feel free to ask me questions to keep the conversation going.
#
# If I make any mistakes, politely correct them and offer a short explanation to help me learn.
#
# Here’s an example interaction:
#
# User: 'Hi, how are you?' Assistant: 'I’m doing great, thanks for asking! How about you?'
#
# Only give conversation response.
#
# Let’s begin! My first message is:
# """
#
#
# conversation_history = [
#     {"role": "system", "content": prompt}
# ]
# def ask_openai(prompt, conversation_history):
#     conversation_history.append({"role": "user", "content": prompt})
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=conversation_history,
#     )
#
#     assistant_reply = response.choices[0].message.content
#
#     conversation_history.append({"role": "assistant", "content": assistant_reply})
#
#     return assistant_reply


# # Example interaction
# user_input = "Hi, how are you? I am Harun"
# response = ask_openai(user_input, conversation_history)
# print(response)
#
# # Another interaction
# user_input = "Do you know my name?"
# response = ask_openai(user_input, conversation_history)
# print(response)


from openai import OpenAI

speech_file_path = Path(__file__).parent / "speech.mp3"

with client.with_streaming_response.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!"
) as response:
    response.stream_to_file(speech_file_path)