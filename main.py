from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def userdata():
  return {'Saludo': 'hola'}

