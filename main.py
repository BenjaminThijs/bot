from client import Client

def retrieve_token():
    with open("token", "r") as token_file:
        return token_file.read()

if __name__ == "__main__":
    client = Client()
    client.run(retrieve_token())
