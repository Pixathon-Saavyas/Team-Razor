from uagents import Agent, Context, Model
import requests
import google.generativeai as genai
from pydantic import Field
#from ai_engine import UAgentResponse, UAgentResponseType # type: ignore
# Define the GraphQL query as a multi-line string
genai.configure(api_key="AIzaSyDZbLNK62ncgJpA22-YDAaJ6gQt1CTYujE")
 
class anorman(Model):
    choice: str = Field(description="The choice. Must be ANIME or MANGA.")
    genre: str = Field(description = "The input must be a valid anime/manga genre")
    
class Message(Model):
    message: str
 
# First generate a secure seed phrase (e.g. https://pypi.org/project/mnemonic/)
SEED_PHRASE = "ytgdsjdiuhwodiuicoicjw"
 
# Copy the address shown below
print(f"Your agent's address is: {Agent(seed=SEED_PHRASE).address}")
 
# Then go to https://agentverse.ai, register your agent in the Mailroom
# and copy the agent's mailbox key
AGENT_MAILBOX_KEY = "1f57b9b8-5339-4498-83a2-ebf953ee6c25"
 
# Now your agent is ready to join the agentverse!
agent = Agent(
    name="alice",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)
 
 # Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

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

model = genai.GenerativeModel(model_name='gemini-pro')

convo = model.start_chat(history=[
])
@agent.on_message(model=anorman, replies={Message})
async def handle_message(ctx: Context, sender: str, msg: anorman):
    ctx.logger.info(f"Received message from {sender}: {msg.choice}")
    query = '''
    query (
    $page: Int,
    $perPage: Int,
    $type: MediaType,
    $sort: [MediaSort],
    $genre: String,
    ) {
    Page (page: $page, perPage: $perPage) {
        media (
        type: $type,
        sort: $sort,
        genre: $genre
        ) {
        id
        title {
            userPreferred
        }
        popularity
        }
    }
    }
    '''

    # Function to get user input for media type

    # Function to get user input for genre
    def get_genre():
        return msg.genre

    # Get user input for media type and genre
    media_type = msg.choice
    genre = get_genre()

    # Define the query variables and values based on user input
    variables = {
        'page': 1,
        'perPage': 10,  # Limit to 10 results
        'type': media_type.upper(),  # Filter by user-selected media type (anime or manga)
        'sort': ['POPULARITY_DESC'],  # Sort by popularity in descending order
        'genre': genre if genre else None,  # Filter by user-selected genre (or None for all genres)
    }

    # Define the URL of the GraphQL API endpoint
    url = 'https://graphql.anilist.co'

    # Make the HTTP POST request to the API
    response = requests.post(url, json={'query': query, 'variables': variables})
    lt = ""
    tt = ""
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract and print the response data
        data = response.json()
        top_10_media = data['data']['Page']['media']
        
        # Print the titles of the top 10 most popular media
        print(f"Top 10 Most Popular {media_type.capitalize()} in {genre.capitalize() if genre else 'All Genres'}:")
        for media in top_10_media:
            title = media['title']['userPreferred']
            lt = lt + f"{title}\n"
            tt = tt + f"{title}\n"
            popularity = media['popularity']
            #print(f"{title} - Popularity: {popularity}")
            
            resp = model.generate_content(f"write a brief description of the {title} {media_type} ")
            #convo.send_message(f"write a brief description of the {title} {media_type} ")
            lt  = lt+f"{resp.text}\n\n\n"
            #lt[title]=convo.last.text
            #print(lt[title])
            #print(convo.last.text)
    
            
    else:
        # Print an error message if the request failed
        print(f"Error: {response.status_code}")
        lt  = lt+f"Error: {response.status_code}"
    print(lt)
    mg = f"{lt}"
    print(type(mg))
        # send the response
    ctx.logger.info("Sending message to bob")
    #await ctx.send(sender, UAgentResponse(message=mg, type=UAgentResponseType.FINAL))
    await ctx.send(sender, Message(message=mg), Message(message=tt))
 
if __name__ == "__main__":
    agent.run()