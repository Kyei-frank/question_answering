import csv

# Open the evaluation.csv file for reading
with open("evaluation.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    
    # Define the headers for the rated CSV file
    rated_headers = ["Question", "Passage 1", "Is Passage 1 Relevant?", "Passage 2", "Is Passage 2 Relevant?", "Passage 3", "Is Passage 3 Relevant?"]

    # Open the new CSV file for writing
    with open("evaluation_rated.csv", "w", newline="", encoding="utf-8") as rated_file:
        writer = csv.DictWriter(rated_file, fieldnames=rated_headers)
        writer.writeheader()

        for row in reader:
            question = row["Question"]
            passage1 = row["Passage 1"]
            passage2 = row["Passage 2"]
            passage3 = row["Passage 3"]
            
            # Display the question and passages
            print("Question:")
            print(question)
            print("\nPassage 1:")
            print(passage1)
            print("\nPassage 2:")
            print(passage2)
            print("\nPassage 3:")
            print(passage3)
            
            # Get manual input for rating
            rating1 = input("\nIs Passage 1 Relevant? (Yes/No): ").strip()
            rating2 = input("Is Passage 2 Relevant? (Yes/No): ").strip()
            rating3 = input("Is Passage 3 Relevant? (Yes/No): ").strip()
            
            # Write the ratings to the new CSV file
            writer.writerow({
                "Question": question,
                "Passage 1": passage1,
                "Is Passage 1 Relevant?": rating1,
                "Passage 2": passage2,
                "Is Passage 2 Relevant?": rating2,
                "Passage 3": passage3,
                "Is Passage 3 Relevant?": rating3
            })
            
            # Print a separator for readability
            print("\n" + "=" * 40 + "\n")

print("Ratings have been saved to evaluation_rated.csv")
