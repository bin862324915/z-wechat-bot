from plugins import *#line:1
import plugins #line:2
from bridge .context import ContextType #line:3
from bridge .reply import Reply ,ReplyType #line:4
from common .log import logger #line:5
import re #line:6
import os #line:7
import json #line:8
import time #line:9
from threading import Thread ,Lock #line:10
from lib import itchat #line:11
from lib .itchat .content import *#line:12
@plugins .register (name ="Car_push",desire_priority =99 ,desc ="Real time interactive car information push service through WeChat. Visit www.zzzwb.com for service support",version ="1.0",author ="zzzwb",)#line:20
class Carpush (Plugin ):#line:21
    def __init__ (OO000O0O0OOOOO0O0 ):#line:22
        super ().__init__ ()#line:23
        try :#line:24
            if not OO000O0O0OOOOO0O0 .on_handle_contex ():#line:25
                return #line:26
            logger .info ("[Carpush] Plugin initialized successfully")#line:27
            OO000O0O0OOOOO0O0 .handlers [Event .ON_HANDLE_CONTEXT ]=OO000O0O0OOOOO0O0 .on_handle_context #line:28
            OO000O0O0OOOOO0O0 .file_path =os .path .join (os .path .dirname (__file__ ),"data.json")#line:30
            OO000O0O0OOOOO0O0 .get_path =os .path .join (os .path .dirname (__file__ ),"get.json")#line:31
            OO000O0O0OOOOO0O0 .file_lock =Lock ()#line:33
            OO000O0O0OOOOO0O0 .is_processing =False #line:34
            OO000O0O0OOOOO0O0 .stop_thread =True #line:35
            OO000O0O0OOOOO0O0 .thread =None #line:36
        except Exception as OO00O00O0OO0O000O :#line:38
            logger .error (f"[Carpush] Initialization error: {OO00O00O0OO0O000O}")#line:39
            raise "[Carpush] init failed, ignore"#line:40
    def start_file_watcher (OO00O0O0O0OOOO0O0 ):#line:43
        ""#line:46
        if not OO00O0O0O0OOOO0O0 .stop_thread :#line:47
            logger .info ("[Carpush] File watcher is already running.")#line:48
            return #line:49
        OO00O0O0O0OOOO0O0 .stop_thread =False #line:51
        OO00O0O0O0OOOO0O0 .thread =Thread (target =OO00O0O0O0OOOO0O0 .watch_file ,daemon =True )#line:52
        OO00O0O0O0OOOO0O0 .thread .start ()#line:53
        logger .info ("[Carpush] File watcher started.")#line:54
    def stop_file_watcher (OOO0O00OO0O0O0O00 ):#line:56
        ""#line:59
        if OOO0O00OO0O0O0O00 .stop_thread :#line:60
            logger .info ("[Carpush] File watcher is not running.")#line:61
            return #line:62
        OOO0O00OO0O0O0O00 .stop_thread =True #line:64
        if OOO0O00OO0O0O0O00 .thread and OOO0O00OO0O0O0O00 .thread .is_alive ():#line:65
            OOO0O00OO0O0O0O00 .thread .join ()#line:66
        logger .info ("[Carpush] File watcher stopped.")#line:67
    def watch_file (O0OOOO0O00O00OO0O ):#line:69
        ""#line:72
        while not O0OOOO0O00O00OO0O .stop_thread :#line:73
            O0OOOO0O00O00OO0O .check_and_process_file ()#line:74
            time .sleep (5 )#line:75
    def check_and_process_file (OO00O0OOO0OO0O0O0 ):#line:77
        ""#line:80
        with OO00O0OOO0OO0O0O0 .file_lock :#line:81
            if OO00O0OOO0OO0O0O0 .is_processing :#line:82
                return #line:83
            OO00O0OOO0OO0O0O0 .is_processing =True #line:85
            try :#line:86
                if not os .path .exists (OO00O0OOO0OO0O0O0 .file_path ):#line:87
                    return #line:88
                with open (OO00O0OOO0OO0O0O0 .file_path ,"r",encoding ="utf-8")as O0O0OOOOOOO0OOO00 :#line:90
                    OOOO0O000OOOO000O =O0O0OOOOOOO0OOO00 .read ().strip ()#line:91
                if not OOOO0O000OOOO000O :#line:93
                    return #line:94
                OO0O000O00O0O0O00 =json .loads (OOOO0O000OOOO000O )#line:96
                O00O0O000O0O00OO0 =OO0O000O00O0O0O00 .get ("user")#line:97
                OOOO0OO0O0OO0000O =OO0O000O00O0O0O00 .get ("msg")#line:98
                if O00O0O000O0O00OO0 and OOOO0OO0O0OO0000O :#line:100
                    O000OO0O0O00000OO =OO00O0OOO0OO0O0O0 .find_friend_by_remark_name (O00O0O000O0O00OO0 )#line:102
                    if O000OO0O0O00000OO :#line:103
                        O0O0OOO0OO000OO0O =f"[Car push]消息:\n\n{OOOO0OO0O0OO0000O}"#line:104
                        OO00O0OOO0OO0O0O0 .send_message_to_user (O000OO0O0O00000OO ,O0O0OOO0OO000OO0O )#line:105
                        open (OO00O0OOO0OO0O0O0 .file_path ,"w").close ()#line:108
                        logger .info (f"[Carpush] Message sent to {O00O0O000O0O00OO0}. Data.json cleared.")#line:109
                    else :#line:110
                        logger .warning (f"[Carpush] Friend with remark name '{O00O0O000O0O00OO0}' not found.")#line:111
                else :#line:112
                    logger .warning ("[Carpush] Invalid data in data.json.")#line:113
            except Exception as O0O0O000OOOOO0000 :#line:114
                logger .error (f"[Carpush] Error processing file: {O0O0O000OOOOO0000}")#line:115
            finally :#line:116
                OO00O0OOO0OO0O0O0 .is_processing =False #line:117
    def on_handle_context (OO00O0OO0OO0OO00O ,OO0OO000OO00OOOO0 :EventContext ):#line:119
        if OO0OO000OO00OOOO0 ["context"].type !=ContextType .TEXT :#line:120
            return #line:121
        OO00O00OO0OO0O0OO =OO0OO000OO00OOOO0 ["context"].content .strip ()#line:123
        logger .debug (f"[Carpush] Received message: {OO00O00OO0OO0O0OO}")#line:124
        if OO00O00OO0OO0O0OO =="$car start":#line:127
            OO00O0OO0OO0OO00O .start_file_watcher ()#line:128
            OO0O0O0O0OOO0O0OO =Reply ()#line:129
            OO0O0O0O0OOO0O0OO .type =ReplyType .TEXT #line:130
            OO0O0O0O0OOO0O0OO .content ="Car_push服务已启动 ✅"#line:131
            OO0OO000OO00OOOO0 ["reply"]=OO0O0O0O0OOO0O0OO #line:132
            OO0OO000OO00OOOO0 .action =EventAction .BREAK_PASS #line:133
            return #line:134
        if OO00O00OO0OO0O0OO =="$car stop":#line:136
            OO00O0OO0OO0OO00O .stop_file_watcher ()#line:137
            OO0O0O0O0OOO0O0OO =Reply ()#line:138
            OO0O0O0O0OOO0O0OO .type =ReplyType .TEXT #line:139
            OO0O0O0O0OOO0O0OO .content ="Car_push服务已停止 ❎"#line:140
            OO0OO000OO00OOOO0 ["reply"]=OO0O0O0O0OOO0O0OO #line:141
            OO0OO000OO00OOOO0 .action =EventAction .BREAK_PASS #line:142
            return #line:143
        if not OO00O00OO0OO0O0OO .startswith ("发送回复"):#line:146
            return #line:147
        OO00O00OO0OO0O0OO =OO00O00OO0OO0O0OO [len ("发送回复"):].strip ()#line:150
        if not OO00O00OO0OO0O0OO :#line:151
            OO0O0O0O0OOO0O0OO =Reply ()#line:152
            OO0O0O0O0OOO0O0OO .type =ReplyType .TEXT #line:153
            OO0O0O0O0OOO0O0OO .content ="请提供需要回复的内容。例如：发送回复 我已经收到您的通知，我会尽快处理"#line:154
            OO0OO000OO00OOOO0 ["reply"]=OO0O0O0O0OOO0O0OO #line:155
            OO0OO000OO00OOOO0 .action =EventAction .BREAK_PASS #line:156
            return #line:157
        OOO00OOO0OOOO0000 ={"msg":OO00O00OO0OO0O0OO ,"code":200 }#line:160
        try :#line:162
            with open (OO00O0OO0OO0OO00O .get_path ,"w",encoding ="utf-8")as O0OOOO000OOOOOOO0 :#line:163
                json .dump (OOO00OOO0OOOO0000 ,O0OOOO000OOOOOOO0 ,ensure_ascii =False ,indent =4 )#line:164
            logger .info (f"[Carpush] JSON data written to {OO00O0OO0OO0OO00O.get_path}: {OOO00OOO0OOOO0000}")#line:165
        except Exception as OOOOO0OOOOOOO00O0 :#line:166
            logger .error (f"[Carpush] Failed to write JSON to {OO00O0OO0OO0OO00O.get_path}: {OOOOO0OOOOOOO00O0}")#line:167
            OO0O0O0O0OOO0O0OO =Reply ()#line:168
            OO0O0O0O0OOO0O0OO .type =ReplyType .TEXT #line:169
            OO0O0O0O0OOO0O0OO .content ="回复失败，请检查日志。"#line:170
            OO0OO000OO00OOOO0 ["reply"]=OO0O0O0O0OOO0O0OO #line:171
            OO0OO000OO00OOOO0 .action =EventAction .BREAK_PASS #line:172
            return #line:173
        OO0O0O0O0OOO0O0OO =Reply ()#line:176
        OO0O0O0O0OOO0O0OO .type =ReplyType .TEXT #line:177
        OO0O0O0O0OOO0O0OO .content ="回复成功 ✅"#line:178
        OO0OO000OO00OOOO0 ["reply"]=OO0O0O0O0OOO0O0OO #line:179
        OO0OO000OO00OOOO0 .action =EventAction .BREAK_PASS #line:180
    def find_friend_by_remark_name (OO00OOO000000OO0O ,OOOOOO0OOO0OO0000 ):#line:182
        ""#line:185
        try :#line:186
            OOO0000O0O0OO00OO =itchat .get_friends (update =True )#line:187
            for O0O000OO0OOO0O0O0 in OOO0000O0O0OO00OO :#line:188
                if O0O000OO0OOO0O0O0 ["RemarkName"]==OOOOOO0OOO0OO0000 :#line:189
                    return O0O000OO0OOO0O0O0 #line:190
            for O0O000OO0OOO0O0O0 in OOO0000O0O0OO00OO :#line:193
                if O0O000OO0OOO0O0O0 ["NickName"]==OOOOOO0OOO0OO0000 :#line:194
                    return O0O000OO0OOO0O0O0 #line:195
            return None #line:197
        except Exception as OO000O000O00OO0O0 :#line:198
            logger .error (f"[Carpush] Failed to get friends list: {OO000O000O00OO0O0}")#line:199
            return None #line:200
    def send_message_to_user (O00O0O0O0O00O00O0 ,O0O0O0OOOO00O0000 ,O00O0OO00OOO0O000 ):#line:202
        ""#line:205
        try :#line:206
            itchat .send (O00O0OO00OOO0O000 ,toUserName =O0O0O0OOOO00O0000 ["UserName"])#line:207
            logger .info (f"[Carpush] Message sent to {O0O0O0OOOO00O0000['RemarkName']}: {O00O0OO00OOO0O000}")#line:208
        except Exception as O0000O00O0OOOO000 :#line:209
            logger .error (f"[Carpush] Failed to send message: {O0000O00O0OOOO000}")#line:210
    def on_handle_contex (OO0O00O0OOO000000 ):#line:212
        if not hasattr (itchat .content ,"AUTH"):#line:213
            logger .error (f"[Carpush] initiate error：It should come from www.zzzwb.com")#line:214
            return False #line:215
        return True #line:216
    def get_help_text (O0O0O00OOO0000OOO ,**O0O0O0OOOO00O0OO0 ):#line:218
        return ("使用 发送回复，进行回复用户，比如：发送回复 我已经收到您的通知，我会尽快处理\n" "使用 $car start 启动Car_push服务，使用 $car stop 停止Car_push服务。\n")#line:222
