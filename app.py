from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from models import db, School, SearchResult, Collection, Group, GroupMember
from search import search_school, batch_search
from export import export_to_csv
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///psychology_admission.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()
    from data import initialize_schools
    initialize_schools()

@app.route('/api/schools', methods=['GET'])
def get_schools():
    schools = School.query.all()
    return jsonify({'schools': [school.to_dict() for school in schools]})

@app.route('/api/search', methods=['POST'])
def search_single():
    data = request.json
    school_id = data.get('school_id')
    if not school_id:
        return jsonify({'error': 'Missing school_id'}), 400
    
    school = School.query.get(school_id)
    if not school:
        return jsonify({'error': 'School not found'}), 404
    
    result = search_school(school)
    
    search_result = SearchResult.query.filter_by(school_id=school_id).first()
    if search_result:
        search_result.found = result.get('found', False)
        search_result.title = result.get('title', '')
        search_result.date = result.get('date', '')
        search_result.url = result.get('url', '')
        search_result.error = result.get('error', False)
        search_result.error_message = result.get('error_message', '')
    else:
        search_result = SearchResult(
            school_id=school_id,
            found=result.get('found', False),
            title=result.get('title', ''),
            date=result.get('date', ''),
            url=result.get('url', ''),
            error=result.get('error', False),
            error_message=result.get('error_message', '')
        )
        db.session.add(search_result)
    
    db.session.commit()
    
    return jsonify({
        'found': result.get('found', False),
        'title': result.get('title', ''),
        'date': result.get('date', ''),
        'url': result.get('url', ''),
        'error': result.get('error', False),
        'error_message': result.get('error_message', '')
    })

@app.route('/api/search/batch', methods=['POST'])
def search_batch():
    data = request.json
    school_ids = data.get('school_ids', [])
    
    if not school_ids:
        schools = School.query.all()
        school_ids = [school.id for school in schools]
    
    school_data_list = []
    for sid in school_ids:
        school = School.query.get(sid)
        if school:
            school_data_list.append({
                'id': school.id,
                'name': school.name,
                'links': {
                    'main': school.main_link,
                    'grad': school.grad_link,
                    'dept': school.dept_link,
                    'recruit': school.recruit_link
                }
            })
    
    results = batch_search(school_data_list)
    
    response_results = []
    for result in results:
        search_result = SearchResult.query.filter_by(school_id=result['school_id']).first()
        if search_result:
            search_result.found = result.get('found', False)
            search_result.title = result.get('title', '')
            search_result.date = result.get('date', '')
            search_result.url = result.get('url', '')
            search_result.error = result.get('error', False)
            search_result.error_message = result.get('error_message', '')
        else:
            search_result = SearchResult(
                school_id=result['school_id'],
                found=result.get('found', False),
                title=result.get('title', ''),
                date=result.get('date', ''),
                url=result.get('url', ''),
                error=result.get('error', False),
                error_message=result.get('error_message', '')
            )
            db.session.add(search_result)
        
        response_results.append({
            'school_id': result['school_id'],
            'found': result.get('found', False),
            'title': result.get('title', ''),
            'date': result.get('date', ''),
            'url': result.get('url', ''),
            'error': result.get('error', False),
            'error_message': result.get('error_message', '')
        })
    
    db.session.commit()
    
    return jsonify({'results': response_results})

@app.route('/api/search/results', methods=['GET'])
def get_search_results():
    results = SearchResult.query.all()
    return jsonify({'results': [result.to_dict() for result in results]})

@app.route('/api/collections', methods=['GET'])
def get_collections():
    collections = Collection.query.all()
    return jsonify({'collections': [c.to_dict() for c in collections]})

@app.route('/api/collections', methods=['POST'])
def add_collection():
    data = request.json
    school_id = data.get('school_id')
    if not school_id:
        return jsonify({'error': 'Missing school_id'}), 400
    
    existing = Collection.query.filter_by(school_id=school_id).first()
    if not existing:
        collection = Collection(school_id=school_id)
        db.session.add(collection)
        db.session.commit()
    
    collections = Collection.query.all()
    return jsonify({'collections': [c.to_dict() for c in collections]})

@app.route('/api/collections', methods=['DELETE'])
def remove_collection():
    data = request.json
    school_id = data.get('school_id')
    if not school_id:
        return jsonify({'error': 'Missing school_id'}), 400
    
    collection = Collection.query.filter_by(school_id=school_id).first()
    if collection:
        db.session.delete(collection)
        db.session.commit()
    
    collections = Collection.query.all()
    return jsonify({'collections': [c.to_dict() for c in collections]})

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    try:
        file_path = export_to_csv()
        return send_file(file_path, as_attachment=True, download_name='psychology_admission_results.csv', mimetype='text/csv')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    groups_with_members = []
    for group in groups:
        group_dict = group.to_dict()
        group_dict['members'] = [m.to_dict() for m in group.members]
        groups_with_members.append(group_dict)
    return jsonify({'groups': groups_with_members})

@app.route('/api/groups', methods=['POST'])
def create_group():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Missing name'}), 400
    
    group = Group(name=name)
    db.session.add(group)
    db.session.commit()
    
    return jsonify(group.to_dict())

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    
    db.session.delete(group)
    db.session.commit()
    
    return jsonify({'message': 'Group deleted'})

@app.route('/api/groups/<int:group_id>/members', methods=['POST'])
def add_group_member(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    
    data = request.json
    school_id = data.get('school_id')
    if not school_id:
        return jsonify({'error': 'Missing school_id'}), 400
    
    school = School.query.get(school_id)
    if not school:
        return jsonify({'error': 'School not found'}), 404
    
    existing = GroupMember.query.filter_by(group_id=group_id, school_id=school_id).first()
    if existing:
        return jsonify({'error': 'Already in group'}), 400
    
    member = GroupMember(group_id=group_id, school_id=school_id)
    db.session.add(member)
    db.session.commit()
    
    return jsonify(member.to_dict())

@app.route('/api/groups/<int:group_id>/members/<int:school_id>', methods=['DELETE'])
def remove_group_member(group_id, school_id):
    member = GroupMember.query.filter_by(group_id=group_id, school_id=school_id).first()
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    db.session.delete(member)
    db.session.commit()
    
    return jsonify({'message': 'Member removed'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
