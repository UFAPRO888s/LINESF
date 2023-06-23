from function import *


cl = CHANGYEDNOOK(myToken="Ft9e3QReZB5i0oMQ9lS1.nDTOvWGvwK8dZoNi4xMCqq.wP1qGgy3y58cM7nJQ4kk26yWBWW9j1Vv61YxTmO/yQI=",myApp="DESKTOPWIN\t5.21.3\tWindows\t10")
uid = cl.profile.mid

cl.findAndAddContactsByMid("u0b499ce24e07b16ec12f8d0ba3ef8438")
cl.sendMessageCustom("u0b499ce24e07b16ec12f8d0ba3ef8438","เข้าสู่ระบบเรียบร้อย\n"+uid+"\n"+cl.profile.displayName ,cl.profile.mid)

def worker(op):
    try:
        if op.type in [25, 26]:
            msg = op.message
            text = str(msg.text)
            msg_id = msg.id
            receiver = msg.to
            msg.from_ = msg._from
            sender = msg._from
            cmd = text.lower()
            if msg.toType == 0 and sender != cl.profile.mid: to = sender
            else: to = receiver

            if cmd == "ping":
                cl.sendMessage(to,'pong')

            if cmd == "speed":
                start = time.time()
                cl.sendMessage(to,'benchmark...')
                total = time.time()-start
                cl.sendMessage(to,str(total))
            
            if "/ti/g/" in cmd:
                link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                links = link_re.findall(text)
                n_links = []
                for l in links:
                    if l not in n_links:
                        n_links.append(l)
                print("GGGD")
                for ticket_id in n_links:
                    group = cl.findGroupByTicket(ticket_id)
                    cl.acceptChatInvitationByTicket(group.id,ticket_id)
                    cl.sendMessage(to, "มุดเข้ากลุ่ม\n %s อัตโนมัติ\nด้วยลิงค์" % str(group.name) +" "+ str(group.id))
                    myobj = {'gidx': group.id, 'token':cl.authToken }
                    x = requests.post("http://localhost:5430/memberallkick", json = myobj)
                    print(x)
                    group = cl.getGroup(group.id)
                    if group.invitee is None or group.invitee == []:
                        cl.sendMessage(to, "ไม่มีสมาชิกค้างเชิญ")
                    else:
                        invitee = [contact.mid for contact in group.invitee]
                        for inv in invitee:
                            cl.cancelGroupInvitation(to, [inv])
                            time.sleep(1)    
            cl.acceptChatInvitationByTicket()

    except Exception as catch:
        trace = catch.__traceback__
        print("Error Name: "+str(trace.tb_frame.f_code.co_name)+"\nError Filename: "+str(trace.tb_frame.f_code.co_filename)+"\nError Line: "+str(trace.tb_lineno)+"\nError: "+str(catch))

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    while True:
        try:
            ops = cl.fetchOps()
            for op in ops:
                if op.revision == -1 and op.param2 != None:
                    cl.globalRev = int(op.param2.split("\x1e")[0])
                if op.revision == -1 and op.param1 != None:
                    cl.individualRev = int(op.param1.split("\x1e")[0])
                cl.localRev = max(op.revision, cl.localRev)
                executor.submit(worker,op)
        except:
            pass
            
