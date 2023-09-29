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

# Calculating Accuracy for Top-1 and Top-3
# Load the rated CSV file (evaluation_rated.csv)
with open("evaluation_rated.csv", "r", newline="", encoding="utf-8") as rated_file:
    reader = csv.DictReader(rated_file)
    
    # Initialize variables to count top-1 and top-3 correct answers
    top_1_correct = 0
    top_3_correct = 0

    for row in reader:
        question = row["Question"]
        is_relevant_1 = row["Is Passage 1 Relevant?"].strip().lower()  # Convert to lowercase for comparison
        is_relevant_2 = row["Is Passage 2 Relevant?"].strip().lower()
        is_relevant_3 = row["Is Passage 3 Relevant?"].strip().lower()
        
        # Check if the first passage is relevant (top-1)
        if is_relevant_1 == "yes":
            top_1_correct += 1
        
        # Check if at least one of the top-3 passages is relevant (top-3)
        if is_relevant_1 == "yes" or is_relevant_2 == "yes" or is_relevant_3 == "yes":
            top_3_correct += 1

# Calculate the top-1 and top-3 accuracy percentages
total_queries = 10
top_1_accuracy = (top_1_correct / total_queries) * 100
top_3_accuracy = (top_3_correct / total_queries) * 100

# Save the accuracy results to a new CSV file (performance.csv)
with open("performance.csv", "w", newline="", encoding="utf-8") as performance_file:
    writer = csv.writer(performance_file)
    
    # Write the header row
    writer.writerow(["Top 1 Accuracy", "Top 3 Accuracy"])
    
    # Write the accuracy values
    writer.writerow([top_1_accuracy, top_3_accuracy])

print("Performance metrics have been saved to performance.csv")
