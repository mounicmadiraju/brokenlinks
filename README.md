# Crawling Broken Links {404 Error's} in Python
Using Python to crawl Webpages via sitemap and checking broken links for every page

# Basic Steps
1. Reading sitemap.xml of the Website and Searching for 'href'attribute to get all valid links in every page.
2. Checking link response status and dumping 404 error URLs to a text file.

# How to run
1. Install beautifulsoup4 [Python library] and 
1. Specifying the target sitemap in broken_links.py file @ [request = build_request("https://www.jobstreet.com.my/career-resources/page-sitemap.xml")]
2. Run the command "python broken_links.py"
3. To stop the program while executing,just Use "ctrl+c"
