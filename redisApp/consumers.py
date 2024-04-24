from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
list_of_user=[]
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        await self.send({
            'type':'websocket.accept'
        })
        self.group_name=self.scope['url_route']['kwargs'].get('slug')
        if self.group_name:
            user={f"{self.group_name}":self.channel_name}
            list_of_user.append(user)
            await self.channel_layer.group_add(self.group_name,self.channel_name)
        else: 
            user={"public":self.channel_name}
            list_of_user.append(user)
            await self.channel_layer.group_add('public',self.channel_name)

          
   

        

    async def websocket_receive(self,event):
        if self.group_name:  
         await self.channel_layer.group_send(self.group_name,{
            'type':'chat.message',
            'message':event['text'],
            "sender_channel_name": self.channel_name,
         })
        else:
           await self.channel_layer.group_send('public',{
            'type':'chat.message',
            'message':event['text'],
            "sender_channel_name": self.channel_name,})
            
    async def chat_message(self,event):
      sender_channel_name = event["sender_channel_name"]
      if sender_channel_name != self.channel_name:
          await  self.send({
                "type": "websocket.send",
                "text": event["message"],
            })  

    async def websocket_disconnect(self,event):
        if self.group_name: 
         await self.channel_layer.group_discard(self.group_name,self.channel_name)
        else: 
         await self.channel_layer.group_discard('public',self.channel_name)

        raise StopConsumer
    

