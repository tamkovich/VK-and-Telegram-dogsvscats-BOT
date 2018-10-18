import command_system


def hello():
    message = "Привет мир!"
    return message, ""


hello_command = command_system.Command()

hello_command.keys = ["привет", "hello", "hi"]
hello_command.description = "Поприветствую тебя"
hello_command.process = hello
