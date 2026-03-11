import csv
from models import db, School, SearchResult, Collection
import os
import datetime

def export_to_csv():
    """Export search results to CSV"""
    # 获取所有学校
    schools = School.query.all()
    
    # 获取所有搜索结果
    results = SearchResult.query.all()
    result_dict = {r.school_id: r for r in results}
    
    # 获取所有收藏
    collections = Collection.query.all()
    collected_ids = {c.school_id for c in collections}
    
    # 创建导出目录
    export_dir = "exports"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # 生成文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(export_dir, f"心理学调剂监控_{timestamp}.csv")
    
    # 导出到CSV
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ["院校名称", "省市", "是否收藏", "官网", "研究生院", "心理学院", "研招公告", "是否找到调剂信息", "检索到的文档标题", "调剂信息链接", "检索状态"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for school in schools:
            result = result_dict.get(school.id)
            writer.writerow({
                "院校名称": school.name,
                "省市": school.province,
                "是否收藏": "是" if school.id in collected_ids else "否",
                "官网": school.main_link,
                "研究生院": school.grad_link,
                "心理学院": school.dept_link or "",
                "研招公告": school.recruit_link or "",
                "是否找到调剂信息": "是" if result and result.found else "否",
                "检索到的文档标题": result.title if result else "",
                "调剂信息链接": result.url if result else "",
                "检索状态": "成功" if result and not result.error else "失败" if result and result.error else "未检索"
            })
    
    print(f"Exported to {file_path}")
    return file_path