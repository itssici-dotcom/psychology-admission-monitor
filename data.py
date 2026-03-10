from models import db, School

def initialize_schools():
    """Initialize schools data"""
    # Check if schools already exist
    if School.query.count() > 0:
        return
    
    # Schools data
    schools_data = [
        {"name": "首都师范大学", "province": "北京", "links": {"main": "https://www.cnu.edu.cn/", "grad": "https://grad.cnu.edu.cn/", "dept": "https://psy.cnu.edu.cn/"}},
        {"name": "北京联合大学", "province": "北京", "links": {"main": "https://www.buu.edu.cn/", "grad": "https://graduate.buu.edu.cn/", "dept": "https://tc.buu.edu.cn/"}},
        {"name": "天津师范大学", "province": "天津", "links": {"main": "https://www.tjnu.edu.cn/", "grad": "https://yjsy.tjnu.edu.cn/", "dept": "https://psych.tjnu.edu.cn/"}},
        {"name": "天津体育学院", "province": "天津", "links": {"main": "https://www.tjus.edu.cn/", "grad": "https://yjsb.tjus.edu.cn/", "dept": "https://tyjyxy.tjus.edu.cn/gyxy/xyjj.htm"}},
        {"name": "河北大学", "province": "河北", "links": {"main": "https://www.hbu.edu.cn/", "grad": "https://yjsy.hbu.edu.cn/", "dept": "https://jiaoyu.hbu.edu.cn/"}},
        {"name": "河北师范大学", "province": "河北", "links": {"main": "https://www.hebtu.edu.cn/", "grad": "https://yjsy.hebtu.edu.cn/", "dept": "https://psych.hebtu.edu.cn/"}},
        {"name": "河北科技大学", "province": "河北", "links": {"main": "https://www.hebust.edu.cn/", "grad": "https://yjsxy.web.hebust.edu.cn/", "dept": "https://wenfaxy.web.hebust.edu.cn/xygk/xyjj/index.htm"}},
        {"name": "华北理工大学", "province": "河北", "links": {"main": "https://www.ncst.edu.cn/", "grad": "https://yjsxy.ncst.edu.cn/", "dept": "https://xlx.ncst.edu.cn/"}},
        {"name": "承德医学院", "province": "河北", "links": {"main": "https://www.cdmc.edu.cn/", "grad": "https://yjs.cdmc.edu.cn/", "dept": "https://xl.cdmc.edu.cn/"}},
        {"name": "山西大学", "province": "山西", "links": {"main": "https://www.sxu.edu.cn/", "grad": "https://grs.sxu.edu.cn/", "dept": "https://jky.sxu.edu.cn/"}},
        {"name": "山西师范大学", "province": "山西", "links": {"main": "https://www.sxnu.edu.cn/", "grad": "https://grc.sxnu.edu.cn/", "dept": "https://xlxy.sxnu.edu.cn/"}},
        {"name": "辽宁师范大学", "province": "辽宁", "links": {"main": "https://www.lnnu.edu.cn/", "grad": "https://master.lnnu.edu.cn/", "dept": "https://xlxy.lnnu.edu.cn/"}},
        {"name": "沈阳师范大学", "province": "辽宁", "links": {"main": "https://www.synu.edu.cn/", "grad": "https://yjs.synu.edu.cn/", "dept": "https://jky.synu.edu.cn/"}},
        {"name": "中国医科大学", "province": "辽宁", "links": {"main": "https://www.cmu.edu.cn/", "grad": "https://www.cmu.edu.cn/cmuyjs/", "dept": "https://www.cmu.edu.cn/yxrw/"}},
        {"name": "大连医科大学", "province": "辽宁", "links": {"main": "https://www.dmu.edu.cn/", "grad": "https://yjs.dmu.edu.cn/"}},
        {"name": "沈阳体育学院", "province": "辽宁", "links": {"main": "https://www.syty.edu.cn/", "grad": "https://yjs.syty.edu.cn/", "dept": "https://ydrt.syty.edu.cn/"}},
        {"name": "吉林师范大学", "province": "吉林", "links": {"main": "https://www.jlnu.edu.cn/", "grad": "https://www.jlnu.edu.cn/yjsy/", "dept": "https://www.jlnu.edu.cn/jykx/index.htm"}},
        {"name": "长春师范大学", "province": "吉林", "links": {"main": "https://www.ccsfu.edu.cn/", "grad": "https://yjs.ccsfu.edu.cn/", "dept": "https://jiaoke.ccsfu.edu.cn/"}},
        {"name": "黑龙江大学", "province": "黑龙江", "links": {"main": "https://www.hlju.edu.cn/", "grad": "https://yjsy.hlju.edu.cn/", "dept": "https://jykxyjy.hlju.edu.cn/"}},
        {"name": "哈尔滨师范大学", "province": "黑龙江", "links": {"main": "http://www.hrbnu.edu.cn/", "grad": "http://yjsxy.hrbnu.edu.cn/info/1021/2374.htm", "dept": "http://jykxxy.hrbnu.edu.cn/"}},
        {"name": "齐齐哈尔大学", "province": "黑龙江", "links": {"main": "https://www.qqhru.edu.cn/", "grad": "https://yjs.qqhru.edu.cn/", "dept": "https://zs.qqhru.edu.cn/zyjs/jsjyxy.htm"}},
        {"name": "上海师范大学", "province": "上海", "links": {"main": "https://www.shnu.edu.cn/", "grad": "https://yjsc.shnu.edu.cn/", "dept": "https://psy.shnu.edu.cn/"}},
        {"name": "上海体育学院（上海体育大学）", "province": "上海", "links": {"main": "https://www.sus.edu.cn/", "grad": "https://yjsc.sus.edu.cn/", "dept": "https://xlxy.sus.edu.cn/"}},
        {"name": "江苏师范大学", "province": "江苏", "links": {"main": "http://www.jsnu.edu.cn/", "grad": "http://yjsy.jsnu.edu.cn/", "dept": "http://edu.jsnu.edu.cn/"}},
        {"name": "扬州大学", "province": "江苏", "links": {"main": "https://www.yzu.edu.cn/", "grad": "https://yjsc.yzu.edu.cn/", "dept": "https://jykxxy.yzu.edu.cn/xygk/xyjj.htm"}},
        {"name": "南京医科大学", "province": "江苏", "links": {"main": "https://www.njmu.edu.cn/", "grad": "https://yjsy.njmu.edu.cn/", "dept": "https://silin.njmu.edu.cn/", "recruit": "https://yjszs.njmu.edu.cn/"}},
        {"name": "南京体育学院", "province": "江苏", "links": {"main": "https://www.nsi.edu.cn/", "grad": "https://www.nsi.edu.cn/yjs/main.htm", "dept": "https://www.nsi.edu.cn/ydjkkxx/main.htm"}},
        {"name": "浙江理工大学", "province": "浙江", "links": {"main": "https://www.zstu.edu.cn/", "grad": "https://gradschool.zstu.edu.cn/", "dept": "https://sci.zstu.edu.cn/"}},
        {"name": "杭州师范大学", "province": "浙江", "links": {"main": "https://www.hznu.edu.cn/", "grad": "https://yjs.hznu.edu.cn/", "dept": "https://jyxy.hznu.edu.cn/c/2022-05-01/2702939.shtml"}},
        {"name": "浙江师范大学", "province": "浙江", "links": {"main": "https://www.zjnu.edu.cn/", "grad": "https://yjsb.zjnu.edu.cn/", "dept": "https://jky.zjnu.edu.cn/"}},
        {"name": "宁波大学", "province": "浙江", "links": {"main": "https://www.nbu.edu.cn/", "grad": "https://graduate.nbu.edu.cn/", "dept": "https://jsjy.nbu.edu.cn/"}},
        {"name": "安徽师范大学", "province": "安徽", "links": {"main": "https://www.ahnu.edu.cn/", "grad": "https://gs.ahnu.edu.cn/", "dept": "https://edu.ahnu.edu.cn/安徽师大"}},
        {"name": "合肥师范学院", "province": "安徽", "links": {"main": "https://www.hfnu.edu.cn/", "grad": "https://yjsc.hfnu.edu.cn/", "dept": "https://edu.ahnu.edu.cn/"}},
        {"name": "皖南医学院", "province": "安徽", "links": {"main": "https://www.wnmc.edu.cn/", "grad": "https://yjs.wnmc.edu.cn/"}},
        {"name": "福建师范大学", "province": "福建", "links": {"main": "https://www.fjnu.edu.cn/", "grad": "https://yjsy.fjnu.edu.cn/", "dept": "https://psy.fjnu.edu.cn/"}},
        {"name": "闽南师范大学", "province": "福建", "links": {"main": "https://www.mnnu.edu.cn/", "grad": "https://yjsc.mnnu.edu.cn/", "dept": "https://jkxy.mnnu.edu.cn/index.htm"}},
        {"name": "江西师范大学", "province": "江西", "links": {"main": "https://www.jxnu.edu.cn/", "grad": "https://graduate.jxnu.edu.cn/", "dept": "https://psych.jxnu.edu.cn/"}},
        {"name": "赣南师范大学", "province": "江西", "links": {"main": "https://www.gnnu.edu.cn/", "grad": "https://yjs.gnnu.edu.cn/index.htm", "dept": "https://jkxy.gnnu.edu.cn/info/1059/1098.htm"}},
        {"name": "山东师范大学", "province": "山东", "links": {"main": "https://www.sdnu.edu.cn/", "grad": "http://www.yjs.sdnu.edu.cn/", "dept": "http://www.psy.sdnu.edu.cn/"}},
        {"name": "济南大学", "province": "山东", "links": {"main": "https://www.ujn.edu.cn/", "grad": "https://yz.ujn.edu.cn/", "dept": "https://sep.ujn.edu.cn/"}},
        {"name": "曲阜师范大学", "province": "山东", "links": {"main": "https://www.qfnu.edu.cn/", "grad": "https://yjs.qfnu.edu.cn/", "dept": "https://xlxy.qfnu.edu.cn/"}},
        {"name": "鲁东大学", "province": "山东", "links": {"main": "https://www.ldu.edu.cn/", "grad": "https://grad.ldu.edu.cn/", "dept": "https://jyxy.ldu.edu.cn/"}},
        {"name": "聊城大学", "province": "山东", "links": {"main": "https://www.lcu.edu.cn/", "grad": "https://yjsc.lcu.edu.cn/", "dept": "https://jykxxy.lcu.edu.cn/sypc/index.htm"}},
        {"name": "山东中医药大学", "province": "山东", "links": {"main": "https://www.sdutcm.edu.cn/", "grad": "https://yjs.sdutcm.edu.cn/"}},
        {"name": "青岛大学", "province": "山东", "links": {"main": "https://www.qdu.edu.cn/", "grad": "https://grad.qdu.edu.cn/", "dept": "https://sf.qdu.edu.cn/"}},
        {"name": "河南大学", "province": "河南", "links": {"main": "https://www.henu.edu.cn/", "grad": "https://grs.henu.edu.cn/", "dept": "https://jykx.henu.edu.cn/"}},
        {"name": "河南师范大学", "province": "河南", "links": {"main": "https://www.htu.edu.cn/", "grad": "https://www.htu.edu.cn/yjsxy/main.htm", "dept": "https://www.htu.edu.cn/tjb/xlxy/list.htm"}},
        {"name": "信阳师范大学", "province": "河南", "links": {"main": "https://www.xynu.edu.cn/", "grad": "http://yjs.xynu.edu.cn/", "dept": "http://jky.xynu.edu.cn/"}},
        {"name": "湖北大学", "province": "湖北", "links": {"main": "https://www.hubu.edu.cn/", "grad": "https://gs.hubu.edu.cn/", "dept": "https://sfxy.hubu.edu.cn/"}},
        {"name": "武汉体育学院", "province": "湖北", "links": {"main": "https://www.whsu.edu.cn/", "grad": "https://yjsy.whsu.edu.cn/"}},
        {"name": "江汉大学", "province": "湖北", "links": {"main": "https://www.jhun.edu.cn/", "grad": "https://gs.jhun.edu.cn/", "dept": "https://jyxy.jhun.edu.cn/"}},
        {"name": "湖南科技大学", "province": "湖南", "links": {"main": "https://www.hnust.edu.cn/", "grad": "https://graduate.hnust.edu.cn/", "dept": "https://jyxy.hnust.edu.cn/"}},
        {"name": "衡阳师范学院", "province": "湖南", "links": {"main": "https://www.hynu.edu.cn/", "grad": "https://xkjsb.hynu.edu.cn/", "dept": "https://jykxxy.hynu.edu.cn/"}},
        {"name": "深圳大学", "province": "广东", "links": {"main": "https://www.szu.edu.cn/", "grad": "https://yz.szu.edu.cn/", "dept": "https://psy.szu.edu.cn/"}},
        {"name": "广州大学", "province": "广东", "links": {"main": "https://www.gzhu.edu.cn/", "grad": "https://yjsy.gzhu.edu.cn/"}},
        {"name": "广东外语外贸大学", "province": "广东", "links": {"main": "https://www.gdufs.edu.cn/", "grad": "https://gwyjs.gdufs.edu.cn/", "dept": "https://zg.gdufs.edu.cn/"}},
        {"name": "南方医科大学", "province": "广东", "links": {"main": "https://www.smu.edu.cn/", "grad": "https://yjs.smu.edu.cn/", "dept": "https://portal.smu.edu.cn/gwxy/"}},
        {"name": "广州医科大学", "province": "广东", "links": {"main": "https://www.gzhmu.edu.cn/", "grad": "https://yjs.gzhmu.edu.cn/", "dept": "https://yjs.gzhmu.edu.cn/dsdw/axklcz/ggwsyyfyx/wsglxy.htm"}},
        {"name": "重庆师范大学", "province": "重庆", "links": {"main": "https://www.cqnu.edu.cn/", "grad": "https://graduate.cqnu.edu.cn/", "dept": "https://jykx.cqnu.edu.cn/szdw1/xlxx.htm"}},
        {"name": "重庆医科大学", "province": "重庆", "links": {"main": "https://www.cqmu.edu.cn/", "grad": "https://yjsy.cqmu.edu.cn/", "dept": "http://www.uhcmu.com/info/1047/9419.htm"}},
        {"name": "西华师范大学", "province": "四川", "links": {"main": "https://www.cwnu.edu.cn/", "grad": "https://yjsy.cwnu.edu.cn/", "dept": "https://es.cwnu.edu.cn/"}},
        {"name": "成都医学院", "province": "四川", "links": {"main": "https://www.cmc.edu.cn/", "grad": "https://yjsy.cmc.edu.cn/", "dept": "https://psy.cmc.edu.cn/"}},
        {"name": "西安体育学院", "province": "陕西", "links": {"main": "https://www.xaipe.edu.cn/", "grad": "https://www.xaipe.edu.cn/yjsb/", "dept": "https://www.xaipe.edu.cn/jkkxx/"}}
    ]
    
    # Add schools to database
    for school_data in schools_data:
        school = School(
            name=school_data['name'],
            province=school_data['province'],
            main_link=school_data['links']['main'],
            grad_link=school_data['links']['grad'],
            dept_link=school_data['links'].get('dept'),
            recruit_link=school_data['links'].get('recruit')
        )
        db.session.add(school)
    
    db.session.commit()
    print(f"Initialized {len(schools_data)} schools")