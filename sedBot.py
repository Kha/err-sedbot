# encoding=utf-8
# vim:noet:sw=4:ts=4

import re
from errbot import BotPlugin, botcmd
from errbot.utils import get_sender_username

class SedBot(BotPlugin):
	def __init__(self):
		super(SedBot, self).__init__()
		self.last_mess = None

	def callback_message(self, conn, mess):
		if self.last_mess:
			command = re.match('s/([^/]+)/([^/]*)/?', mess.getBody())
			if command:
				try:
					(replaced, n) = re.subn(command.group(1), command.group(2), self.last_mess.getBody())
				except Exception as e:
					self.send(mess.getFrom(), "regex does not compute", message_type=mess.getType())
					return

				if n > 0:
					reply = '{0} meant: "{1}"'.format(get_sender_username(self.last_mess), replaced)
					self.send(mess.getFrom(), reply, message_type=mess.getType())
		self.last_mess = mess
