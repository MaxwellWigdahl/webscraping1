from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

#create empty dictionaries, lists, establish longest and shortest quote to later fill with values
author_count = {}
tag_count = {}
quote_lengths = []
longest_quote = ""
shortest_quote = ""


#loop thru first 10 pages
for page_number in range(1, 11):
    url = f'https://quotes.toscrape.com/page/{page_number}/'
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    #scrap author
    author_data = soup.findAll("small", attrs={"class": "author"})
    for author in author_data:
        author_name = author.text.strip()

        if author_name in author_count:
            author_count[author_name] += 1
        else:
            author_count[author_name] = 1

    #loop to scrape w uote data / determine longest and shortest quote
    quote_data = soup.findAll("span", attrs={"class": "text"})
    for quote in quote_data:
        quote_text = quote.text.strip()
        quote_lengths.append(len(quote_text))
        
        if not longest_quote or len(quote_text) > len(longest_quote):
            longest_quote = quote_text
        if not shortest_quote or len(quote_text) < len(shortest_quote):
            shortest_quote = quote_text

    #loop to scrape and count tags
    tag_data = soup.findAll("div", attrs={"class": "tags"})
    for tags in tag_data:
        for tag in tags.findAll('a', class_='tag'):
            tag_text = tag.text.strip()
            if tag_text in tag_count:
                tag_count[tag_text] += 1
            else:
                tag_count[tag_text] = 1

#author analysis
print("\nAuthor Statistics")
for author, count in author_count.items():
    print(f"{author}: {count}")

print()

max_quotes_author = max(author_count, key=author_count.get)
min_quotes_author = min(author_count, key=author_count.get)
print(f"Author with the most quotes: {max_quotes_author}")
print(f"Author with the least quotes: {min_quotes_author}")

#quote analysis
average_length = sum(quote_lengths) / len(quote_lengths)
print(f"\nAverage length of quotes: {average_length:.2f} characters")
print()
print(f"Longest quote: {longest_quote} This quote is {len(longest_quote)} characters.")
print()
print(f"Shortest quote: {shortest_quote} This quote is {len(shortest_quote)} characters.")

#tag analysis
most_popular_tag = max(tag_count, key=tag_count.get)
total_tags = sum(tag_count.values())

print("\nTag Analysis:")
print("Distribution of tags:")
for tag, count in tag_count.items():
    print(f"{tag}: {count} occurrences")

print(f"\nMost popular tag: {most_popular_tag}")
print(f"Total number of tags used across all quotes: {total_tags}")

#import plotly
from plotly.graph_objs import bar
from plotly import offline


#top 10 descending for authors and tags
sorted_author_count = sorted(author_count.items(), key=lambda x: x[1], reverse=True)
top_10_authors = sorted_author_count[:10]

sorted_tag_count = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
top_10_tags = sorted_tag_count[:10]

#plot1
data = [
    {
        "type": 'bar',
        "x": [author for author, count in top_10_authors],
        "y": [count for author, count in top_10_authors],
        "marker": {
            "color": "rgb(60,100,150)",
            "line": {"width": 1.5, "color": "rgb(25,25,25)"},
        },
        "opacity": 0.6
    }
]

my_layout = {
    "title": "Top 10 Authors by Quote Count",
    "xaxis": {"title": "Authors"},
    "yaxis": {"title": "# of quotes"}
}

fig = {"data": data, "layout": my_layout}

offline.plot(fig, filename="top10authors.html")

#plot2
data2 = [
    {
        "type": 'bar',
        "x": [tag for tag, count in top_10_tags],
        "y": [count for tag, count in top_10_tags],
        "marker": {
            "color": "rgb(60,100,150)",
            "line": {"width": 1.5, "color": "rgb(25,25,25)"},
        },
        "opacity": 0.6
    }
]

my_layout2 = {
    "title": "Top 10 Tags by Occurrence Count",
    "xaxis": {"title": "Tag"},
    "yaxis": {"title": "# of occurrences"}
}

fig2 = {"data": data2, "layout": my_layout2}

offline.plot(fig2, filename="top10tags.html")