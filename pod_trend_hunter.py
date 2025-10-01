import requests
from bs4 import BeautifulSoup
import pandas as pd
import tweepy
import time  # For delays

# Replace with your FRESH X Bearer Token
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAB854gEAAAAAmsp0c3B%2B1%2FAXCwMy%2BkKEPsT7NZ0%3DNxDrsvCWAhc4Jb0XCSLadxNrd5VuRZsrfrUOyG07qOgEr6BjDG'

# Step 1: Scrape Redbubble with anti-403 headers
def scrape_redbubble(category='apparel'):
    url = f'https://www.redbubble.com/shop/{category}?sortOrder=popular'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',  # Recent Chrome
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.redbubble.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }
    time.sleep(1)  # Polite delay
    response = requests.get(url, headers=headers)
    print(f"Redbubble status: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed to fetch: {response.status_code}. Try VPN or more headers.")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Lambda for your hashed class (matches styles_box__54ba70e3 + variants)
    items = soup.find_all('div', class_=lambda x: x and 'styles_box__54ba70e3' in ' '.join(x))[:10]
    
    if not items:
        print("No products found—double-check class via inspect. Debug: Sample div classes:")
        sample_divs = [ ' '.join(d.get('class', [])) for d in soup.find_all('div')[:5] if d.get('class') ]
        print(sample_divs)
        return pd.DataFrame()
    
    products = []
    for i, item in enumerate(items, 1):
        # Title: Try h3, fallback to a/link
        title_elem = item.find('h3') or item.find('a', href=True)
        title = title_elem.text.strip() if title_elem else 'N/A'
        
        # Tags: Fallback to spans/links inside
        tag_elems = item.find_all(['span', 'a'], class_=lambda x: x and ('tag' in ' '.join(x).lower() or 'category' in ' '.join(x).lower()))[:3]
        tags = [t.text.strip() for t in tag_elems if t.text.strip()]
        
        products.append({'source': 'Redbubble', 'title': title, 'tags': tags, 'rank': i})
    
    df = pd.DataFrame(products)
    print(f"Scraped {len(df)} products.")
    return df

# Step 2: X trends (with auth debug)
def search_x_trends(query='print on demand designs OR POD merch', max_results=10):
    try:
        client = tweepy.Client(bearer_token=BEARER_TOKEN)
        # Quick auth test
        me = client.get_me()
        print("X auth good:", me.data.name if me.data else "Failed—check token!")
        
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
    except tweepy.TweepyException as e:
        print(f"X API error: {e}. Regen token or check permissions.")
        return pd.DataFrame()

# Step 3: Analyze (guarded)
def analyze_trends(rb_df, x_df):
    if rb_df.empty or x_df.empty:
        return pd.DataFrame([{'trend': 'No data—fix scrapes above', 'score': 0, 'sources': 'N/A'}])
    
    trends = []
    for _, rb in rb_df.iterrows():
        score = 0
        sources = [rb['source']]
        for _, x in x_df.iterrows():
            if any(word in rb['title'].lower() for word in x['title'].lower().split()):
                score += x['engagement']
                sources.append(x['source'])
        trends.append({'trend': rb['title'], 'score': score, 'sources': sources})
    
    return pd.DataFrame(trends).sort_values('score', ascending=False).head(5)

# Run
if __name__ == '__main__':
    print("Hunting POD trends...\n")
    
    rb_data = scrape_redbubble()
    if not rb_data.empty:
        print("Redbubble Tops:\n", rb_data[['title', 'rank']].to_string(index=False))
    else:
        print("Redbubble skipped—focus on headers/token first.")
    
    x_data = search_x_trends()
    if not x_data.empty:
        print("\nX Buzz:\n", x_data[['title', 'engagement']].to_string(index=False))
    else:
        print("\nX skipped—auth issue.")
    
    trends = analyze_trends(rb_data, x_data)
    print("\nTop Overlaps:\n", trends.to_string(index=False))
    
    trends.to_csv('pod_trends_today.csv', index=False)
    print("\nCSV saved. If still 403/401, holler with output!")