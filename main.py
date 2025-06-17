from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from transformers import AutoTokenizer, T5ForConditionalGeneration
import uvicorn

# Initialize FastAPI
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Load the model and tokenizer
model_path = "app/t5-small-hungarian-translator"
loaded_model = T5ForConditionalGeneration.from_pretrained(model_path)
loaded_tokenizer = AutoTokenizer.from_pretrained(model_path)

# Define input structure
class TextRequest(BaseModel):
    text: str

@app.get("/")
def home(request: Request):
    # Render the index.html template    
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
def generate_text(request: TextRequest):
    input_text = "translate English to Hungarian: " + request.text
    inputs = loaded_tokenizer(input_text, return_tensors="pt", truncation=True)
    outputs = loaded_model.generate(**inputs, num_beams=4, early_stopping=True)
    generated_text = loaded_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_text": generated_text}

# Health Check
@app.get("/health")
def read_root():
    return {"message": "T5 Model API is running"}

