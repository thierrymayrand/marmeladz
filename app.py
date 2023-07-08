import openai
import json
from message_manager import MessageManager

message_manager = MessageManager()



openai.api_key = "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"

functions = [
            {
                "name": "get_availabilities",
                "description": "Get the next availabilities to schedule appointment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "day": {
                            "type": "string",
                            "description": "The day prefered to check availabilities",
                        }
                    },
                    "required": [],
                },
            },
            {
                "name": "book_appointment",
                "description": "Book appointment for a given date and time. Must first confirm that the slot is available",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date_time": {
                            "type": "string",
                            "description": "The day and time of the available slot",
                        }
                    },
                    "required": ["date_time"],
                },
            }
        ]

def create_variable(name, value):
    globals()[name] = value


class Dataframe:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Plot:
    def __init__(self, dataframe, x, y, summary, title, chart_type):
        self.dataframe = dataframe
        self.x = id
        self.y = y
        self.summary = summary
        self.title = title
        self.chart_type = chart_type

username = "nick@dbee.io"
password = "N00b1234"
security_token = "C7z7EdnaWTmTOg5FgNr3dzMC"



def get_availabilities(date="Today"):
     
    completed_task = {
    "message": f"Our next avalabilities are today afternoon or tommorow morning"
    }  
    return json.dumps(completed_task)

messages = [
{"role": "system", "content": "You are a booking agent. You're job is to answer user questions and get them to book an appointment.You work for a company that finds jobs for people."},
{"role": "assistant", "content": f"Hey Thierry are you still looking for a job ?"}
]
def book_appointment(date_time):
    completed_task = {
    "message": f"I booked you're appointment for {date_time}"
    }  
    return json.dumps(completed_task)

def run_conversation(messages):
    function_looper = True
    looper = 0
   
    while True:
        # Step 1: send the conversation and available functions to GPT
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]
        
        
        useFunc = False
        # Step 2: check if GPT wanted to call a function
        if response_message.get("function_call") or response_message.get("manipulate_df"):
            
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_availabilities": get_availabilities,
                "book_appointment": book_appointment,
            }  # only one function in this example, but you can have multiple
            function_name = response_message["function_call"]["name"]
            fuction_to_call = available_functions[function_name]
            
            function_args = json.loads(response_message["function_call"]["arguments"])
            
            if function_name == "get_availabilities":
                useFunc = True
                function_response = fuction_to_call(
                )
            if function_name == "book_appointment":
                useFunc = True
                function_response = fuction_to_call(
                    date_time=function_args.get("date_time")
                )

            if useFunc == True:
                # Step 4: send the info on the function call and function response to GPT
                messages.append(response_message)  # extend conversation with assistant's reply
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
                print(messages) 
            
        if useFunc == False :
            final_response = response_message["content"]
            
            messages.append(response_message)
            return final_response
            messages.append(
                {
                    "role": "user",
                    "content": "execute the plan by taking one of the actions ",
                }
            )
        
                
