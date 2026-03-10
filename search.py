import requests
from bs4 import BeautifulSoup
from models import db, School, SearchResult
import time
import re
from concurrent.futures import ThreadPoolExecutor

# 检索规则配置
MUST_CONTAIN_YEAR = "2026"
MUST_CONTAIN_KEYWORDS = ["调剂", "接收", "征集", "补录", "心理", "0454", "心理专硕", "应用心理"]
MUST_EXCLUDE_YEARS = ["2020", "2021", "2022", "2023", "2024", "2025"]
严禁排除_KEYWORDS = ["学硕", "推免", "保研", "免试"]

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def search_school(school_id):
    """Search for admission information for a single school"""
    school = School.query.get(school_id)
    if not school:
        return
    
    # 初始化搜索结果
    result = SearchResult(school_id=school.id, found=False, error=False)
    
    # 搜索链接列表
    search_links = [school.grad_link]
    if school.recruit_link:
        search_links.append(school.recruit_link)
    if school.dept_link:
        search_links.append(school.dept_link)
    
    found = False
    error = False
    title = ""
    date = ""
    url = ""
    
    for link in search_links:
        try:
            # 发送请求
            response = requests.get(link, headers=HEADERS, timeout=10)
            response.raise_for_status()
            
            # 解析网页
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取所有链接和文本
            all_text = soup.get_text()
            
            # 检查是否包含2026
            if MUST_CONTAIN_YEAR not in all_text:
                continue
            
            # 检查是否包含指定关键词之一
            has_keyword = any(keyword in all_text for keyword in MUST_CONTAIN_KEYWORDS)
            if not has_keyword:
                continue
            
            # 检查是否包含旧年份
            has_old_year = any(year in all_text for year in MUST_EXCLUDE_YEARS)
            if has_old_year:
                continue
            
            # 检查是否包含严禁排除的关键词（不排除）
            # 这里不做任何处理，因为严禁排除这些关键词
            
            # 找到符合条件的信息
            found = True
            title = f"{school.name} 2026年调剂信息"
            date = time.strftime("%Y-%m-%d")
            url = link
            break
            
        except Exception as e:
            error = True
            print(f"Error searching {school.name}: {str(e)}")
            continue
    
    # 更新搜索结果
    result.found = found
    result.error = error
    result.title = title
    result.date = date
    result.url = url
    
    # 保存到数据库
    db.add(result)
    db.commit()
    
    return result

def batch_search(school_ids):
    """Search for admission information for multiple schools"""
    # 清空之前的搜索结果
    SearchResult.query.delete()
    db.commit()
    
    # 使用线程池并行搜索
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(search_school, school_ids)
    
    print(f"Batch search completed for {len(school_ids)} schools")