from fastapi import FastAPI


app = FastAPI()


""""
what i need is to make api to handle users support 

save the the user complaint into the db and then run background job to generate response and

summary ....... for agent to handle 


step 1 create migrations and tables
step 2 create api to create the support ticket and return id
step 3 send the user input to worker
step 4 insert ticket detail with response to the user (email with draft)
step 5 get notification using SSE
step 6 have comment section for the users (POST + SSE) 

"""

@app.get('/')
def home():
    return "Home"











