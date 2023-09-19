import os
from PyPDF2 import PdfReader
import re
from datasets import Dataset
import pandas as pd

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_reader = PdfReader(pdf_path)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to extract job titles using a regular expression
def extract_job_titles(text):
    job_title_pattern = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\b'  # Matches capitalized words (potential job titles)
    job_titles = re.findall(job_title_pattern, text)
    return job_titles

# Function to extract skills using a regular expression
def extract_skills(text, skills_keywords):
    skills_pattern = r'\b(?:' + '|'.join(re.escape(skill) for skill in skills_keywords) + r')\b'
    skills = re.findall(skills_pattern, text, re.IGNORECASE)
    return skills

# Function to extract education details using a regular expression
def extract_education(text):
    education_pattern = r'((?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:in|at)\s+(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*))'
    education = re.findall(education_pattern, text)
    return education

# Specify the path to the folder containing your PDFs
folder_path = r'C:\Users\TAPESH\Downloads\resumedataset\data\data\SALES'  # Replace with your actual folder path

# Create a folder to store the extracted details if it doesn't exist
output_folder = 'C:\\Users\\TAPESH\\Downloads\\extracted_details'  # Replace with your desired output folder path

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List of skills keywords (customize as needed)
skills_keywords = ["Python", "Machine Learning", "SQL", "Data Analysis", "Project Management"]

# List all PDF files in the folder
pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

# Iterate through each PDF file and extract text and details
for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Extract job titles from the PDF
    job_titles = extract_job_titles(pdf_text)
    
    # Extract skills from the PDF
    skills = extract_skills(pdf_text, skills_keywords)
    
    # Extract education details from the PDF
    education = extract_education(pdf_text)
    
    # Save the extracted details to a text file
    output_file_path = os.path.join(output_folder, f'{pdf_file}_details.txt')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"Details from {pdf_file}:\n")
        output_file.write(f"Job Titles: {', '.join(job_titles)}\n")
        output_file.write(f"Skills: {', '.join(skills)}\n")
        output_file.write(f"Education: {', '.join(education)}\n")

    print(f"Details saved to: {output_file_path}")

print("Extraction and saving of details completed.")

# Load your CSV file using pandas
df = pd.read_csv('C:\\Users\\TAPESH\\Downloads\\training_data.csv')

# Define the keywords you want to filter for
keywords = ["data analyst", "python", "machine learning"]

# Filter job descriptions that contain any of the keywords
filtered_df = df[df['job_description'].str.lower().str.contains('|'.join(keywords), na=False, case=False)]

# Create a new dataset in the required format
dataset_dict = {
    'train': {
        'description': filtered_df['job_description'].tolist()
    }
}

# Convert the dictionary to a dataset
custom_dataset = Dataset.from_dict(dataset_dict)

# Define the output folder for matching job descriptions
output_folder = 'matching_job_descriptions'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through the matching job descriptions and save them to the output folder
for idx, description in enumerate(custom_dataset['train']['description']):
    # Define a unique filename (you can customize the naming convention)
    filename = f'matching_description_{idx + 1}.txt'
    output_path = os.path.join(output_folder, filename)

    # Save the matching job description to a text file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(description)

    print(f"Matching description saved to: {output_path}")

print("Matching job descriptions saved to the output folder.")
