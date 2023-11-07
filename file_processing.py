import os
import random
import shutil

# Define the paths to your main folder, training folder, and testing folder
main_folder = "data"
training_folder = "Trainning"
testing_folder = "Testing"

# Create the training and testing folders if they don't exist
if not os.path.exists(training_folder):
    os.makedirs(training_folder)
if not os.path.exists(testing_folder):
    os.makedirs(testing_folder)

# Define the split ratio (e.g., 90% for training, 10% for testing)
split_ratio = 0.9

# Loop through the sub-folders in the main folder
for subfolder_name in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder_name)

    if os.path.isdir(subfolder_path):
        # Create sub-folders in the training and testing folders
        training_subfolder_path = os.path.join(training_folder, subfolder_name)
        testing_subfolder_path = os.path.join(testing_folder, subfolder_name)

        if not os.path.exists(training_subfolder_path):
            os.makedirs(training_subfolder_path)
        if not os.path.exists(testing_subfolder_path):
            os.makedirs(testing_subfolder_path)

        # Get the list of files in the current sub-folder
        files = os.listdir(subfolder_path)

        # Calculate the number of files to put in the training set
        num_training_files = int(len(files) * split_ratio)

        # Randomly shuffle the list of files
        random.shuffle(files)

        # Split the files into training and testing sets
        training_files = files[:num_training_files]
        testing_files = files[num_training_files:]

        # Copy files to the training and testing sub-folders
        for file_name in training_files:
            source_path = os.path.join(subfolder_path, file_name)
            destination_path = os.path.join(training_subfolder_path, file_name)
            shutil.copy(source_path, destination_path)

        for file_name in testing_files:
            source_path = os.path.join(subfolder_path, file_name)
            destination_path = os.path.join(testing_subfolder_path, file_name)
            shutil.copy(source_path, destination_path)

print("Data split into training and testing sets.")
