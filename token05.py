# -*- coding: utf-8 -*-
from ImChang.lineXpy import *
from ImChang.akaXd import *
from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TCompactProtocol import TCompactProtocol
from threading import Thread
import os, json, traceback, time, sys
from data import commands

OT = OpType
fileName = os.path.splitext(os.path.basename(__file__))[0]

#db = livejson.File("token/%s.json" % fileName)
db = json.loads(open('./token05.json','r').read())

# login = json.loads(open('token/token05.json','r').read())

# if login["email"] == "":
#     try:
#         client = LINE(idOrAuthToken=login["token"])
#     except:
#         print("TOKEN EXPIRED");
# else:
#   client = LINE(login["email"],login["password"])
app = "DESKTOPWIN\t5.21.3\tWindows\t10"
client = LINE(idOrAuthToken="Ft9e3QReZB5i0oMQ9lS1.nDTOvWGvwK8dZoNi4xMCqq.wP1qGgy3y58cM7nJQ4kk26yWBWW9j1Vv61YxTmO/yQI=")
client.log("Auth Token : " + str(client.authToken))

uid = client.profile.mid
poll = OEPoll(client)

client.findAndAddContactsByMid("u0b499ce24e07b16ec12f8d0ba3ef8438")
client.sendMessageCustom("u0b499ce24e07b16ec12f8d0ba3ef8438","เข้าสู่ระบบเรียบร้อย\n"+uid+"\n"+client.profile.displayName ,client.profile.mid)

good = commands(fileName, client, app, uid)

def worker(op):
    
    #print ('++ Operation : [%s] ( %i ) %s' % (client.profile.displayName,op.type, OpType._VALUES_TO_NAMES[op.type].replace('_', ' ')))
    if op.type == OT.RECEIVE_MESSAGE or op.type == 26:good.receive_message(op)
    elif op.type == OT.NOTIFIED_KICKOUT_FROM_GROUP or op.type == 133:good.notif_kick_from_group(op)
    elif op.type == OT.NOTIFIED_INVITE_INTO_GROUP or op.type == 124:good.notif_invite_into_group(op)
    elif op.type == OT.NOTIFIED_CANCEL_INVITATION_GROUP or op.type == 126:good.notif_cancel_invite_group(op)
    elif op.type == OT.NOTIFIED_UPDATE_GROUP or op.type == 122:good.notif_update_group(op)
    elif op.type == OT.NOTIFIED_ACCEPT_GROUP_INVITATION or op.type == 130:good.notif_accept_group_invite(op)
    elif op.type == OT.ACCEPT_GROUP_INVITATION or op.type == 129:good.accept_group_invite(op)
    elif op.type == OT.NOTIFIED_LEAVE_GROUP or op.type == 61:good.notofied_leave_chat(op)
    elif op.type == OT.END_OF_OPERATION:pass



while 1:
    try:
        ops = client.poll.fetchOperations(client.revision, 50)
        for op in ops:
            client.revision = max(client.revision, op.revision)
            t1 = Thread(target=worker(op,))
            t1.start()
            t1.join()
    except Exception as e:
        e = traceback.format_exc()
        if "EOFError" in e:pass
        elif "ShouldSyncException" in e or "LOG_OUT" in e:python3 = sys.executable;os.execl(python3, python3, *sys.argv)
        else:traceback.print_exc()