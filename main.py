from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import os

# 在 Vercel 环境中，所有文件都在根目录
# 显式设置 template_folder='.' 以确保 Jinja2 能找到 index.html 等文件
app = Flask(__name__, template_folder='.', static_folder='.')
app.secret_key = os.environ.get('SECRET_KEY', 'some_secret_key')

# 翻译字典
translations = {
    'zh': {
        '首页': '首页',
        '用药知识库': '用药知识库',
        '个性化中心': '个性化中心',
        '专题区': '专题区',
        '关于我们': '关于我们',
        '联系我们': '联系我们',
        '蓬蓬科普': '蓬蓬科普',
        '老年肿瘤患者用药科普个性化筛选和推荐': '老年肿瘤患者用药科普个性化筛选和推荐',
        '欢迎来到蓬蓬科普': '欢迎来到蓬蓬科普',
        '为老年肿瘤患者提供个性化的用药科普和推荐': '为老年肿瘤患者提供个性化的用药科普和推荐',
        '欢迎来到老年肿瘤患者用药科普平台': '欢迎来到老年肿瘤患者用药科普平台',
        '我们致力于为老年肿瘤患者提供个性化的用药科普信息，帮助您更好地了解和管理药物治疗。': '我们致力于为老年肿瘤患者提供个性化的用药科普信息，帮助您更好地了解和管理药物治疗。',
        '获取个性化推荐': '获取个性化推荐',
        '根据您的肿瘤类型、用药情况和身体状况，为您推荐最相关的科普文章和用药建议。': '根据您的肿瘤类型、用药情况和身体状况，为您推荐最相关的科普文章和用药建议。',
        '知识库': '知识库',
        '涵盖各类肿瘤药物的详细信息、副作用管理、药物相互作用等专业知识。': '涵盖各类肿瘤药物的详细信息、副作用管理、药物相互作用等专业知识。',
        '定期更新热门话题、最新研究进展和专家解读，助您全面了解肿瘤治疗。': '定期更新热门话题、最新研究进展和专家解读，助您全面了解肿瘤治疗。',
        '开始探索': '开始探索',
        '精选专题': '精选专题',
        '标签': '标签',
        '返回上一页': '返回上一页',
        '保留所有权利': '保留所有权利',
        '这里汇集了针对老年肿瘤患者常见用药问题、护理、生活方式调整等方面的深度科普文章和指南。': '这里汇集了针对老年肿瘤患者常见用药问题、护理、生活方式调整等方面的深度科普文章和指南。',
        '靶向药物引起的皮肤反应：预防与处理': '靶向药物引起的皮肤反应：预防与处理',
        '针对多种靶向药物可能导致的皮肤干燥、皮疹、瘙痒等问题，提供预防和护理建议。': '针对多种靶向药物可能导致的皮肤干燥、皮疹、瘙痒等问题，提供预防和护理建议。',
        '老年肿瘤患者多重用药管理策略': '老年肿瘤患者多重用药管理策略',
        '探讨老年肿瘤患者常合并多种慢性病，面临多重用药的风险及管理对策，如何避免药物相互作用。': '探讨老年肿瘤患者常合并多种慢性病，面临多重用药的风险及管理对策，如何避免药物相互作用。',
        '靶向治疗': '靶向治疗',
        '皮肤护理': '皮肤护理',
        '副作用': '副作用',
        '多重用药': '多重用药',
        '老年患者': '老年患者',
        '药物相互作用': '药物相互作用',
        '副作用管理': '副作用管理',
        '用药安全': '用药安全',
        '分类': '分类',
        '阅读更多': '阅读更多',
        '请填写您的信息，我们将为您推荐个性化的用药科普内容。': '请填写您的信息，我们将为您推荐个性化的用药科普内容。',
        '例如：肺癌、胃癌': '例如：肺癌、胃癌',
        '年龄段': '年龄段',
        '推荐内容': '推荐内容',
        '暂无推荐，请填写信息后获取。': '暂无推荐，请填写信息后获取。',
        '获取推荐失败，请稍后再试。': '获取推荐失败，请稍后再试。',
        '项目背景与目标': '项目背景与目标',
        '核心技术': '核心技术',
        '数据来源与权威性': '数据来源与权威性',
        '免责声明': '免责声明',
        '重要提示：': '重要提示：',
        '项目负责人：白浩': '项目负责人：白浩',
        '联系电话：023-65079130 (此为申报书中电话，实际部署时可替换)': '联系电话：023-65079130 (此为申报书中电话，实际部署时可替换)',
        '单位：重庆大学附属肿瘤医院 (此为申报书中单位，实际部署时可替换)': '单位：重庆大学附属肿瘤医院 (此为申报书中单位，实际部署时可替换)',
        '二维码1': '二维码1',
        '二维码2': '二维码2',
        '二维码3': '二维码3',
        '本项目旨在运用机器学习技术，搭建一个基于人际连续性的社区老年肿瘤患者用药科普教育新体系。随着我国人口老龄化趋势加剧，老年肿瘤患者数量逐年增多，他们往往面临多病共存、多重用药、生理功能衰退等复杂情况，导致用药风险增高，用药依从性差，严重影响治疗效果和生活质量。': '本项目旨在运用机器学习技术，搭建一个基于人际连续性的社区老年肿瘤患者用药科普教育新体系。随着我国人口老龄化趋势加剧，老年肿瘤患者数量逐年增多，他们往往面临多病共存、多重用药、生理功能衰退等复杂情况，导致用药风险增高，用药依从性差，严重影响治疗效果和生活质量。',
        '传统的用药教育模式往往缺乏针对性和个性化，难以满足老年患者的特殊需求。本平台致力于解决这一痛点，通过整合权威的用药科普知识，结合机器学习算法，为老年肿瘤患者提供个性化的信息筛选和智能推荐服务，帮助他们及其家属更清晰、便捷地获取所需用药知识，提高用药安全性和有效性，最终改善患者的健康结局。': '传统的用药教育模式往往缺乏针对性和个性化，难以满足老年患者的特殊需求。本平台致力于解决这一痛点，通过整合权威的用药科普知识，结合机器学习算法，为老年肿瘤患者提供个性化的信息筛选和智能推荐服务，帮助他们及其家属更清晰、便捷地获取所需用药知识，提高用药安全性和有效性，最终改善患者的健康结局。',
        '平台的核心技术依托于项目申报书中提出的方案，主要包括：': '平台的核心技术依托于项目申报书中提出的方案，主要包括：',
        '知识图谱构建:': '知识图谱构建:',
        '系统化梳理和组织老年肿瘤用药相关的知识，包括药物信息、疾病信息、症状、不良反应、相互作用等，形成结构化的知识网络，为精准检索和智能推荐奠定基础。': '系统化梳理和组织老年肿瘤用药相关的知识，包括药物信息、疾病信息、症状、不良反应、相互作用等，形成结构化的知识网络，为精准检索和智能推荐奠定基础。',
        '分面检索:': '分面检索:',
        '基于知识图谱，提供多维度、层级化的信息筛选方式，帮助用户快速定位到所需的科普内容。': '基于知识图谱，提供多维度、层级化的信息筛选方式，帮助用户快速定位到所需的科普内容。',
        '机器学习与个性化推荐:': '机器学习与个性化推荐:',
        '通过分析用户提供的个人情况（如肿瘤类型、年龄、合并症等）和浏览行为，构建用户画像，利用机器学习算法（如协同过滤、基于内容的推荐等）实现个性化的科普信息推送。': '通过分析用户提供的个人情况（如肿瘤类型、年龄、合并症等）和浏览行为，构建用户画像，利用机器学习算法（如协同过滤、基于内容的推荐等）实现个性化的科普信息推送。',
        '本平台提供的所有科普信息均来源于权威医学指南、专业医学文献、以及临床药学专家的经验总结。我们会尽最大努力确保信息的准确性和时效性。项目团队由重庆大学附属肿瘤医院的药学专家和技术人员组成，致力于提供高质量的科普内容。': '本平台提供的所有科普信息均来源于权威医学指南、专业医学文献、以及临床药学专家的经验总结。我们会尽最大努力确保信息的准确性和时效性。项目团队由重庆大学附属肿瘤医院的药学专家和技术人员组成，致力于提供高质量的科普内容。',
        '本网站提供的所有信息仅用于科普教育目的，不能替代任何专业的医疗诊断、治疗建议或处方。老年肿瘤患者的用药方案复杂且个体差异大，请务必在专业医师 or 药师的指导下进行治疗和用药调整。': '本网站提供的所有信息仅用于科普教育目的，不能替代任何专业的医疗诊断、治疗建议或处方。老年肿瘤患者的用药方案复杂且个体差异大，请务必在专业医师 or 药师的指导下进行治疗和用药调整。',
        '若您在浏览本网站内容后有任何关于自身健康状况 or 治疗方案的疑问，请及时咨询您的主治医生或相关医疗专业人士。对于因依赖本网站信息而采取的任何行动所导致的任何直接或间接损失，本平台不承担任何责任。': '若您在浏览本网站内容后有任何关于自身健康状况 or 治疗方案的疑问，请及时咨询您的主治医生或相关医疗专业人士。对于因依赖本网站信息而采取的任何行动所导致的任何直接或间接损失，本平台不承担任何责任。',
        '如果您对本平台有任何建议或疑问，欢迎通过以下方式联系我们：': '如果您对本平台有任何建议或疑问，欢迎通过以下方式联系我们：',
    },
    'en': {
        '首页': 'Home',
        '用药知识库': 'Drug Knowledge Base',
        '个性化中心': 'Personalization Center',
        '专题区': 'Special Topics',
        '关于我们': 'About Us',
        '联系我们': 'Contact Us',
        '蓬蓬科普': 'Peng Peng Health',
        '老年肿瘤患者用药科普个性化筛选和推荐': 'Personalized Drug Science Popularization and Recommendation for Elderly Cancer Patients',
        '欢迎来到蓬蓬科普': 'Welcome to Peng Peng Health',
        '为老年肿瘤患者提供个性化的用药科普 and 推荐': 'Providing personalized drug science popularization and recommendations for elderly cancer patients',
        '欢迎来到老年肿瘤患者用药科普平台': 'Welcome to the Medication Education Platform for Elderly Cancer Patients',
        '我们致力于为老年肿瘤患者提供个性化的用药科普信息，帮助您更好地了解和管理药物治疗。': 'We are committed to providing personalized medication education for elderly cancer patients, helping you better understand and manage your treatment.',
        '获取个性化推荐': 'Get Personalized Recommendations',
        '根据您的肿瘤类型、用药情况和身体状况，为您推荐最相关的科普文章和用药建议。': 'Recommend the most relevant articles and advice based on your cancer type, medication, and health status.',
        '知识库': 'Knowledge Base',
        '涵盖各类肿瘤药物的详细信息、副作用管理、药物相互作用等专业知识。': 'Covers detailed information on various cancer drugs, side effect management, and drug interactions.',
        '定期更新热门话题、最新研究进展 and 专家解读，助您全面了解肿瘤治疗。': 'Regularly updated with hot topics, latest research, and expert interpretations to help you understand cancer treatment.',
        '开始探索': 'Start Exploring',
        '精选专题': 'Featured Topics',
        '标签': 'Tags',
        '返回上一页': 'Go Back',
        '保留所有权利': 'All Rights Reserved',
        '这里汇集了针对老年肿瘤患者常见用药问题、护理、生活方式调整等方面的深度科普文章 and 指南。': 'Here is a collection of in-depth science popularization articles and guides on common medication issues, nursing, and lifestyle adjustments for elderly cancer patients.',
        '靶向药物引起的皮肤反应：预防与处理': 'Skin Reactions Caused by Targeted Drugs: Prevention and Treatment',
        '针对多种靶向药物可能导致的皮肤干燥、皮疹、瘙痒等问题，提供预防 and 护理建议。': 'Provide prevention and care suggestions for skin dryness, rash, itching and other problems that may be caused by various targeted drugs.',
        '老年肿瘤患者多重用药管理策略': 'Polypharmacy Management Strategies for Elderly Cancer Patients',
        '探讨老年肿瘤患者常合并多种慢性病，面临多重用药的风险及管理对策，如何避免药物相互作用。': 'Discuss the risks and management strategies of polypharmacy in elderly cancer patients who often have multiple chronic diseases, and how to avoid drug interactions.',
        '靶向治疗': 'Targeted Therapy',
        '皮肤护理': 'Skin Care',
        '副作用': 'Side Effects',
        '多重用药': 'Polypharmacy',
        '老年患者': 'Elderly Patients',
        '药物相互作用': 'Drug Interactions',
        '副作用管理': 'Side Effect Management',
        '用药安全': 'Medication Safety',
        '分类': 'Category',
        '阅读更多': 'Read More',
        '请填写您的信息，我们将为您推荐个性化的用药科普内容。': 'Please fill in your information, and we will recommend personalized medication education content for you.',
        '例如：肺癌、胃癌': 'e.g., Lung Cancer, Gastric Cancer',
        '年龄段': 'Age Group',
        '推荐内容': 'Recommended Content',
        '暂无推荐，请填写信息后获取。': 'No recommendations yet, please fill in the information to get them.',
        '获取推荐失败，请稍后再试。': 'Failed to get recommendations, please try again later.',
        '项目背景与目标': 'Project Background and Objectives',
        '核心技术': 'Core Technologies',
        '数据来源与权威性': 'Data Sources and Authority',
        '免责声明': 'Disclaimer',
        '重要提示：': 'Important Note: ',
        '项目负责人：白浩': 'Project Leader: Bai Hao',
        '联系电话：023-65079130 (此为申报书中电话，实际部署时可替换)': 'Contact: 023-65079130 (Phone from proposal, can be replaced)',
        '单位：重庆大学附属肿瘤医院 (此为申报书中单位，实际部署时可替换)': 'Affiliation: Chongqing University Cancer Hospital (Affiliation from proposal, can be replaced)',
        '二维码1': 'QR Code 1',
        '二维码2': 'QR Code 2',
        '二维码3': 'QR Code 3',
        '本项目旨在运用机器学习技术，搭建一个基于人际连续性的社区老年肿瘤患者用药科普教育新体系。随着我国人口老龄化趋势加剧，老年肿瘤患者数量逐年增多，他们往往面临多病共存、多重用药、生理功能衰退等复杂情况，导致用药风险增高，用药依从性差，严重影响治疗效果 and 生活质量。': 'This project aims to use machine learning technology to build a new system for medication education for community elderly cancer patients based on interpersonal continuity. With the intensification of the aging trend in China, the number of elderly cancer patients is increasing year by year. They often face complex situations such as comorbidities, polypharmacy, and decline in physiological functions, leading to increased medication risks and poor compliance, which seriously affects treatment outcomes and quality of life.',
        '传统的用药教育模式往往缺乏针对性和个性化，难以满足老年患者的特殊需求。本平台致力于解决这一痛点，通过整合权威的用药科普知识，结合机器学习算法，为老年肿瘤患者提供个性化的信息筛选 and 智能推荐服务，帮助他们及其家属更清晰、便捷地获取所需用药知识，提高用药安全性和有效性，最终改善患者的健康结局。': 'Traditional medication education models often lack pertinence and personalization, making it difficult to meet the special needs of elderly patients. This platform is dedicated to solving this pain point. By integrating authoritative medication knowledge and combining machine learning algorithms, it provides personalized information screening and intelligent recommendation services for elderly cancer patients, helping them and their families obtain the required medication knowledge more clearly and conveniently, improving medication safety and effectiveness, and ultimately improving patient health outcomes.',
        '平台的核心技术依托于项目申报书中提出的方案，主要包括：': 'The core technology of the platform relies on the plan proposed in the project application, mainly including:',
        '知识图谱构建:': 'Knowledge Graph Construction:',
        '系统化梳理和组织老年肿瘤用药相关的知识，包括药物信息、疾病信息、症状、不良反应、相互作用等，形成结构化的知识网络，为精准检索和智能推荐奠定基础。': 'Systematically organizing knowledge related to elderly cancer medication, including drug information, disease information, symptoms, adverse reactions, interactions, etc., forming a structured knowledge network to lay the foundation for precise retrieval and intelligent recommendation.',
        '分面检索:': 'Faceted Search:',
        '基于知识图谱，提供多维度、层级化的信息筛选方式，帮助用户快速定位到所需的科普内容。': 'Based on the knowledge graph, it provides multi-dimensional and hierarchical information screening methods to help users quickly locate the required science popularization content.',
        '机器学习与个性化推荐:': 'Machine Learning and Personalized Recommendation:',
        '通过分析用户提供的个人情况（如肿瘤类型、年龄、合并症等） and 浏览行为，构建用户画像，利用机器学习算法（如协同过滤、基于内容的推荐等）实现个性化的科普信息推送。': 'By analyzing the personal situation provided by the user (such as cancer type, age, comorbidities, etc.) and browsing behavior, a user profile is constructed, and machine learning algorithms (such as collaborative filtering, content-based recommendation, etc.) are used to achieve personalized science popularization information push.',
        '本平台提供的所有科普信息均来源于权威医学指南、专业医学文献、以及临床药学专家的经验总结。我们会尽最大努力确保信息的准确性和时效性。项目团队由重庆大学附属肿瘤医院的药学专家和技术人员组成，致力于提供高质量的科普内容。': 'All science popularization information provided by this platform comes from authoritative medical guides, professional medical literature, and the experience summary of clinical pharmacy experts. We will do our best to ensure the accuracy and timeliness of the information. The project team consists of pharmacy experts and technical personnel from Chongqing University Cancer Hospital, dedicated to providing high-quality science popularization content.',
        '本网站提供的所有信息仅用于科普教育目的，不能替代任何专业的医疗诊断、治疗建议或处方。老年肿瘤患者的用药方案复杂且个体差异大，请务必在专业医师 or 药师的指导下进行治疗和用药调整。': 'All information provided on this website is for science popularization and education purposes only and cannot replace any professional medical diagnosis, treatment advice, or prescription. The medication regimen for elderly cancer patients is complex and has large individual differences. Please be sure to undergo treatment and medication adjustment under the guidance of a professional physician or pharmacist.',
        '若您在浏览本网站内容后有任何关于自身健康状况 or 治疗方案的疑问，请及时咨询您的主治医生或相关医疗专业人士。对于因依赖本网站信息而采取的任何行动所导致的任何直接或间接损失，本平台不承担任何责任。': 'If you have any questions about your own health status or treatment plan after browsing the content of this website, please consult your attending physician or relevant medical professionals in time. This platform does not assume any responsibility for any direct or indirect losses caused by any actions taken based on the information on this website.',
        '如果您对本平台有任何建议或疑问，欢迎通过以下方式联系我们：': 'If you have any suggestions or questions about this platform, please feel free to contact us through the following ways:',
    }
}

