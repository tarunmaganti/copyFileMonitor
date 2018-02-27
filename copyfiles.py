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

def copyEventSubset(passedList,requiredList):
    flag = True
    for i, j in zip(passedList,requiredList):
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
            #print("*************\nPATH=[{}] FILENAME=[{}] EVENT_TYPES={}\n************".format(path, filename, type_names))
            eventList += [type_names[0]]

            # print(eventList)
            if len(eventList) > 0 and len(eventList) < 4:
                if copyEventSubset(eventList,copyAction[0:len(eventList)]):
                    eventList = []

            if len(eventList) == 4:
                if flag_cp_event:
                    if 'IN_CLOSE_WRITE' == eventList[-1]:
                        flag_cp_event = False
                    eventList = []

                if copyEvent(eventList):
                    i.remove_watch('./Source')
                    shutil.copy2(f'./Source/{filename}',f'./Destination/{filename}')
                    i.add_watch('./Source')
                    print("\nDone!")
                    eventList = []
                    flag_cp_event = True
                    
            print(eventList)
    except KeyboardInterrupt:
        print("\b\bTschüss!!!")
        exit()

if __name__ == '__main__':
    _main()