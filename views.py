from tornado import web, websocket

opened_sockets = {}

class MainHandler(web.RequestHandler):
	def get(self):
		self.render('index.html')

def send_message(message):
	must_remove = []
	
	for (nick, socket) in opened_sockets.items():
		try:
			socket.write_message(message)
		except:
			must_remove.append(nick)
			
	for socket in must_remove:
		del opened_sockets[nick]

class MessageHandler(websocket.WebSocketHandler):
	def open(self):
		self.receive_message(self.on_message)
		
		for (nick, socket) in opened_sockets.items():
			self.write_message('new_user:' + nick)
		
	def on_message(self, message):
		if len(message) > 5 and message[:5] == 'nick:':
			self.nick = message[5:].strip()
			send_message('new_user:' + self.nick)
			opened_sockets[self.nick] = self
		elif len(message) > 8 and message[:8] == 'message:':
			message = message[8:].strip()
			send_message(self.nick + ': ' + message)
		elif message == 'close':
			send_message('remove_user:' + self.nick)
			del opened_sockets[self.nick]
				
		self.receive_message(self.on_message)