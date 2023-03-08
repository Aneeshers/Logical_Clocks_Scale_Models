import matplotlib.pyplot as plt


def plot_msg_queue_len_over_time(port, maxtick, seperated):

    # Get time data from P1
    filename = "logs/" + str(port) + "time.txt"
    T = open(filename,mode='r')
    
    # read all lines at once
    T_all_of_it = T.read()
    
    # close the file
    T.close()

    # Get msg queue len from P1
    filename = "logs/" + str(port) + "msgqueulen.txt"
    MSQ = open(filename, mode='r')
    
    # read all lines at once
    MSQ_all_of_it = MSQ.read()
    
    # close the file
    MSQ.close()

    x = T_all_of_it.split(",")

    for i in range(len(x) - 1):
        x[i] = round(float(x[i]), 3)

    

    y = MSQ_all_of_it.split(",")
    for l in range(len(y) - 1):
        y[l] = int(y[l])
    m = min(len(x), len(y))

    if seperated:
        plt.figure()
    plt.plot(x[:m - 1],y[:m - 1])
    if seperated:
        plt.title(str(port) + " MSQ_QUEUE_LEN over TIME" + " TickMax (Full range)=" + str(maxtick))
    else:
        plt.title("(ALL Machines) MSQ_QUEUE_LEN over TIME" + " TickMax (Full range)=" + str(maxtick))
    plt.xlabel("time (seconds)")
    plt.ylabel("MSG_QUEUE_LEGNTH")
    if seperated:
        plt.savefig("figures/" + str(maxtick) + "/" + "FullRange" + "/" + str(port) +  " MSQ_QUEUE_LEN over TIME" + " TickMax (Full range)=" + str(maxtick) + ".pdf")
    else:
        plt.savefig("figures/" + str(maxtick) + "/" + "FullRange" + "/" + "(ALL Machines) MSQ_QUEUE_LEN over TIME" + " TickMax (Full range)=" + str(maxtick) + ".pdf")

def plot_logical_clock_over_time(port, maxtick, seperated):

    # Get time data from P1
    filename = "logs/" + str(port) + "time.txt"
    T = open(filename,mode='r')
    
    # read all lines at once
    T_all_of_it = T.read()
    
    # close the file
    T.close()

    # Get msg queue len from P1
    filename = "logs/" + str(port) + "timestamps.txt"
    logical_clock = open(filename, mode='r')
    
    # read all lines at once
    logical_clock_all_of_it = logical_clock.read()
    
    # close the file
    logical_clock.close()

    x = T_all_of_it.split(",")

    for i in range(len(x) - 1):
        x[i] = round(float(x[i]), 3)

    

    y = logical_clock_all_of_it.split(",")
    for l in range(len(y) - 1):
        y[l] = int(y[l])
    m = min(len(x), len(y))

    if seperated:
        plt.figure()
    plt.plot(x[:m - 1],y[:m - 1])
    if seperated:
        plt.title(str(port) + " LOGICAL CLOCK over TIME" + " TickMax (Full range)=" + str(maxtick))
    else:
        plt.title("(ALL Machines) LOGICAL CLOCK over TIME" + " TickMax (Full range)=" + str(maxtick))
    plt.xlabel("time (seconds)")
    plt.ylabel("LOGICAL CLOCK (LAMPORT TIME STAMP)")
    if seperated:
        plt.savefig("figures/" + str(maxtick) + "/" + "FullRange" + "/"+ str(port) + " LOGICAL CLOCK over TIME" + " TickMax (Full range)=" + str(maxtick) + "_SEP"+ ".pdf")
    else:
        plt.savefig("figures/" + str(maxtick) + "/" + "FullRange" + "/" + "(ALL Machines) LOGICAL CLOCK DRIFT over TIME" + " TickMax (Full range)=" + str(maxtick) + ".pdf")


maxtick = 24
plot_msg_queue_len_over_time(2056,maxtick, True)
plot_msg_queue_len_over_time(3056,maxtick, True)
plot_msg_queue_len_over_time(4056,maxtick, True)

plot_msg_queue_len_over_time(2056,maxtick, False)
plot_msg_queue_len_over_time(3056,maxtick, False)
plot_msg_queue_len_over_time(4056,maxtick, False)


plot_logical_clock_over_time(2056,maxtick, True)
plot_logical_clock_over_time(3056,maxtick, True)
plot_logical_clock_over_time(4056,maxtick, True)


plot_logical_clock_over_time(2056,maxtick, False)
plot_logical_clock_over_time(3056,maxtick, False)
plot_logical_clock_over_time(4056,maxtick, False)

