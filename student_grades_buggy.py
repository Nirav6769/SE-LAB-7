def average_marks(marks_csv):
    marks = [int(m) for m in marks_csv.split(',')]
    return round(sum(marks) / len(marks), 2)


def parse_srn(srn):
    return srn[:4], int(srn[6:8]), srn[8:10]


def short_name(full_name):
    first, last = full_name.split()
    return first[0].upper() + ". " + last.capitalize()


def main():
    print("==== Running average_marks (original buggy version) ====")
    user_input = input("Enter marks as CSV (e.g. 78,85,92): ")
    result = average_marks(user_input)
    print("Average Marks:", result)

    print("\n==== Running parse_srn ====")
    user_input = input("Enter an SRN (e.g. PES1UG23CS123): ")
    result = parse_srn(user_input)
    print("Campus, Year and Dept:", result)

    print("\n==== Running short_name ====")
    user_input = input("Enter first and last name (e.g. ravi kumar): ")
    result = short_name(user_input)
    print("Short Name:", result)


if __name__ == "__main__":
    main()
