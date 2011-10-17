#coding:utf-8
import socket, select, time, msnlib, msncb

def void(s): pass
msnlib.debug = msncb.debug = void

def get_friend_list(email, password):
#    print email, password
    m = msnlib.msnd()
    m.cb = msncb.cb()

    m.email = email.strip()
    m.pwd = password.strip()
    m.encoding = 'utf-8'
    try:
        m.login()
        m.sync()
    except:
        return
    m.change_status('invisible')

    begin_time = time.time()

    users = set()
    while True:
        fds = m.pollable()
        infd = fds[0]
        outfd = fds[1]

        fds = select.select(infd, outfd, [], 0)

        for i in fds[0] + fds[1]:
            try:
                m.read(i)
            except ('SocketError', socket.error), err:
                if i != m:
                    m.close(i)
        merge_users = users|set(m.users.keys())
        if len(users) == len(merge_users):
            end_time = time.time()
            if len(users):
                if end_time-begin_time >= 2:
                    break
            elif end_time-begin_time >= 3:
                break
            time.sleep(0.05)
        else:
            users = merge_users
            begin_time = time.time()
    result = {}
    for i in users:
        nick = m.users[i].nick
        i_lower = i.lower()
        if nick.lower() == i_lower:
            nick = nick.split("@", 1)[0]
        result[i_lower] = nick

    return result

if __name__ == "__main__":
    result = get_friend_list(raw_input("email:"), raw_input("password:"))
    if result is False:
        print "email or password or network error , login failed"
    else:
        for k, v in result.iteritems():
            print k, v.decode("utf-8", "ignore")

