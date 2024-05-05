if __name__ == "__main__":
    from turtle_helper import move_turtle
    from command_detect import find_command
    from audio_record import record_audio
    from audio2text import convert_to_text

    while True:
        record_audio()
        convert_to_text()
        command = find_command()
        move_turtle(command)
        if command == "stop":
            break
