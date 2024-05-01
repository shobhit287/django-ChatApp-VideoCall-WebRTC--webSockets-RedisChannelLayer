from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from .models import group_chat_message
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer
import json
from time import sleep
from asyncio import sleep
from django.conf import settings
import uuid
users_list=[]
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        await self.send({
            'type':'websocket.accept'
        })
        self.group_name=self.scope['url_route']['kwargs'].get('slug')
        if self.group_name:
            await self.channel_layer.group_add(self.group_name,self.channel_name)
        else: 
            await self.channel_layer.group_add('public',self.channel_name)

          
    async def websocket_receive(self,event):
        if self.group_name: 
         await self.save_message(self.group_name,event['text'])
         await self.channel_layer.group_send(self.group_name,{
            'type':'chat.message',
            'message':event['text'],
            "sender_channel_name": self.channel_name,
         })
        else:
           await self.save_message('public',event['text'])
           await self.channel_layer.group_send('public',{
            'type':'chat.message',
            'message':event['text'],
            "sender_channel_name": self.channel_name,})
            
    async def chat_message(self,event):
        sender_channel_name = event["sender_channel_name"]
        if sender_channel_name!=self.channel_name:
            await  self.send({
            "type": "websocket.send",
            "text": event["message"],
            })  
          
    @database_sync_to_async      
    def save_message(self,group_name,event_msg):
       msg_save=group_chat_message(group_name=group_name,current_user=self.scope["user"].username,msg=event_msg) 
       msg_save.save()      

    async def websocket_disconnect(self,event):
        if self.group_name: 
         await self.channel_layer.group_discard(self.group_name,self.channel_name)
        else: 
         await self.channel_layer.group_discard('public',self.channel_name)

        raise StopConsumer
    
   
class handleVideoCall(AsyncWebsocketConsumer):
   async def connect(self):
      await self.accept()
      await self.channel_layer.group_add('public',self.channel_name)
      user={f'user-{uuid.uuid4()}':self.channel_name}
      users_list.append(user)
      
      await self.channel_layer.group_send('public',{
         'type':'send_current_user',
      })
      

   async def send_current_user(self,event):
         modified_users=[]
         for user in users_list:
           for key,value in user.items(): 
            if value != self.channel_name:
               modified_users.append(user)
               break
         data_users={'type':'users_info','users':modified_users}   
         await self.send(json.dumps(data_users))
     

      
      

   async def receive(self, text_data=None, bytes_data=None):
     received_data=json.loads(text_data)     
     if received_data['type']=="create_offer":
        remote_user=None
        offered_by=None
        for user in users_list:
          for key,value in user.items():
             if received_data['user']==key:
               remote_user=value
             if self.channel_name==value:
                offered_by=key  
        if received_data is not None:
           await self.channel_layer.group_send('public',{
              'type':'send_offer',
              'remote_user':remote_user,
              'offer_sdp':received_data['offer_sdp'],
              'offered_by':offered_by
           })   
     if received_data['type']=='accepted':
        await self.channel_layer.group_send('public',{
           'type':'accepted_handler',
           'current_user':self.channel_name,
           'remote_user':received_data['offered_by'],
           'offer_sdp':received_data['offer_sdp']
        })
     if received_data['type']=='rejected':
        await self.channel_layer.group_send('public',{
           'type':'rejected_handler',
           'remote_user':received_data['offered_by']
        })

     if received_data['type']=='accepted_answer_sdp':
        await self.channel_layer.group_send('public',{
           'type':'accepted_answer_sdp',
           'remote_user':received_data['remote_user'],
           'answer_sdp':received_data['answer_sdp']
        })

     if received_data['type']=='cancelled':
        await self.channel_layer.group_send('public',{
           'type':'cancelled',
           'remote_user':received_data['remote_user'],
        })

   async def cancelled(self,event):
         remote_channel_name=None
         for user in users_list:
            for key,value in user.items():
               if key==event['remote_user']:
                  remote_channel_name=value

         if remote_channel_name:
            if remote_channel_name==self.channel_name:
               ans={'type':'cancelled'}     
               await self.send(json.dumps(ans))

            



   async def accepted_answer_sdp(self,event):
      remote_channel_name=None
      for user in users_list:
         for key,value in user.items():
            if key==event['remote_user']:
               remote_channel_name=value

      if remote_channel_name:
         if remote_channel_name==self.channel_name:
            ans={'type':'call_accepted','answer_sdp':event['answer_sdp']}     
            await self.send(json.dumps(ans))


   async def rejected_handler(self,event):
      remote_channel_name=None
      for user in users_list:
         for key,value in user.items():
            if key==event['remote_user']:
               remote_channel_name=value

      if remote_channel_name:
         if remote_channel_name==self.channel_name:
            rej={'type':'rejected'}     
            await self.send(json.dumps(rej))

   async def accepted_handler(self,event):
      if event['current_user']==self.channel_name:
         gen_ans_sdp={'type':'answer_sdp','offered_by':event['remote_user'],'offer_sdp':event['offer_sdp']}     
         await self.send(json.dumps(gen_ans_sdp))


   async def send_offer(self,event):
      if self.channel_name==event['remote_user']:
         offer_sdp={'type':'send_offer','offer':event['offer_sdp'],'offered_by':event['offered_by']}
         await self.send(json.dumps(offer_sdp))       
    

   async def disconnect(self, code):
       self.channel_layer.group_discard('public',self.channel_name)
       for user in users_list:
             if self.channel_name in user.values():
                users_list.remove(user)
                break

       await self.channel_layer.group_send('public',{
          'type':'send_user_after_disconnect'
       })     

   async def send_user_after_disconnect(self,event):
         modified_users=[]
         for user in users_list:
           for key,value in user.items(): 
            if value !=self.channel_name:
               modified_users.append(user)
               break

         data_users={'type':'users_info','users':modified_users}   
         await self.send(json.dumps(data_users))
      
          
             
   

