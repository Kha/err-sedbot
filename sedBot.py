# encoding=utf-8
# vim:noet:sw=4:ts=4

import re
import collections
from errbot import BotPlugin, botcmd
from errbot.utils import get_sender_username

class SedBot(BotPlugin):
	def __init__(self):
		super(SedBot, self).__init__()
		self.backlog = collections.defaultdict(list)

	def configure(self, configuration):
		super().configure(configuration)
		self.config = self.config or self.get_configuration_template()

	def get_configuration_template(self):
		return {'BACKLOG_LENGTH': 3}

	def check_configuration(self, configuration):
		super().check_configuration(configuration)

		if configuration['BACKLOG_LENGTH'] <= 0:
			raise ValidationException('BACKLOG_LENGTH must be positive')

	def callback_message(self, conn, mess):
		command = re.match('s/([^/]+)/([^/]*)/?', mess.getBody())
		if command:
			for old_mess in self.backlog[conn]:
				try:
					(replaced, n) = re.subn(command.group(1), command.group(2), old_mess.getBody())
				except Exception as e:
					self.send(mess.getFrom(), "regex does not compute", message_type=mess.getType())
					return

				if n > 0:
					reply = '{0} meant: "{1}"'.format(get_sender_username(old_mess), replaced)
					self.send(mess.getFrom(), reply, message_type=mess.getType())
					return

		self.backlog[conn] = ([mess] + self.backlog[conn])[:self.config['BACKLOG_LENGTH']]
