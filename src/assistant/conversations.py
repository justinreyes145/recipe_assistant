import shelve

# Method to save conversation into a shelf
def save_conversation(conv_id, title):
    # Opening the convos file and writing conv_id key with associated title value
    with shelve.open("convos_db", writeback=True) as convos_shelf:
        convos_shelf[conv_id] = title

# Method to save conversation into a shelf
def retrieve_conversations():
    # Opening the convos file and writing conv_id key with associated title value
    with shelve.open("convos_db") as convos_shelf:
        return list(convos_shelf.values())