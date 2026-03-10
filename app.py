from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from models import db, School, SearchResult, Collection
from search import search_school, batch_search
from export import export_to_excel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///psychology_admission.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

# Initialize CORS
CORS(app)

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    # Initialize schools if not exists
    from data import initialize_schools
    initialize_schools()

@app.route('/api/schools', methods=['GET'])
def get_schools():
    """Get all schools"""
    schools = School.query.all()
    return jsonify([school.to_dict() for school in schools])

@app.route('/api/search', methods=['POST'])
def search():
    """Search for admission information"""
    data = request.json
    school_ids = data.get('school_ids', [])
    
    if not school_ids:
        # Search all schools
        schools = School.query.all()
        school_ids = [school.id for school in schools]
    
    # Start batch search
    batch_search(school_ids)
    
    return jsonify({'message': 'Search started', 'school_ids': school_ids})

@app.route('/api/search-results', methods=['GET'])
def get_search_results():
    """Get search results"""
    results = SearchResult.query.all()
    return jsonify([result.to_dict() for result in results])

@app.route('/api/collection', methods=['POST'])
def manage_collection():
    """Manage school collection"""
    data = request.json
    school_id = data.get('school_id')
    action = data.get('action')  # 'add' or 'remove'
    
    if not school_id or not action:
        return jsonify({'error': 'Missing school_id or action'}), 400
    
    if action == 'add':
        # Add to collection
        collection = Collection(school_id=school_id)
        db.session.add(collection)
    elif action == 'remove':
        # Remove from collection
        collection = Collection.query.filter_by(school_id=school_id).first()
        if collection:
            db.session.delete(collection)
    
    db.session.commit()
    
    # Get updated collection
    collections = Collection.query.all()
    collected_school_ids = [c.school_id for c in collections]
    
    return jsonify({'collected_school_ids': collected_school_ids})

@app.route('/api/export', methods=['GET'])
def export():
    """Export search results to Excel"""
    try:
        file_path = export_to_excel()
        return send_file(file_path, as_attachment=True, download_name='psychology_admission_results.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)