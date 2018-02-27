import inotify.adapters
import shutil

copyAction = ['IN_CREATE','IN_OPEN','IN_MODIFY','IN_CLOSE_WRITE']

def copyEvent(passedList):
    flag = True
    for i, j in zip(passedList,copyAction):
        if (i == j):
            pass
        else:
            flag = False
    return flag

def _main():
    try:
        i = inotify.adapters.Inotify()
        i.add_watch('./Source')

        flag_cp_event = False
        eventList = []
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            print("*************\nPATH=[{}] FILENAME=[{}] EVENT_TYPES={}\n************".format(path, filename, type_names))
            eventList += [type_names[0]]

            # print(eventList)
            if len(eventList) == 4:
                if flag_cp_event:
                    if 'IN_CLOSE_WRITE' == eventList[-1]:
                        flag_cp_event = False
                    eventList = []

                if copyEvent(eventList):
                    shutil.copy2(f'./Source/{filename}',f'./Destination/{filename}')
                    print("\nDone!")
                    eventList = []
                    flag_cp_event = True
    except KeyboardInterrrupt:
        print("You cancelled the program")
        exit()

if __name__ == '__main__':
    _main()