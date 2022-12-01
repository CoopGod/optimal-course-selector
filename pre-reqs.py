"""
This program takes in courses and their prereqs 
and returns which courses depend on each other
Author: Cooper Goddard
Date Init: 2022-11-30
Date Fin: 2022-12-01
"""


def get_courses() -> tuple[dict[list[list]], list[str]]:
    """
    Gets the courses and their prereqs in a dictionary.
    user should type in the title of their course,
    then the pre-reqs for that course with or/and to separate.
    stop to break.
    """
    courses = {}
    course_titles = []
    # get user submissions
    while True:
        course_title = input("Course Title: ")
        if course_title.lower() == "stop":  # break from loop
            break

        # get pre-reqs and cleanup string
        course_titles.append(course_title)
        course_prereqs_input = input("Course Prerequisites: ").strip().replace(" ", "")

        # process prereqs like so: 100 or 200 and 300 --> [[100, 200], [300]]
        if course_prereqs_input == "":
            courses[course_title] = []
        else:
            course_prereqs = course_prereqs_input.split("and")
            for i in range(len(course_prereqs)):
                course_prereqs[i] = course_prereqs[i].split("or")
            # add to dictionary
            courses[course_title] = course_prereqs

    return courses, course_titles


def sort_courses(
    courses: dict[list[list[str]]], course_titles: list[str]
) -> tuple[list[str], list[list[str]]]:
    """
    Uses a greedy algorithm to find the most prudent/necessary courses.
    """
    needed_courses = course_titles
    must_decide_courses = []

    # find needed courses based on "must haves"
    for key in list(courses.keys()):
        for list_index in range(len(courses[key])):
            current_set = courses[key][list_index]
            if len(current_set) == 1 and current_set[0] not in needed_courses:
                needed_courses.append(current_set[0])

    # find all other courses and add if they do not exist already
    for key in list(courses.keys()):
        for list_index in range(len(courses[key])):
            current_set = courses[key][list_index]

            # check if inside needed_courses already
            found = False
            for course_index in range(len(current_set)):
                if current_set[course_index] in needed_courses:
                    found = True
                    break
            if not found:
                must_decide_courses.append(current_set)

    return needed_courses, must_decide_courses


def find_best_options(course_lists: list[str]) -> tuple[list[str], list[list[str]]]:
    """
    Uses a greedy algorithm to find to best possible courses.
    The goal being the smallest amount of courses possible
    """
    # create dictionary with courses as key values, adding for duplicates found
    course_duplicates = {}
    for course_list in course_lists:
        for course in course_list:
            result = course_duplicates.get(course, None)
            if result == None:
                course_duplicates[course] = 1
            else:
                course_duplicates[course] = result + 1

    # search course lists for best option
    best_options = []
    undecided_options = []
    for course_list in course_lists:
        best_option = []
        best_value = 0
        for course in course_list:
            # check against duplicates. search for highest
            current_course_value = course_duplicates.get(course)

            # if best current option, remove other and update value
            if current_course_value > best_value:
                best_option = [course]
                best_value = current_course_value

            # if tied as best current option, add to array
            elif current_course_value == best_value:
                best_option.append(course)

        # if only one best option, it must be best
        if len(best_option) == 1:
            for option in best_option:
                best_options.append(option)
        # if there is a tie between best options, add to separate array
        else:
            undecided_options.append(best_option)

    # remove duplicates and return
    best_options = list(dict.fromkeys(best_options))
    return best_options, undecided_options


def display_results(
    needed_courses: list[str],
    optimal_courses: list[str],
    undecided_courses: list[list[str]],
) -> None:
    print("NEEDED COURSES:")
    print(", ".join(needed_courses) + "\n")
    if len(optimal_courses) > 0:
        print("OPTIMAL COURSES:")
        print(", ".join(optimal_courses) + "\n")
    if len(undecided_courses) > 0:
        print("UNDECIDED COURSES:")
        display_list = []
        for section in undecided_courses:
            display_list.append(" or ".join(section))
        print(" | ".join(display_list))


def main() -> None:
    courses, course_titles = get_courses()
    needed_courses, undecided_courses = sort_courses(courses, course_titles)
    optimal_courses, undecided_courses = find_best_options(undecided_courses)

    display_results(needed_courses, optimal_courses, undecided_courses)

    return


if __name__ == "__main__":
    main()
