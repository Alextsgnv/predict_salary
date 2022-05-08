import os
import pickle

path = os.getcwd()


def get_list_feature() -> tuple:
    with open("./media/features/levels", "rb") as file:
        levels = pickle.load(file)
    with open("./media/features/other", "rb") as file:
        other_col = pickle.load(file)
    with open("./media/features/main_skills", "rb") as file:
        main_skills = pickle.load(file)
    with open("./media/features/skills", "rb") as file:
        dict_skills = pickle.load(file)

    return other_col, main_skills, dict_skills, levels
