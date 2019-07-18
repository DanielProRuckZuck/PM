import csv


def load_file():
    try:
        f = open("Datenbasis_GPM_Prince.csv", "r")
        pm_lines = f.readlines()
        f.close()
    except:
        print("Can't open the file!")
        pm_lines = []
    return pm_lines


def data_to_lists(pm_lines):
    """creates gpm_dic and prince_dict and saves data as key and value in it"""
    if pm_lines:
        del pm_lines[0]  # remove header line
        gpm_dict = {}  # create empty dictionary
        prince_dict = {}  # create a second empty dict
        for line in pm_lines:  # walk through the file line by line
            entries = line.split(';')  # split line into elements
            entries = [e.strip() for e in entries[:3]]  # first 3 columns only, remove blanks
            if entries[1] == "gpm":
                gpm_dict[entries[0]] = entries[2]
            elif entries[1] == "prince2":
                prince_dict[entries[0]] = entries[2]
            else:
                print("entries[1]", entries[1], "error")

        return gpm_dict, prince_dict


def choose_pm_dict(user_question, gpm_dict, prince_dict):
    """method searches for gpm or prince2 in user_question and choose the right dict"""
    question_list = user_question.lower().strip(".").strip(",").strip(";").strip("!").strip(":").strip("?").strip(
        "-").split()
    basic_word = ""
    for word in question_list:

        if word.lower() == "/help":
            return_string = str(
                "Ich kann dir folgendes sagen\n Zu GPM:" + str(gpm_dict.keys()) + "\nUnd zu Prince2: " + str(
                    prince_dict.keys()))
            return return_string

        elif word.lower() == "gpm":
            basic_word = "GPM"
            return_string = print_value_of_dict(question_list, gpm_dict, basic_word)
            return return_string

        elif word.lower() == "prince2":
            basic_word = "Prince2"
            return_string = print_value_of_dict(question_list, prince_dict, basic_word)
            return return_string

    if basic_word == "":
        return "Bitte fragen Sie erneut und geben Sie an ob Sie nach Definitionen von GPM oder " \
               "Prince2 suchen. mit dem Befehl \n /help können Sie alle verfügbaren Stichwörter finden."


def print_value_of_dict(user_question, dictionary, basic_word):
    checker = ""
    for word in user_question:
        if word in dictionary:
            checker = "something"
            answer_string = basic_word + " " + word + " : " + dictionary[word]
            return answer_string

    if checker == "":
        return "Im Dictionary von " + basic_word + " wurde in ihrer Anfrage kein Schlüsselwort gefunden."


pm_lines_loaded = load_file()
gpm_dict, prince_dict = data_to_lists(pm_lines_loaded)
