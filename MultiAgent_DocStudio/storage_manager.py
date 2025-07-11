import json
import csv
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

class StorageManager:
  
    
    def __init__(self):
        self.json_file = "summaries.json"
        self.csv_file = "summaries.csv"
        self.db_file = "summaries.db"
        self._init_database()
    
    def _init_database(self):
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
          
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_type TEXT,
                    file_size_kb REAL,
                    original_word_count INTEGER,
                    summary TEXT NOT NULL,
                    summary_word_count INTEGER,
                    model_used TEXT,
                    summary_length TEXT,
                    date TEXT NOT NULL,
                    extracted_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
         
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_filename ON summaries(filename)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON summaries(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_model ON summaries(model_used)')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
    
    def save_to_json(self, summary_data: Dict):
        
        try:
            summaries = []
            
            
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    summaries = json.load(f)
            
           
            summaries.append(summary_data)
            
            
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(summaries, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise Exception(f"Error saving to JSON: {str(e)}")
    
    def save_to_csv(self, summary_data: Dict):
       
        try:
            file_exists = os.path.exists(self.csv_file)
            
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'filename', 'file_type', 'file_size_kb', 'original_word_count',
                    'summary', 'summary_word_count', 'model_used', 'summary_length',
                    'date', 'extracted_text'
                ]
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                
                if not file_exists:
                    writer.writeheader()
                
                
                writer.writerow(summary_data)
                
        except Exception as e:
            raise Exception(f"Error saving to CSV: {str(e)}")
    
    def save_to_sqlite(self, summary_data: Dict):
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO summaries (
                    filename, file_type, file_size_kb, original_word_count,
                    summary, summary_word_count, model_used, summary_length,
                    date, extracted_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                summary_data['filename'],
                summary_data['file_type'],
                summary_data['file_size_kb'],
                summary_data['original_word_count'],
                summary_data['summary'],
                summary_data['summary_word_count'],
                summary_data['model_used'],
                summary_data['summary_length'],
                summary_data['date'],
                summary_data['extracted_text']
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            raise Exception(f"Error saving to SQLite: {str(e)}")
    
    def get_all_summaries(self, storage_type: str = "sqlite") -> List[Dict]:
        
        try:
            if storage_type.lower() == "json":
                return self._get_from_json()
            elif storage_type.lower() == "csv":
                return self._get_from_csv()
            else:  # sqlite
                return self._get_from_sqlite()
                
        except Exception as e:
            raise Exception(f"Error retrieving summaries: {str(e)}")
    
    def _get_from_json(self) -> List[Dict]:
        
        if not os.path.exists(self.json_file):
            return []
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_from_csv(self) -> List[Dict]:
        
        if not os.path.exists(self.csv_file):
            return []
        
        summaries = []
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                summaries.append(row)
        
        return summaries
    
    def _get_from_sqlite(self) -> List[Dict]:
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT filename, file_type, file_size_kb, original_word_count,
                   summary, summary_word_count, model_used, summary_length,
                   date, extracted_text
            FROM summaries
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        summaries = []
        for row in rows:
            summaries.append({
                'filename': row[0],
                'file_type': row[1],
                'file_size_kb': row[2],
                'original_word_count': row[3],
                'summary': row[4],
                'summary_word_count': row[5],
                'model_used': row[6],
                'summary_length': row[7],
                'date': row[8],
                'extracted_text': row[9]
            })
        
        return summaries
    
    def get_statistics(self) -> Optional[Dict]:
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
           
            cursor.execute('SELECT COUNT(*) FROM summaries')
            total_documents = cursor.fetchone()[0]
            
            if total_documents == 0:
                conn.close()
                return None
            
            
            cursor.execute('SELECT SUM(original_word_count) FROM summaries')
            total_words = cursor.fetchone()[0] or 0
            
           
            cursor.execute('SELECT AVG(summary_word_count) FROM summaries')
            avg_summary_length = cursor.fetchone()[0] or 0
            
            
            cursor.execute('''
                SELECT model_used, COUNT(*) 
                FROM summaries 
                GROUP BY model_used
            ''')
            model_usage = dict(cursor.fetchall())
            
            
            cursor.execute('''
                SELECT file_type, COUNT(*) 
                FROM summaries 
                GROUP BY file_type
            ''')
            file_type_distribution = dict(cursor.fetchall())
            
            
            cursor.execute('''
                SELECT COUNT(*) 
                FROM summaries 
                WHERE date(created_at) = date('now')
            ''')
            today_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_documents': total_documents,
                'total_words': total_words,
                'avg_summary_length': avg_summary_length,
                'model_usage': model_usage,
                'file_type_distribution': file_type_distribution,
                'today_count': today_count
            }
            
        except Exception as e:
            print(f"Error getting statistics: {str(e)}")
            return None
    
    def search_summaries(self, query: str, storage_type: str = "sqlite") -> List[Dict]:
        
        try:
            if storage_type.lower() == "sqlite":
                return self._search_sqlite(query)
            else:
                
                all_summaries = self.get_all_summaries(storage_type)
                return self._filter_summaries(all_summaries, query)
                
        except Exception as e:
            raise Exception(f"Error searching summaries: {str(e)}")
    
    def _search_sqlite(self, query: str) -> List[Dict]:
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT filename, file_type, file_size_kb, original_word_count,
                   summary, summary_word_count, model_used, summary_length,
                   date, extracted_text
            FROM summaries
            WHERE filename LIKE ? OR summary LIKE ? OR extracted_text LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        summaries = []
        for row in rows:
            summaries.append({
                'filename': row[0],
                'file_type': row[1],
                'file_size_kb': row[2],
                'original_word_count': row[3],
                'summary': row[4],
                'summary_word_count': row[5],
                'model_used': row[6],
                'summary_length': row[7],
                'date': row[8],
                'extracted_text': row[9]
            })
        
        return summaries
    
    def _filter_summaries(self, summaries: List[Dict], query: str) -> List[Dict]:
       
        query_lower = query.lower()
        filtered = []
        
        for summary in summaries:
            if (query_lower in summary['filename'].lower() or
                query_lower in summary['summary'].lower() or
                query_lower in summary.get('extracted_text', '').lower()):
                filtered.append(summary)
        
        return filtered
    
    def delete_summary(self, filename: str, storage_type: str = "sqlite"):
        
        try:
            if storage_type.lower() == "sqlite":
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM summaries WHERE filename = ?', (filename,))
                conn.commit()
                conn.close()
            else:
               
                raise Exception("Delete operation not implemented for JSON/CSV storage")
                
        except Exception as e:
            raise Exception(f"Error deleting summary: {str(e)}")
    
    def export_summaries(self, format: str = "json", filename: str = None):
        
        try:
            summaries = self.get_all_summaries("sqlite")
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"summaries_export_{timestamp}.{format}"
            
            if format.lower() == "json":
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(summaries, f, indent=2, ensure_ascii=False)
            elif format.lower() == "csv":
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = [
                        'filename', 'file_type', 'file_size_kb', 'original_word_count',
                        'summary', 'summary_word_count', 'model_used', 'summary_length',
                        'date', 'extracted_text'
                    ]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(summaries)
            else:
                raise Exception(f"Unsupported export format: {format}")
            
            return filename
            
        except Exception as e:
            raise Exception(f"Error exporting summaries: {str(e)}") 