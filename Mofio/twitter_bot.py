import tweepy # lib do twitter

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import re
import time
import datetime
from random import randint

def data_hora():
	''' RETURNS DATE AND TIME FORMATED '''
	data_hora = "%d/%d/%d - %d:%d" % (datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year, datetime.datetime.now().hour, datetime.datetime.now().minute)
	return data_hora

def cantar_brega():
	''' THIS FUNCTIONS RETURNS A VERSE OF A RANDOM BREGA SONG '''
	bregas = ['CHA-PU-LE-TEI',  'O DJ ta mt loooouco e mandou te avisar', \
	'Passo o dia sonhando pensando em você, meu amooor', 'desça daí, seu corno, desça daíiii'\
	'Quando acordar de manha e tomar seu café sozinha, pergunte pra sua tristeza se ela também é minhaaa :(']

	index = randint(0, len(bregas)-1)
	return bregas[index]


# =================================== TOKENS ============================================= #
CONSUMER_KEY = 'LEK3YlwVYwsr8N07VbQQta3Hx' # Consumer API key
CONSUMER_SECRET = 'eeiJrVzN36MOEp0sBbFyQeiUTr2V3bPpBSjwWUcxnkAvfxCSft' # Consumer API secret key
ACCESS_KEY = '1164078743381561344-0YmsHK6X72m96XhuvnFWxtnTYU59xI' # Access token
ACCESS_SECRET = 'jqn2OkTZCqOPmPgvMiMhTm7wcLDPbYAfO91s4DVPPVzRb' # Access token secret key
# ======================================================================================== #

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# ================================== PT BÁSICO ======================================== #
mofio_bot = ChatBot('mofio')
basico = ['Oi', 'Olá mundo!', \
'Quem é você?', 'Meu nome é Mofio! Sou um bot criado por Vinícius Vieira', \
'O que você quer?', 'Dominar o mundo',\
'O que você pretende?', 'Dominar o mundo',\
'Ĉanta um brega aleatorio pra mim', cantar_brega(),\
'Que horas são?', data_hora()]


TREINAR_BASICO = ListTrainer(mofio_bot)
TREINAR_BASICO.train(basico)
# ===================================================================================== #

# English trainer
eng_trainer = ChatterBotCorpusTrainer(mofio_bot)
eng_trainer.train("chatterbot.corpus.english.conversations", "chatterbot.corpus.english.greetings")


# Verificando e respondendo tweets:
while True:
	# Verificando os tweets da time line...
	tweets = api.home_timeline()
	# Serão retornados os vinte primeiros tweets

	# Verificando cada tweet...
	for tweet in tweets:
		# Escrevendo informações sobre cada tweet no terminal...
		print('-------------------------------------------------------------------\n')
		print(str(tweet.id) + ' - '+ str(tweet.text) + '\n')
		# Escrevendo o id de cada tweet em um arquivo txt para conferências futuras...
		tweets_respondidos = open('tweets_respondidos.txt', 'a+')

		# Tentando responder o tweet:
		try:
			if tweet.text == '#oimofio':
				resposta = 'oi amor <3'
				api.update_status('@%s %s' % (tweet.user.screen_name, resposta), tweet.id)

				print('Tweet respondido: ',resposta)

			elif '#oimofio' in tweet.text:
				# Pegando todos os caracteres depois de '#oimofio '...
				TWEET_TEXT = tweet.text[9:]
				resposta = mofio_bot.get_response(TWEET_TEXT)
				api.update_status('@%s %s' % (tweet.user.screen_name, resposta), tweet.id)
				tweets_respondidos.write(str(tweet.id)+'\n')

				print('Tweet respondido: ',resposta)

		except tweepy.error.TweepError:
			# Se o tweet já tiver sido respondido, ele cai nesta exceção
			print('O tweet já foi respondido\n')

		except Exception as e:
			# Se aconteceu algum erro diferente, cai neste caso.
			# É importante para tratamento de erros futuros.
			print('Houve um pequeno problema: ' % e)

	tweets_respondidos.close()

	# Esperando 20 segundos para dar um refresh no feed
	print("\n* Espera só 20 segundinhos que eu vou dar refresh no feed, ok? *\n")
	time.sleep(30)