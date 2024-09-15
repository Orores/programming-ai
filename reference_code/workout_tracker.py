import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt

class WorkoutTracker:
    """
    Short Description:
    This class provides functionalities to track and plot workout progress using JSON files for data storage.

    Methods:
    - add_workout_data(file_path: str, workout_data: dict):
        Adds workout data to the specified file.
    - save_to_file(file_path: str):
        Method to ensure data is saved to the file (kept for compatibility with unittests).
    - load_from_file(file_path: str) -> dict:
        Loads workout data from the specified file.
    - plot_workout_progress(file_path: str, exercise: str, plot_file: str):
        Plots workout progress for the specified exercise and saves the plot to a file.
    - execute(file_path: str, workout_data: dict, exercise: str, plot_file: str):
        Orchestrates the addition, saving, and plotting of workout data.
    """

    @staticmethod
    def add_workout_data(file_path: str, workout_data: dict):
        """
        Short Description:
        Adds workout data to the specified file.

        Parameters:
        file_path (str): Path to the file where workout data is stored.
            Example: "workout_data.json"
        workout_data (dict): Dictionary containing workout data.
            Example:
            {
                "date": "2023-10-01",
                "exercise": "bench_press",
                "sets": 3,
                "reps": [10, 8, 6],
                "weight": [100, 110, 120]
            }

        How to Use:
        This method takes the path to a JSON file and a dictionary containing workout data, adds the data to the file, and saves it.

        Usage Example:
        >>> workout_data = {
        >>>     "date": "2023-10-01",
        >>>     "exercise": "bench_press",
        >>>     "sets": 3,
        >>>     "reps": [10, 8, 6],
        >>>     "weight": [100, 110, 120]
        >>> }
        >>> WorkoutTracker.add_workout_data("workout_data.json", workout_data)
        """
        # Load existing data if file exists, otherwise create a new dictionary
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = defaultdict(dict)

        # Extract the date and exercise from the workout data
        date = workout_data["date"]
        exercise = workout_data["exercise"]

        # Ensure the date key exists in the dictionary
        if date not in data:
            data[date] = {}

        # Add the workout data to the dictionary
        data[date][exercise] = {
            "sets": workout_data.get("sets", []),
            "reps": workout_data.get("reps", []),
            "weight": workout_data.get("weight", [])
        }

        # Save the updated data back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def save_to_file(file_path: str):
        """
        Short Description:
        Method to ensure data is saved to the file.

        Parameters:
        file_path (str): Path to the file where workout data is stored.
            Example: "workout_data.json"

        How to Use:
        This method is kept for compatibility with unittests. It typically does not perform any action.

        Usage Example:
        >>> WorkoutTracker.save_to_file("workout_data.json")
        """
        # This method is kept for compatibility with the unittests
        pass

    @staticmethod
    def load_from_file(file_path: str) -> dict:
        """
        Short Description:
        Loads workout data from the specified file.

        Parameters:
        file_path (str): Path to the file where workout data is stored.
            Example: "workout_data.json"

        Returns:
        dict: Dictionary containing the loaded workout data.
            Example:
            {
                "2023-10-01": {
                    "bench_press": {
                        "sets": 3,
                        "reps": [10, 8, 6],
                        "weight": [100, 110, 120]
                    }
                }
            }

        How to Use:
        This method reads workout data from a specified JSON file and returns it as a dictionary.

        Usage Example:
        >>> data = WorkoutTracker.load_from_file("workout_data.json")
        >>> print(data)
        """
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        return {}

    @staticmethod
    def plot_workout_progress(file_path: str, exercise: str, plot_file: str):
        """
        Short Description:
        Plots workout progress for the specified exercise and saves the plot to a file.

        Parameters:
        file_path (str): Path to the file where workout data is stored.
            Example: "workout_data.json"
        exercise (str): The exercise to plot progress for.
            Example: "bench_press"
        plot_file (str): Path to the file where the plot should be saved.
            Example: "workout_plot.png"

        How to Use:
        This method generates a plot of workout progress for a specified exercise based on data from a JSON file and saves the plot to a specified file.

        Usage Example:
        >>> WorkoutTracker.plot_workout_progress("workout_data.json", "bench_press", "workout_plot.png")
        """
        data = WorkoutTracker.load_from_file(file_path)

        dates = []
        weights = []

        for date, exercises in sorted(data.items()):
            if exercise in exercises:
                dates.append(date)
                weights.append(max(exercises[exercise]["weight"]))

        plt.figure(figsize=(10, 6))
        plt.plot(dates, weights, marker='o', linestyle='-', color='b')
        plt.xlabel('Date')
        plt.ylabel('Weight Lifted (lbs)')
        plt.title(f'Progress for {exercise.capitalize()}')
        plt.grid(True)
        plt.savefig(plot_file)
        plt.close()  # Close the plot to avoid displaying it in interactive environments

    @staticmethod
    def execute(file_path: str, workout_data: dict, exercise: str, plot_file: str):
        """
        Short Description:
        Orchestrates the addition, saving, and plotting of workout data.

        Parameters:
        file_path (str): Path to the file where workout data is stored.
            Example: "workout_data.json"
        workout_data (dict): Dictionary containing workout data.
            Example:
            {
                "date": "2023-10-01",
                "exercise": "bench_press",
                "sets": 3,
                "reps": [10, 8, 6],
                "weight": [100, 110, 120]
            }
        exercise (str): The exercise to plot progress for.
            Example: "bench_press"
        plot_file (str): Path to the file where the plot should be saved.
            Example: "workout_plot.png"

        How to Use:
        This method uses the other methods to add workout data, save it to a file, and plot the progress.

        Usage Example:
        >>> workout_data = {
        >>>     "date": "2023-10-01",
        >>>     "exercise": "bench_press",
        >>>     "sets": 3,
        >>>     "reps": [10, 8, 6],
        >>>     "weight": [100, 110, 120]
        >>> }
        >>> WorkoutTracker.execute("workout_data.json", workout_data, "bench_press", "workout_plot.png")
        """
        WorkoutTracker.add_workout_data(file_path, workout_data)
        WorkoutTracker.save_to_file(file_path)
        WorkoutTracker.plot_workout_progress(file_path, exercise, plot_file)

# Example usage:
if __name__ == "__main__":
    workout_tracker = WorkoutTracker()
    workout_data = {
        "date": "2023-10-01",
        "exercise": "bench_press",
        "sets": 3,
        "reps": [10, 8, 6],
        "weight": [100, 110, 120]
    }
    workout_tracker.execute("workout_data.json", workout_data, "bench_press", "workout_plot.png")
