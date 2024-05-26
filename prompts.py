import json
import time
from typing import List, Optional, Dict, Union
from pydantic import BaseModel, ValidationError
from groq import Groq
from groq._exceptions import BadRequestError
from medical_report_summarizer import Summarizer
from grocery_finder import GroceryStoreFetcher

client = Groq(
    api_key="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",
)

api_key = "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",
medical_report_path = "Sample-filled-in-MR.pdf",
model_name = "mixtral-8x7b-32768",


def get_user_first_prompt(
    nationality: str,
    body_part: str,
    preferred_diet: List[str],
    address: str,
    workout_plan: Union[int, str],
    age: str,
    allergies: List[str],
    medical_report: str = "",
) -> str:
    api_key = "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",
    medical_report_path = medical_report,
    model_name = "mixtral-8x7b-32768",

    if len(medical_report_path) > 4 :
        summarizer = Summarizer(api_key, model_name, medical_report_path)
        medical_report = summarizer.summarize_pdf()

    nationality_string = f"I am an {nationality}," if nationality else ""
    body_part_string = f"I want to take care of my {body_part}," if body_part else ""
    preferred_diet_string = (
        f"The diets that talk the most to me are {' and '.join(preferred_diet)},"
        if preferred_diet
        else ""
    )
    address_string = f"I live in {address}," if address else ""
    workout_plan_string = (
        f"I am working out {workout_plan} times a week," if workout_plan else ""
    )
    age_string = f"I am {age} years old," if age else ""
    allergies = f"I have {', '.join(allergies)} allergies," if allergies else ""
    medical_report_string = (
        f"My medical report says {medical_report}" if medical_report else ""
    )

    final_prompt = " ".join(
        [
            nationality_string,
            body_part_string,
            preferred_diet_string,
            address_string,
            workout_plan_string,
            age_string,
            allergies,
            medical_report_string,
        ]
    ).strip()

    return final_prompt


def get_user_final_prompt(user_prompt: str, diet_name: str, explanation: str) -> str:
    # Construct the prompt in a clear and structured manner
    beginning = (
        f"To refresh your memory, here is my personal information:\n{user_prompt}\n"
    )
    diet_plan = f"\nHere is the diet I chose from your last recommendation:\nDiet Name: {diet_name}\nExplanation: {explanation}\n"

    request = (
        "Based on this chosen diet, can you please provide me with a detailed nutrition plan for an entire week? "
        "The plan should include breakfast, lunch, and dinner for each day of the week. For each meal, please provide:\n"
        "1. The name of the meal\n"
        "2. A list of ingredients\n"
        "3. Instructions on how to prepare the meal\n"
        "Additionally, at the end, please provide the total quantities of each ingredient needed for the entire week in grams."
    )

    return beginning + diet_plan + request


def get_model_four_diets_answer(
    user_prompt: str, client, model_name: str = "mixtral-8x7b-32768"
):

    system_message = {
        "role": "system",
        "content": (
            "You are a helpful assistant. Your task is to generate four personalized diet plans for users based on their provided data. "
            "If a medical report is provided, you should give it more weight and ensure the nutrition plan adheres closely to the medical guidelines and recommendations."
            "You'll provide 4 different diet plans. The data includes medical reports, address, weights, workout plans, body parts they want to take care of, age, nationality, and dietary preferences (e.g., vegan, vegetarian, etc.). "
            "Each diet plan should be safe, healthy, and tailored to the user's specific needs and preferences. "
            "Ensure the diets are diverse and cater to different aspects of the user's needs and preferences. "
            "Please provide the output in the following JSON format strictly adhering to this schema:\n"
            "{\n"
            '    "diet_plans": [\n'
            "        {\n"
            '            "diet_name": "string",\n'
            '            "explanation": "string"\n'
            "        },\n"
            "        {\n"
            '            "diet_name": "string",\n'
            '            "explanation": "string"\n'
            "        },\n"
            "        {\n"
            '            "diet_name": "string",\n'
            '            "explanation": "string"\n'
            "        },\n"
            "        {\n"
            '            "diet_name": "string",\n'
            '            "explanation": "string"\n'
            "        }\n"
            "    ]\n"
            "}\n"
        ),
    }

    user_message = {"role": "user", "content": user_prompt}

    chat_completion = client.chat.completions.create(
        messages=[system_message, user_message],
        response_format={"type": "json_object"},
        model=model_name,
        temperature=0.3,
    )

    return chat_completion.choices[0].message.content