def translate(text):
    lang = session.get('lang', 'zh')
    result = translations.get(lang, translations['zh']).get(text, text)
    return result

@app.context_processor
def inject_translate():
    return dict(_=translate, current_lang=session.get('lang', 'zh'))

@app.route('/set_language/<lang_code>')
def set_language_route(lang_code):
    if lang_code in ['zh', 'en']:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

articles = {
    '1': {
        'title': '靶向药物引起的皮肤反应：预防与处理',
        'category': '副作用管理',
        'tags': ['靶向治疗', '皮肤护理', '副作用'],
        'content': '针对多种靶向药物可能导致的皮肤干燥、皮疹、瘙痒等问题，提供预防和护理建议。'
    },
    '2': {
        'title': '老年肿瘤患者多重用药管理策略',
        'category': '用药安全',
        'tags': ['多重用药', '老年患者', '药物相互作用'],
        'content': '探讨老年肿瘤患者常合并多种慢性病，面临多重用药的风险及管理对策，如何避免药物相互作用。'
    }
}

@app.route('/knowledge_base')
def knowledge_base():
    return render_template('knowledge_base.html', articles=articles)

@app.route('/article/<article_id>')
def article_detail(article_id):
    article = articles.get(article_id)
    if not article:
        return "Article not found", 404
    return render_template('article_detail_template.html', article=article)

@app.route('/personalization')
def personalization():
    return render_template('personalization.html')

@app.route('/special_topics')
def special_topics():
    return render_template('special_topics.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    cancer_type = data.get('cancer_type', '')
    
    # 简单的推荐逻辑
    recommendations = []
    if '肺' in cancer_type or 'lung' in cancer_type.lower():
        recommendations.append(articles['1'])
    
    recommendations.append(articles['2'])
    
    return jsonify(recommendations)

# For Vercel
app.debug = True
