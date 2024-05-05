# importing text file

def find_command():
    with open("output.wav.txt", "r") as file:
        data = file.read()

    filtered_data = ""
    for chars in data:
        if chars.isalpha() or chars == " ":
            filtered_data += chars
    words = filtered_data.split(" ")
    print(words)

    count = 0
    keyword = " "
    for i in range(len(words)):
        if words[i].lower() in ["up", "down", "left", "right", "stop", "go"]:
            count += 1
            keyword = words[i].lower()

    if count > 1:
        print("Malfunction! Multiple commands given!")
        return
    elif count == 0:
        print("Command not understood: Pls include following instruction words: up, down, left, right, stop, go")
        return
    else:
        return keyword
