import feedparser
from datetime import datetime, timedelta, timezone
import sqlite3
import html2text
import discord
from discord.ext import commands, tasks

from config import TOKEN, CHANNEL_ID, UPDATE_INTERVAL, LAST_COMMENT_RANGE, RSS_FEEDS


connection = sqlite3.connect('comments.db')
c = connection.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS comments (title TEXT, link TEXT)''')
connection.commit()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


def record_comment_in_db(comment):
	c.execute("INSERT INTO comments (title, link) VALUES (?, ?)", (comment.title, comment.link))
	connection.commit()


def comment_in_db(entry):
	c.execute("SELECT link FROM comments WHERE link=?", (entry.link,))
	if c.fetchone() is None:
		return False
	else:
		return True


def get_new_comments():
	new_comments = []

	for rss_feed in RSS_FEEDS:
		entries = feedparser.parse(rss_feed["url"]).entries
		for entry in entries:
			if not comment_in_db(entry):
				pub_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=timezone.utc)
				if datetime.now(timezone.utc) - pub_date <= timedelta(days=LAST_COMMENT_RANGE):
					new_comments.append({"comment": entry, "user": rss_feed["user"]})

	return new_comments


def format_to_message(comment):
	commenter = comment["comment"].title.split(",", 1)[0].strip()
	article_title = comment["comment"].title.split(",", 1)[1].strip()
	article_link = comment["comment"].link
	article_user = comment["user"]
	comment_body = html2text.HTML2Text().handle(comment["comment"].summary).strip()
	
	message = f"**{commenter}** commented on **[{article_title}](<{article_link}>)**" + (f" by <@{article_user}>:" if article_user else ":")
	if (len(comment_body) >= 2000 - len(message)):
		read_more = f"... [read more](<{article_link}>)"
		message += f"\n{comment_body[:(2000 - 1 - len(message)- len(read_more))]}" + read_more
	else:
		message += f"\n{comment_body}"

	return message


@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord!')
	post_new_comments.start()


@tasks.loop(minutes=UPDATE_INTERVAL)
async def post_new_comments():
	channel = bot.get_channel(CHANNEL_ID)

	new_comments = get_new_comments()
	for comment in new_comments:
		message = format_to_message(comment)
		await channel.send(message)
		record_comment_in_db(comment["comment"])


if __name__ == "__main__":
	bot.run(TOKEN)
