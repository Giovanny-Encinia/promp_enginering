import panel as pn
from api_completion import get_completion_from_messages, connect_api


def transform_input_panel_to_input_openai(last_conversation: list) -> list:
    """
    Transform the input panel of a conversation to the OpenAI format.

    Parameters
    ----------
    last_conversation : list of dict
        The list containing dictionaries representing the conversation messages.

    Returns
    -------
    list of dict
        A new list of dictionaries with "role" and "content" keys for each message.

    Notes
    -----
    This function converts the input panel of a conversation to the OpenAI format,
    where each message dictionary is transformed to have "role" and "content" keys.
    The "role" key specifies the role of the message sender (e.g., "user" or "assistant"),
    and the "content" key contains the actual content of the message.

    Example
    -------
    last_conversation = [
        {"user": "Hi, can you help me with something?"},
        {"assistant": "Sure, I'd be happy to help!"},
        {"user": "Great! Here's my question..."},
    ]
    transformed_messages = transform_input_panel_to_input_openai(last_conversation)
    # Output:
    # [
    #     {"role": "user", "content": "Hi, can you help me with something?"},
    #     {"role": "assistant", "content": "Sure, I'd be happy to help!"},
    #     {"role": "user", "content": "Great! Here's my question..."},
    # ]
    """
    messages_transformed = [
        {"role": [*dict_][0], "content": dict_[[*dict_][0]]}
        for dict_ in last_conversation
    ]
    return messages_transformed


def conversation(chat: list):
    """
    Process a chat conversation and generate a response from the assistant.

    Parameters
    ----------
    chat : list of dict
        The list containing dictionaries representing the conversation messages.

    Returns
    -------
    None

    Notes
    -----
    This function processes a chat conversation, extracts the user's query, and
    generates a response from the assistant using the 'get_completion_from_messages' function.
    It updates the 'messages' list with the new user query and the assistant's response.

    The 'get_completion_from_messages' function and the 'widget_chat_box' variable are
    assumed to be defined elsewhere.

    Example
    -------
    chat = [
        {"user": "Hi, can you help me with something?"},
        {"assistant": "Sure, I'd be happy to help!"},
    ]
    conversation(chat)
    # After processing, the 'messages' list will be updated with the new user query
    # and assistant's response.
    """
    # {"you": "content, write something"} to {"role": "user", "content": "..."}

    # there is a query from the customer
    if chat[-1].get("user"):
        new_sentence = {"role": "user", "content": chat[-1]["user"]}
        messages.append(new_sentence)
        response = get_completion_from_messages(messages)
        messages.append({"role": "assistant", "content": response})
        widget_chat_box.append({"assistant": response})
    else:
        pass


def chat_box(values: list) -> pn.widgets.ChatBox:
    """
    Create a chatbox widget with user and assistant messages.

    Parameters
    ----------
    values : list of dict
        The list containing dictionaries representing the chat messages.

    Returns
    -------
    pn.widgets.ChatBox
        A Panel interactive widget with user and assistant messages.

    Notes
    -----
    This function creates a chatbox widget using Panel (pn) library, displaying
    user and assistant messages. The 'values' parameter should be a list of dictionaries,
    where each dictionary represents a message with "user" or "assistant" as keys
    and message content as values.

    The chatbox allows users to interact with messages and provides features like
    allowing messages, adding likes, and displaying icons for user and assistant roles.

    Example
    -------
    values = [
        {"user": "Hi, can you help me with something?"},
        {"assistant": "Sure, I'd be happy to help!"},
    ]
    chatbox_widget = chat_box(values)
    # Display the chatbox widget in a Panel app or layout.
    """
    chat_ = pn.widgets.ChatBox(
        value=values,
        allow_messages=True,
        allow_likes=True,
        primary_name="user",
        message_icons={
            "user": "https://user-images.githubusercontent.com/42288570/246667322-33a2a320-9ea3-4e79-8fb8-fcb5b6eac9c0.png",
            "assistant": "https://user-images.githubusercontent.com/42288570/246667325-ad4e3434-d173-4463-bb98-5c5d4a892b25.png",
        },
    )

    return chat_


connect_api()
content = """As a call center staff member, you are tasked with helping people with problems related to their internet\
 connection. Here's the correct dialogue you should follow:

1. Introduction:
   - You: "Hello, this is Assistant AI. May I know your name, please?"

2. Ask about the problem:
   - You: "Thank you, [Customer's Name]. How can I assist you with your internet connection today?"

3. Troubleshooting:
   - Customer: "The modem has a red light."
   - You: "I apologize for the inconvenience. This issue might be related to the outer wires.\
    I recommend contacting a professional technician for further assistance. Here's a number\
     you can reach them at: 888888-99."

   - Customer: "The internet is slow."
   - You: "I'm sorry to hear that. Please try disconnecting the modem and wait for 15 seconds\
    before connecting it again. This often helps improve the internet speed."

   - Customer: "The phone is not working."
   - You: "I apologize for the inconvenience. If the phone is not functioning properly,\
    I recommend replacing it with a new one."

   - Customer: (Asks another question)
   - You: "I'm sorry, but for that specific issue, I would advise you to contact your service provider for assistance."

4. Check if the problem is resolved:
   - You: "Have any of the issues been resolved, [Customer's Name]? If not, let's try the instructions\
    provided earlier again."

5. If all problems are solved:
   - You: "Great news! If all your issues have been resolved, I'm glad I could be of help."

6. Ending on a light note:
   - You: "Thank you for reaching out to us. Before you go, here's a joke for you: [Share a light-hearted joke].\
    Have a fantastic day!"

Remember to be courteous and patient while assisting customers with their internet connection problems.
"""
messages = [{"role": "system", "content": content}]

value = [{"assistant": "You can ask for my help.."}]
widget_chat_box = chat_box(value)
interactive_chat = pn.bind(conversation, widget_chat_box)
pn.Column(widget_chat_box, interactive_chat).servable()
