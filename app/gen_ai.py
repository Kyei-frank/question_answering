import csv
import openai
import os

# Set up the OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_answer(question, passage_data):
    """
    Uses a generative LLM to provide a direct answer based on the relevant passages.
    
    Parameters:
    - question (str): The user's question.
    - passage_data (list): List of dictionaries containing relevant passage text and metadata.
    
    Returns:
    - str: Direct answer from the generative model.
    """
    # Construct the prompt
    prompt = f"Question: {question}\n\n"
    for idx, passage in enumerate(passage_data):
        prompt += f"Passage {idx + 1}: {passage['text']}\n\n"
    prompt += "Answer: "

    # Make API call to OpenAI's engine
    response = openai.Completion.create(
        engine="davinci",  # Using the most capable model
        prompt=prompt,
        max_tokens=100,  # Limiting the response length
        n=1,  # Only one completion for reproducibility
        temperature=0.7  # Balance between randomness and determinism
    )

    ai_answer = response.choices[0].text.strip()

    # Save the output to the CSV
    file_exists = os.path.isfile('questions_answers_gen.csv')
    with open('questions_answers_gen.csv', 'a', newline='') as csv_file:
        fieldnames = [
            "Question", "Passage 1", "Relevance Score 1", "Passage 1 Metadata",
            "Passage 2", "Relevance Score 2", "Passage 2 Metadata", 
            "Passage 3", "Relevance Score 3", "Passage 3 Metadata", 
            "Generative AI Answer"
        ]
        
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # If file does not exist, write the header first
        
        writer.writerow({
            "Question": question,
            "Passage 1": passage_data[0]['text'] if len(passage_data) > 0 else None,
            "Relevance Score 1": passage_data[0]['score'] if len(passage_data) > 0 else None,
            "Passage 1 Metadata": passage_data[0]['metadata'] if len(passage_data) > 0 else None,
            "Passage 2": passage_data[1]['text'] if len(passage_data) > 1 else None,
            "Relevance Score 2": passage_data[1]['score'] if len(passage_data) > 1 else None,
            "Passage 2 Metadata": passage_data[1]['metadata'] if len(passage_data) > 1 else None,
            "Passage 3": passage_data[2]['text'] if len(passage_data) > 2 else None,
            "Relevance Score 3": passage_data[2]['score'] if len(passage_data) > 2 else None,
            "Passage 3 Metadata": passage_data[2]['metadata'] if len(passage_data) > 2 else None,
            "Generative AI Answer": ai_answer
        })

    return ai_answer

