import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

# 在 Vercel 环境下，显式指定模板文件夹为当前目录
app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))
app.secret_key = 'peng_peng_health_secret_key'

# 翻译字典
translations = {
    'zh': {
        'title': '蓬蓬科普',
        'brand': '蓬蓬科普',
        'nav_home': '首页',
        'nav_kb': '用药知识库',
        'nav_personal': '个性化中心',
        'nav_topics': '专题区',
        'nav_about': '关于我们',
        'lang_zh': '中文',
        'lang_en': 'English',
        'welcome_title': '欢迎来到蓬蓬科普',
        'welcome_subtitle': '为您提供最专业的肿瘤用药知识',
        'about_title': '关于我们',
        'about_bg_title': '项目背景与目标',
        'about_bg_p1': '本项目旨在运用机器学习技术，搭建一个基于人际连续性的社区老年肿瘤患者用药科普教育新体系。随着我国人口老龄化趋势加剧，老年肿瘤患者数量逐年增多，他们往往面临多病共存、多重用药、生理功能衰退等复杂情况，导致用药风险增高，用药依从性差，严重影响治疗效果和生活质量。',
        'about_bg_p2': '传统的用药教育模式往往缺乏针对性和个性化，难以满足老年患者的特殊需求。本平台致力于解决这一痛点，通过整合权威的用药科普知识，结合机器学习算法，为老年肿瘤患者提供个性化的信息筛选 and 智能推荐服务，帮助他们及其家属更清晰、便捷地获取所需用药知识，提高用药安全性和有效性，最终改善患者的健康结局。',
        'about_tech_title': '核心技术',
        'about_tech_intro': '平台的核心技术依托于项目申报书中提出的方案，主要包括：',
        'about_tech_li1_title': '知识图谱构建:',
        'about_tech_li1_desc': '系统化梳理和组织老年肿瘤用药相关的知识，包括药物信息、疾病信息、症状、不良反应、相互作用等，形成结构化的知识网络，为精准检索和智能推荐奠定基础。',
        'about_tech_li2_title': '分面检索:',
        'about_tech_li2_desc': '基于知识图谱，提供多维度、层级化的信息筛选方式，帮助用户快速定位到所需的科普内容。',
        'about_tech_li3_title': '机器学习与个性化推荐:',
        'about_tech_li3_desc': '通过分析用户提供的个人情况（如肿瘤类型、年龄、合并症等） and 浏览行为，构建用户画像，利用机器学习算法（如协同过滤、基于内容的推荐等）实现个性化的科普信息推送。',
        'about_data_title': '数据来源与权威性',
        'about_data_p1': '本平台提供的所有科普信息均来源于权威医学指南、专业医学文献、以及临床药学专家的经验总结。我们会尽最大努力确保信息的准确性和时效性。项目团队由重庆大学附属肿瘤医院的药学专家和技术人员组成，致力于提供高质量的科普内容。',
        'about_disclaimer_title': '免责声明',
        'about_disclaimer_p1': '重要提示： 本网站提供的所有信息仅用于科普教育目的，不能替代任何专业的医疗诊断、治疗建议 or 处方。老年肿瘤患者的用药方案复杂且个体差异大，请务必在专业医师 or 药师的指导下进行治疗和用药调整。',
        'about_disclaimer_p2': '若您在浏览本网站内容后有任何关于自身健康状况 or 治疗方案的疑问，请及时咨询您的主治医生或相关医疗专业人士。对于因依赖本网站信息而采取的任何行动所导致的任何直接或间接损失，本平台不承担任何责任。',
        'about_contact_title': '联系我们',
        'about_contact_p1': '如果您对本平台有任何建议或疑问，欢迎通过以下方式联系我们：',
        'about_contact_leader': '项目负责人：白浩',
        'about_contact_phone': '联系电话：023-65079130 (此为申报书中电话，实际部署时可替换)',
        'about_contact_unit': '单位：重庆大学附属肿瘤医院 (此为申报书中单位，实际部署时可替换)'
    },
    'en': {
        'title': 'Peng Peng Health',
        'brand': 'Peng Peng Health',
        'nav_home': 'Home',
        'nav_kb': 'Drug Knowledge Base',
        'nav_personal': 'Personalization Center',
        'nav_topics': 'Special Topics',
        'nav_about': 'About Us',
        'lang_zh': '中文',
        'lang_en': 'English',
        'welcome_title': 'Welcome to Peng Peng Health',
        'welcome_subtitle': 'Providing you with the most professional cancer medication knowledge',
        'about_title': 'About Us',
        'about_bg_title': 'Project Background and Objectives',
        'about_bg_p1': 'This project aims to use machine learning technology to build a new system of medication science popularization education for community elderly cancer patients based on interpersonal continuity. With the intensification of the aging trend of China\'s population, the number of elderly cancer patients is increasing year by year. They often face complex situations such as coexistence of multiple diseases, multiple medications, and decline in physiological functions, leading to increased medication risks and poor medication compliance, which seriously affects treatment effects and quality of life.',
        'about_bg_p2': 'Traditional medication education models often lack pertinence and personalization, making it difficult to meet the special needs of elderly patients. This platform is committed to solving this pain point. By integrating authoritative medication science popularization knowledge and combining machine learning algorithms, it provides personalized information screening and intelligent recommendation services for elderly cancer patients, helping them and their families obtain the required medication knowledge more clearly and conveniently, improving medication safety and effectiveness, and ultimately improving patients\' health outcomes.',
        'about_tech_title': 'Core Technologies',
        'about_tech_intro': 'The core technology of the platform relies on the plan proposed in the project application, mainly including:',
        'about_tech_li1_title': 'Knowledge Graph Construction:',
        'about_tech_li1_desc': 'Systematically organizing knowledge related to elderly cancer medication, including drug information, disease information, symptoms, adverse reactions, interactions, etc., forming a structured knowledge network to lay the foundation for precise retrieval and intelligent recommendation.',
        'about_tech_li2_title': 'Faceted Search:',
        'about_tech_li2_desc': 'Based on the knowledge graph, it provides multi-dimensional and hierarchical information screening methods to help users quickly locate the required science popularization content.',
        'about_tech_li3_title': 'Machine Learning and Personalized Recommendation:',
        'about_tech_li3_desc': 'By analyzing the personal situation (such as tumor type, age, comorbidities, etc.) and browsing behavior provided by users, user profiles are constructed, and machine learning algorithms (such as collaborative filtering, content-based recommendation, etc.) are used to achieve personalized science popularization information push.',
        'about_data_title': 'Data Sources and Authority',
        'about_data_p1': 'All science popularization information provided by this platform comes from authoritative medical guides, professional medical literature, and the experience summary of clinical pharmacy experts. We will do our best to ensure the accuracy and timeliness of the information. The project team consists of pharmacy experts and technical personnel from Chongqing University Cancer Hospital, dedicated to providing high-quality science popularization content.',
        'about_disclaimer_title': 'Disclaimer',
        'about_disclaimer_p1': 'Important Note: All information provided on this website is for science popularization education purposes only and cannot replace any professional medical diagnosis, treatment advice or prescription. The medication regimen for elderly cancer patients is complex and has large individual differences. Please be sure to carry out treatment and medication adjustment under the guidance of a professional physician or pharmacist.',
        'about_disclaimer_p2': 'If you have any questions about your own health status or treatment plan after browsing the content of this website, please consult your attending physician or relevant medical professionals in time. This platform does not assume any responsibility for any direct or indirect losses caused by any actions taken based on the information on this website.',
        'about_contact_title': 'Contact Us',
        'about_contact_p1': 'If you have any suggestions or questions about this platform, please feel free to contact us through the following ways:',
        'about_contact_leader': 'Project Leader: Bai Hao',
        'about_contact_phone': 'Contact: 023-65079130 (Phone from proposal, can be replaced)',
        'about_contact_unit': 'Affiliation: Chongqing University Cancer Hospital (Affiliation from proposal, can be replaced)'
    }
}

@app.context_processor
def utility_processor():
    def translate(text):
        lang = session.get('lang', 'zh')
        # 如果是 key，直接翻译
        if text in translations[lang]:
            return translations[lang][text]
        # 如果是原文，尝试匹配
        for key, val in translations['zh'].items():
            if val == text:
                return translations[lang].get(key, text)
        return text
    return dict(_=translate)

@app.route('/')
def index():
    current_lang = session.get('lang', 'zh')
    return render_template('index.html', current_lang=current_lang)

@app.route('/knowledge_base')
def knowledge_base():
    current_lang = session.get('lang', 'zh')
    return render_template('knowledge_base.html', current_lang=current_lang)

@app.route('/personalization')
def personalization():
    current_lang = session.get('lang', 'zh')
    return render_template('personalization.html', current_lang=current_lang)

@app.route('/special_topics')
def special_topics():
    current_lang = session.get('lang', 'zh')
    return render_template('special_topics.html', current_lang=current_lang)

@app.route('/about')
def about():
    current_lang = session.get('lang', 'zh')
    return render_template('about.html', current_lang=current_lang)

@app.route('/set_lang')
def set_lang():
    lang = request.args.get('lang', 'zh')
    session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
