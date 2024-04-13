from uagents import Agent, Context, Model
 
class Message(Model):
    message: str
 
# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "project123"
AGENT_MAILBOX_KEY = "063a908d-d56a-41d9-8775-2a94943bee4e"
agent = Agent(
    name="genq",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)
@agent.on_event("startup")
async def handle_message(ctx: Context):
    # ctx.logger.info(f"Received message from {sender}: {msg.message}")

    ctx.logger.info(agent.address)
    await ctx.send("agent1qf9tcuttjj09mmk0jcjz2878dxfnfvtg9vc2zh8etcanvaldh38u58vh37c", Message(message="hello there bob"))
 
if __name__ == "__main__":
    agent.run()
    
there are 2 inputs to be given. one input specifies if it is of type anime or manga, the other input specifies the genre of the anime/manga. the output provides an article of all the top anime/manga along with their brief summary

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

            convo.send_message(f"write a brief, family-friendly  description of the and provide certain details like date of airing, release and if its cureently running or has stopped on{title} {media_type} dont inlude any sexual, violent, harrassment or dangerous content make a family friendly description out of it")
