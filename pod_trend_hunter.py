import requests
from bs4 import BeautifulSoup
import pandas as pd
import tweepy
from io import StringIO

# Replace with your X Bearer Token
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAB854gEAAAAAYGDuCWgWvp3DoaPqFSepzfmDs%2Fw%3Do49HtEnOZAfG2XyNIwa8kmxDLf5fgEbxDt7nAeXdfoj0092MgZ'
# Step 1: Scrape Redbubble best-sellers (example: Apparel category)
def scrape_redbubble(category='apparel'):
    url = f'https://www.redbubble.com/shop/{category}?sortOrder=popular'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # UPDATE THIS SELECTOR based on your inspection (right-click > Inspect)
    items = soup.find_all('div', class_='styles_box__54ba70e3')[:10]  # Matches all variants
    
    if not items:
        print("No products found—check the class selector! Inspect the page for the current div class around titles.")
        print("Sample debug: First few divs on page:", [d.get('class') for d in soup.find_all('div')[:5]])
        return pd.DataFrame()
    
    products = []
    for i, item in enumerate(items, 1):
        title_elem = item.find('h3')
        title = title_elem.text.strip() if title_elem else 'N/A'
        
        # Better tags fallback: Look for common tag spans (update if needed)
        tag_elems = item.find_all('span', class_='tag') or item.find_all('a', href=True)[:3]  # Or inspect for real tags
        tags = [t.text.strip() for t in tag_elems if t.text.strip()]
        
        products.append({'source': 'Redbubble', 'title': title, 'tags': tags, 'rank': i})
    
    df = pd.DataFrame(products)
    print(f"Scraped {len(df)} products successfully.")
    return df

# Step 2: Fetch X trends via semantic search (unchanged)
def search_x_trends(query='print on demand designs OR POD merch', max_results=10):
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    
    tweets = tweepy.Paginator(
        client.search_recent_tweets,
        query=query + ' -is:retweet lang:en',
        tweet_fields=['public_metrics', 'created_at'],
        max_results=max_results
    ).flatten(limit=max_results)
    
    posts = []
    for tweet in tweets:
        posts.append({
            'source': 'X',
            'title': tweet.text[:50] + '...' if len(tweet.text) > 50 else tweet.text,
            'engagement': tweet.public_metrics['like_count'] + tweet.public_metrics['retweet_count'],
            'created': tweet.created_at
        })
    return pd.DataFrame(posts).sort_values('engagement', ascending=False)

# Step 3: Mash & Rank (simple overlap on keywords)
def analyze_trends(rb_df, x_df):
    if rb_df.empty or x_df.empty:
        return pd.DataFrame({'trend': ['No data'], 'score': [0], 'sources': ['Check scrapes']})
    
    trends = []
    for _, rb in rb_df.iterrows():
        score = 0
        matching_sources = [rb['source']]
        for _, x in x_df.iterrows():
            if any(word in rb['title'].lower() for word in x['title'].lower().split()):
                score += x['engagement']
                matching_sources.append(x['source'])
        trends.append({'trend': rb['title'], 'score': score, 'sources': matching_sources})
    
    ranked = pd.DataFrame(trends).sort_values('score', ascending=False).head(5)
    return ranked

# Run the MVP
if __name__ == '__main__':
    print("Hunting POD trends...\n")
    
    rb_data = scrape_redbubble()
    if not rb_data.empty:
        print("Redbubble Tops:\n", rb_data[['title', 'rank']].to_string(index=False))
    else:
        print("Skipping Redbubble print—fix the selector first!")
    
    x_data = search_x_trends()
    print("\nX Buzz:\n", x_data[['title', 'engagement']].to_string(index=False))
    
    trends = analyze_trends(rb_data, x_data)
    print("\nTop Overlaps (Ranked by Hype Score):\n", trends.to_string(index=False))
    
    # Export to CSV
    trends.to_csv('pod_trends_today.csv', index=False)
    print("\nSaved to pod_trends_today.csv – Tweak the selector and re-run for full magic!")