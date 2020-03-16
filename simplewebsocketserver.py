from twisted.internet import reactor, protocol
from txws import WebSocketFactory
import json
import os.path


class EchoServer(protocol.Protocol):
    
    def dataReceived(self, data):
        dt = json.loads(data)

        if (dt['msg']=="join"):

            a = 'room'+dt['room']
            user = dt['client']
            
            if a not in dic:
                dic[a]=[]
                if self in dic[a]:
                    return
                else:
                    dic[a].append(self)
            else:
                if self in dic[a]:
                    return
                else:
                    dic[a].append(self)

            if a not in client:
                client[a]=[]
                if user in client[a]:
                    return
                else:
                    client[a].append(user)
                    # f.write(client[a])
            else:
                if user in client[a]:
                    return
                else:
                    client[a].append(user)
            
            print dic
            print client
     
        elif (dt['msg']=="chat"):
            r = dt['room']
            rooms = 'room'+r
            
            for i in dic[r]:
                if r not in client:
                    client[r]=[]
                    if dt['username'] not in client[r]:
                        client[r].append(dt['username'])
                        x = {"username":dt['username'],"message":dt['message'],"jumlah":client,"room":dt['room'],"today":dt['today'],"jam":dt['jam']}
                    else:
                        x = {"username":dt['username'],"message":dt['message'],"jumlah":client,"room":dt['room'],"today":dt['today'],"jam":dt['jam']}
                        
                else:
                    if dt['username'] not in client[r]:
                        client[r].append(dt['username'])
                        x = {"username":dt['username'],"message":dt['message'],"jumlah":client,"room":dt['room'],"today":dt['today'],"jam":dt['jam']}
                    else:
                        x = {"username":dt['username'],"message":dt['message'],"jumlah":client,"room":dt['room'],"today":dt['today'],"jam":dt['jam']}      
                
                j = json.dumps(x)
                        
                if os.path.isfile(rooms+'.txt'):
                    f = open(rooms+'.txt','a+')
                    f.write(j+'\r\n')
                else:
                    f = open(rooms+'.txt','a+')
                    f.write(j+'\r\n')
                
                
                i.transport.write(j)

        elif (dt['msg']=="onbeforeunload"):
            if dt['room']=='':
                print 'refresh/close'
                return
            else:
                if dt['username'] is None:
                    r = dt['room']
                    if self in dic[r]:
                        dic[r].remove(self)
                    else:
                        return    
                else:
                    if dt['username'] != '':
                        r=dt['room']
                        u=dt['username']
                        
                        if u in client[r]:
                            client[r].remove(u)
                        else:
                            return

                        if self in dic[r]:
                            dic[r].remove(self)
                        else:
                            return
                        
                    else:
                        r = dt['room']
                        if self in dic[r]:
                            dic[r].remove(self)
                        else:
                            return
       
            
            print dic
            print client    
        else:
            r = dt['room']
            u = dt['username']

            if client[r]==[]:
                del client[r]
            else:
                if u in client[r]:
                    client[r].remove(u)
                else:
                    return
            
            
            if(dic.get(r).remove(self)):
                "user keluar"
            else:
                "error"

                
            print dic
            print client

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return EchoServer()

#inisiasi reactor
client=dict()
dic = dict()
factory = EchoFactory()
reactor.listenTCP(7777,WebSocketFactory(factory))
reactor.run()
