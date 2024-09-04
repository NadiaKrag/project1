'''
This is just a simple script that makes sure the method are the same throughout the 
group; as the work was divided with different group members scraping different neighborhood
'''

from instagram_scraper import InstagramScraper
import sys

if __name__ == "__main__":
		if len(sys.argv) < 2:
				print("Please specify which hashtag you wish to scrape: \n")
				sys.exit()

		# user = input("Please input username: ")
		# password = input("Please input password: ")
				
		scrapings = sys.argv[1:]
		instag = InstagramScraper(usernames = scrapings, login_only=False,
			destination='./json_files/10k/', retain_username=False, interactive=False,
			quiet=False, maximum=10000, media_metadata=True, latest=False,
			latest_stamps=False,media_types=[None],
			tag=False, search_location=False, comments=False,
			verbose=1, include_location=True, filter=None)
		 # replace tag = False with location=True and uncomment the scrape_location() line to scrape location
		#instag.scrape_hashtag()
		instag.scrape_location()
# instagram scrape uses unique id's for location: examples here some examples
# 214398345/christianshavn
# 218085806/vesterbro-copenhagen/