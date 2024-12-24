import datetime
import random

class Plant:
    def __init__(self, name, species, last_watered=None):
        self.name = name
        self.species = species
        self.last_watered = last_watered

    def water(self):
        self.last_watered = datetime.date.today()
        print(f"{self.name} watered successfully!")

    def plant_condition(self):
        if self.last_watered:
            days = (datetime.date.today() - self.last_watered).days
            if days <= 7:
                return "Good and healthy."
            else:
                return "Needs watering."
        return "Has never been watered."

def daily_tips():
    tips = [
        "Rotate your plants regularly to ensure even growth.",
        "Check for pests and diseases regularly.",
        "Use a well-draining potting mix for healthy roots.",
        "Adjust watering frequency based on the environment.",
        "Consider using a humidifier for plants that prefer high humidity."
    ]
    return random.choice(tips)

def main():
    plants = []

    while True:
        print("\nPlant Care App Menu:")
        print("1. Add a plant")
        print("2. Water a plant")
        print("3. Check plant health")
        print("4. Get a daily tip")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter plant name: ")
            species = input("Enter plant species: ")
            plant = Plant(name, species)
            plants.append(plant)
            print(f"{name} added successfully!")
        elif choice == '2':
            if not plants:
                print("No plants added yet.")
                continue

            for i, plant in enumerate(plants):
                print(f"{i+1}. {plant.name}")

            plant_index = int(input("Enter the number of the plant to water: ")) - 1

            if 0 <= plant_index < len(plants):
                plants[plant_index].water()
            else:
                print("Invalid plant number.")
        elif choice == '3':
            if not plants:
                print("No plants added yet.")
                continue

            for plant in plants:
                print(f"\nPlant Name: {plant.name}")
                print(f"Species: {plant.species}")
                print(f"Condition: {plant.plant_condition()}")
        elif choice == '4':
            print(f"Daily Tip: {daily_tips()}")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()