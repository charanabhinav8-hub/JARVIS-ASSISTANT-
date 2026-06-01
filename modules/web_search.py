import requests
from bs4 import BeautifulSoup
from utils.logger import logger

class WebSearch:
    """Web search functionality"""
    
    def __init__(self):
        self.search_url = "https://www.google.com/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search(self, query, num_results=5):
        """Search the web using Google"""
        try:
            params = {
                'q': query,
                'num': num_results
            }
            
            response = requests.get(self.search_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = self._parse_results(soup)
            
            logger.info(f"Found {len(results)} results for query: {query}")
            return results
        
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return []
    
    def _parse_results(self, soup):
        """Parse search results from Google"""
        results = []
        
        try:
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:5]:
                try:
                    title_elem = result.find('h3')
                    link_elem = result.find('a')
                    desc_elem = result.find('span', class_='st')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text()
                        link = link_elem.get('href')
                        description = desc_elem.get_text() if desc_elem else "No description"
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'description': description
                        })
                except:
                    continue
        
        except Exception as e:
            logger.error(f"Error parsing search results: {e}")
        
        return results
    
    def get_weather(self, location):
        """Get weather information"""
        try:
            # Using wttr.in API (no key required)
            response = requests.get(f"https://wttr.in/{location}?format=j1", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current = data['current_condition'][0]
            
            weather_info = {
                'location': location,
                'temperature': current['temp_C'],
                'condition': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph']
            }
            
            logger.info(f"Weather data retrieved for {location}")
            return weather_info
        
        except Exception as e:
            logger.error(f"Weather retrieval error: {e}")
            return None

class NewsSearch:
    """News search functionality"""
    
    def __init__(self):
        self.search_url = "https://news.google.com/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_news(self, query, num_results=5):
        """Search for news articles"""
        try:
            web_search = WebSearch()
            results = web_search.search(f"{query} news", num_results)
            logger.info(f"Found {len(results)} news articles")
            return results
        except Exception as e:
            logger.error(f"News search error: {e}")
            return []
