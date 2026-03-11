import requests
from bs4 import BeautifulSoup
from models import School
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse

MUST_CONTAIN_YEAR = "2025"
MUST_CONTAIN_KEYWORDS = ["调剂", "接收", "征集", "补录", "心理", "转专业", "实施细则", "全日制", "本科"]
MUST_EXCLUDE_YEARS = ["2020", "2021", "2022"]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}

def get_base_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def is_valid_announcement_url(url):
    invalid_patterns = [
        'javascript:',
        'mailto:',
        'tel:',
        '#',
        'weixin.qq.com',
        'mp.weixin.qq.com',
        'zhihu.com',
        'baidu.com',
        'bilibili.com',
        'douban.com',
        'weibo.com',
        'kaoyan.com',
        'eol.cn',
        'chsi.com.cn',
        'koolearn.com',
        'xueersi.com',
        'zhongkao.com',
        'exam8.com',
        '51test.net',
        'test163.net',
        'edu-edu.com',
        'sina.com.cn',
        'sohu.com',
        '163.com',
        'qq.com'
    ]
    for pattern in invalid_patterns:
        if pattern in url.lower():
            return False
    return True

def search_school_with_data(school_data):
    """Search for admission information for a single school using pre-fetched data"""
    school_id = school_data['id']
    school_name = school_data['name']
    search_links = [school_data['links']['grad']]
    if school_data['links'].get('recruit'):
        search_links.append(school_data['links']['recruit'])
    if school_data['links'].get('dept'):
        search_links.append(school_data['links']['dept'])
    
    found = False
    error = False
    error_message = ""
    title = ""
    date = ""
    url = school_data['links']['grad']
    best_match = None
    best_match_score = 0
    
    for link in search_links:
        try:
            session = requests.Session()
            response = session.get(link, headers=HEADERS, timeout=20, allow_redirects=True)
            response.raise_for_status()
            
            final_url = response.url
            soup = BeautifulSoup(response.content, 'html.parser')
            base_url = get_base_url(final_url)
            
            all_text = soup.get_text(separator=' ', strip=True)
            
            if MUST_CONTAIN_YEAR not in all_text:
                continue
            
            has_keyword = any(keyword in all_text for keyword in MUST_CONTAIN_KEYWORDS)
            if not has_keyword:
                continue
            
            has_old_year = any(year in all_text for year in MUST_EXCLUDE_YEARS)
            if has_old_year:
                continue
            
            found = True
            title = f"{school_name} 2025年调剂信息"
            date = time.strftime("%Y-%m-%d")
            url = final_url
            
            all_links = soup.find_all('a', href=True)
            
            for a_tag in all_links:
                href = a_tag.get('href', '')
                link_text = a_tag.get_text(strip=True)
                
                if not href or not is_valid_announcement_url(href):
                    continue
                
                full_url = urljoin(base_url, href)
                
                score = 0
                
                if MUST_CONTAIN_YEAR in link_text:
                    score += 10
                
                keyword_count = sum(1 for kw in MUST_CONTAIN_KEYWORDS if kw in link_text)
                score += keyword_count * 5
                
                if len(link_text) > 5 and len(link_text) < 50:
                    score += 3
                
                if score > best_match_score:
                    best_match_score = score
                    best_match = {
                        'url': full_url,
                        'title': link_text if link_text else title,
                        'text': link_text
                    }
            
            if best_match and best_match_score > 0:
                url = best_match['url']
                title = best_match['title']
                break
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                error_message = "403: 网站拒绝访问"
            else:
                error_message = f"HTTP错误: {e.response.status_code}"
            error = True
            print(f"Error searching {school_name}: {error_message}")
            continue
        except requests.exceptions.Timeout:
            error_message = "请求超时"
            error = True
            print(f"Error searching {school_name}: {error_message}")
            continue
        except requests.exceptions.TooManyRedirects:
            error_message = "重定向次数过多"
            error = True
            print(f"Error searching {school_name}: {error_message}")
            continue
        except requests.exceptions.RequestException as e:
            error_message = f"网络错误: {str(e)[:40]}"
            error = True
            print(f"Error searching {school_name}: {error_message}")
            continue
        except Exception as e:
            error_message = f"解析错误: {str(e)[:40]}"
            error = True
            print(f"Error searching {school_name}: {error_message}")
            continue
    
    return {
        'school_id': school_id,
        'found': found,
        'error': error,
        'error_message': error_message,
        'title': title,
        'date': date,
        'url': url
    }

def search_school(school):
    """Search for admission information for a single school"""
    school_data = {
        'id': school.id,
        'name': school.name,
        'links': {
            'main': school.main_link,
            'grad': school.grad_link,
            'dept': school.dept_link,
            'recruit': school.recruit_link
        }
    }
    return search_school_with_data(school_data)

def batch_search(school_data_list):
    """Search for admission information for multiple schools"""
    results = []
    
    def search_and_append(school_data):
        result = search_school_with_data(school_data)
        results.append(result)
        print(f"Completed: {school_data['name']}")
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(search_and_append, sd) for sd in school_data_list]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in search task: {e}")
    
    return results