def get_detailed_nutrition_plan(
    user_final_prompt: str,
    client,
    model_name: str = "mixtral-8x7b-32768",
):

    system_message = {
        "role": "system",
        "content": (
            "You are a nutrition database that outputs detailed weekly meal plans in JSON. Your task is to generate a detailed nutrition plan for an entire week based on the provided diet name and explanation. "
            "The plan should include breakfast, lunch, and dinner for each day (Monday to Sunday). For each meal, provide the name of the meal, a list of ingredients in grams, and instructions on how to prepare it. "
            "At the end, provide the total quantities of each ingredient needed for the week in grams only irrespective of anything. "
            "Ensure the meals are balanced, healthy, and tailored to the user's needs.\n\n"
            "Please provide the output in the following JSON format strictly adhering to this schema and do not provide any other information:\n"
            "{\n"
            '  "week_plan": {\n'
            '    "Monday": {"breakfast": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "lunch": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "dinner": {"name": "string", "ingredients": ["string"], "instructions": "string"}},\n'
            '    "Tuesday": {"breakfast": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "lunch": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "dinner": {"name": "string", "ingredients": ["string"], "instructions": "string"}},\n'
            '    "Wednesday": {"breakfast": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "lunch": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "dinner": {"name": "string", "ingredients": ["string"], "instructions": "string"}},\n'
            '    "Thursday": {"breakfast": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "lunch": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "dinner": {"name": "string", "ingredients": ["string"], "instructions": "string"}},\n'
            '    "Friday": {"breakfast": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "lunch": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "dinner": {"name": "string", "ingredients": ["string"], "instructions": "string"}},\n'
            '    "Saturday": {"breakfast": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "lunch": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "dinner": {"name": "string", "ingredients": ["string"], "instructions": "string"}},\n'
            '    "Sunday": {"breakfast": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "lunch": {"name": "string", "ingredients": ["string"], "instructions": "string"}, "dinner": {"name": "string", "ingredients": ["string"], "instructions": "string"}}\n'
            "  },\n"
            '  "total_quantities (grams) ": {\n'
            '    "ingredient": "quantity "\n'
            "  }\n"
            "}\n"
        ),
    }

    user_message = {"role": "user", "content": user_final_prompt}

    chat_completion = client.chat.completions.create(
        messages=[system_message, user_message],
        temperature=0.3,
        model=model_name,
        response_format={"type": "json_object"},
    )

    return chat_completion.choices[0].message.content


def get_model_four_diets_answer_robust(
    user_prompt: str,
    client = Groq(
    api_key="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",
    ),
    model_name: str = "mixtral-8x7b-32768",
    attempts: int = 10,
):
    """
    Retrieves a robust answer from the model by making multiple attempts.

    Args:
        user_prompt (str): The user prompt for generating the answer.
        client: The client object for making API requests.
        model_name (str, optional): The name of the model to use. Defaults to "llama3-8b-8192".
        attempts (int, optional): The number of attempts to make. Defaults to 10.

    Returns:
        str: The generated answer.

    Raises:
        Exception: If a response cannot be obtained after multiple attempts.
    """
    for _ in range(attempts):
        try:
            return get_model_four_diets_answer(user_prompt, client, model_name)
        except BadRequestError as e:
            pass
    raise Exception("Failed to get a response after multiple attempts")


def get_detailed_nutrition_plan_robust(
    user_final_prompt: str,
    client,
    model_name: str = "mixtral-8x7b-32768",
    attempts: int = 10,
):

    for _ in range(attempts):
        try:
            return get_detailed_nutrition_plan(user_final_prompt, client, model_name)
        except BadRequestError as e:
            pass
    raise Exception("Failed to get a response after multiple attempts")

#
# def __main__(
#     model_name: str = "mixtral-8x7b-32768",
#     medical_report_path: str = None,
#     api_key: str = None,
# ):
#
#     nationality = input("What is your Nationality? ")
#     body_part = input("What body part do you want to take care of? ")
#     preferred_diet = input("What are your preferred diets? ").split(",")
#     address = input("What is your address? ")
#     if address:
#         fetcher = GroceryStoreFetcher(config_file="config.ini")
#         all_grocery_stores = fetcher.fetch_near_grocery_stores_by_address(address)
#     else:
#         address = ""
#         all_grocery_stores = []
#     workout_plan = input("How many times a week do you workout? ")
#     age = input("What is your age? ")
#     allergies = input("Do you have any allergies? ").split(",")
#     if medical_report_path:
#         summarizer = Summarizer(api_key, model_name, medical_report_path)
#         medical_report = summarizer.summarize_pdf()
#     else:
#         medical_report = ""
#     first_user_prompt = get_user_first_prompt(
#         nationality,
#         body_part,
#         preferred_diet,
#         address,
#         workout_plan,
#         age,
#         allergies,
#         medical_report,
#     )
#     ### First answer ####
#     first_answer = get_model_four_diets_answer_robust(first_user_prompt, client)
#     print(first_answer)
#     selected_diet = int(
#         input(
#             "Select the diet plan that you like the most and press enter to continue..."
#         )
#     )
#     suggested_diets = json.loads(first_answer)["diet_plans"][selected_diet - 1]
#     diet_name = suggested_diets["diet_name"]
#     explanation = suggested_diets["explanation"]
#     final_user_prompt = get_user_final_prompt(first_user_prompt, diet_name, explanation)
#     ### Second answer ###
#     second_answer = get_detailed_nutrition_plan_robust(final_user_prompt, client)
#     second_answer_json = json.loads(second_answer)
#     ## Add the grocery list to the final output ##
#     second_answer_json["grocery_list"] = all_grocery_stores
#     ### Save the final output to a json a json file ###
#     with open("nutrition_plan.json", "w") as file:
#         json.dump(second_answer_json, file, indent=4)
#
