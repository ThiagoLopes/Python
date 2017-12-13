import io
import sys
import random

###############################################################################
# By changing the stdout to a 'buffer file' you can manipulate all its outputs#
# as a 'file like' and even save that buffer                                  #
###############################################################################


def return_a_number():
    r = random.SystemRandom()
    return r.randint(1, 100)


def save_file(c):
    with open('output.txt', 'w') as f:
        f.write(c)


def main():
    # lets make stdout copy
    temp = sys.stdout

    # create a string buffer
    buff = io.StringIO()

    # now stdout is a file like
    sys.stdout = buff

    # this print use stdout
    print('Lets start', file=temp)

    ###############################################
    # let's imagine that you want to              #
    # debug(print) all the even numbers.           #
    # an easier way to sort out all these outputs #
    # is to change their output(print) to a file. #
    ###############################################

    for i in range(100):
        r = return_a_number()
        if r % 2 == 0:
            print(r, " ")

    # pass all value in buffer to save
    print('Save debug to a file', file=temp)
    save_file(buff.getvalue())

    print('Is done', file=temp)


if __name__ == '__main__':
    main()
