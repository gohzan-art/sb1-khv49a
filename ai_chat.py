import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

async def handle_ai_question(ctx, question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a military Discord server."},
                {"role": "user", "content": question}
            ]
        )
        await ctx.send(response.choices[0].message['content'])
    except Exception as e:
        await ctx.send(f"An error occurred while processing your question: {str(e)}")

# Add more AI-related functions as needed