import os
import cv2
import sqlite3
import numpy as np
import pandas as pd
from deepface import DeepFace
from datetime import datetime

class PersonalAccessSystem:
    def __init__(self, db_name="person_info.db", dataset_dir="dataset"):
        """
        Sistemi başlatır, veritabanı bağlantısını kurar.
        """
        self.db_name = db_name
        self.dataset_dir = dataset_dir
        
        
        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)
            print(f"[INFO] '{self.dataset_dir}' folder created.")

        
        self._setup_database()
        
        
        
        
        self.model_name = "ArcFace" 
        self.detector_backend = "opencv" 

    def _setup_database(self):
        """SQLite veritabanını ve tabloyu oluşturur."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # PERSON TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    student_number TEXT,
                    department TEXT,
                    date_of_birth TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # LOG TABLE
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_name TEXT,
                    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            print("[INFO] Database connection and tables are ready.")
        except Exception as e:
            print(f"[ERROR] An error occurred while creating the database: {e}")

    def add_person_info(self, name, student_number, department, date_of_birth="Unknown"):
        """Veritabanına yeni kişi ekler."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO people (name, student_number, department, date_of_birth)
                VALUES (?, ?, ?, ?)
            ''', (name, student_number, department, date_of_birth))
            
            conn.commit()
            conn.close()
            print(f"[SUCCESS] {name} added/updated to database.")
        except Exception as e:
            print(f"[ERROR] An error occurred while adding the person: {e}")

    def recognize_face(self, img_path):
        """
        Verilen fotoğraftaki kişiyi tanır ve bilgilerini getirir.
        DeepFace.find fonksiyonu veritabanı/klasör taramasını otomatik yapar.
        """
        if not os.path.exists(img_path):
            print(f"[ERROR] Folder not found: {img_path}")
            return None

        print(f"[PROCESS] Face detection in progress: {img_path}...")
        
        try:
            
            
            dfs = DeepFace.find(
                img_path=img_path,
                db_path=self.dataset_dir,
                model_name=self.model_name,
                detector_backend=self.detector_backend, 
                distance_metric="cosine",
                enforce_detection=False, 
                silent=True
            )
            
            if len(dfs) > 0 and not dfs[0].empty:
                
                
                matched_path = dfs[0].iloc[0]["identity"]
                
            
             
                person_name = os.path.basename(os.path.dirname(matched_path))
                
                print(f"[RESULT] Matching Person: {person_name}")
                return self._get_person_details(person_name)
            else:
                print("[RESULT] No match found or face not detected.")
                return None

        except Exception as e:
            print(f"[ERROR] An error occurred while detecting the face: {e}")
            return None

    def _get_person_details(self, name):
        """İsme göre veritabanından bilgileri çeker."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM people WHERE name=?", (name,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
             
                self._log_access(name, "SUCCESS")
                
                return {
                    "ID": result[0],
                    "Name": result[1],
                    "Student Number": result[2],
                    "Department": result[3],
                    "Date of Birth": result[4]
                }
            else:
                self._log_access(name, "INFO_MISSING")
                print(f"[WARNING] {name} The face is recognized but has no information in the database.")
                return {"Name": name, "Error": "No detailed information found"}
                
        except Exception as e:
            print(f"[ERROR] Data extraction error: {e}")
            return None

    def _log_access(self, name, status):
        """Erişim denemesini loglar."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO access_logs (person_name, status) VALUES (?, ?)", (name, status))
            conn.commit()
            conn.close()
        except:
            pass

# --- EXAMPLE USE ---
if __name__ == "__main__":
    system = PersonalAccessSystem()

    # 1. Adding sample data (Run this only once or when adding new information)
    # You can add your own data as follows:
    # system.add_person_info("Name_Surname", "Student_ID", "Department", "Date_of_Birth")
    # Example:
    # system.add_person_info("John_Doe", "12345678", "Computer Science", "2000-01-01")



    
    print("[SYSTEM] Launched...")
    
    
    test_image_path = "ornek_resim.jpeg" # You can write the name of the photo  you want to test here
    
    if os.path.exists(test_image_path):
        info = system.recognize_face(test_image_path)
        if info:
            print("\n--- PERSONAL INFORMATION ---")
            for key, value in info.items():
                print(f"{key}: {value}")
        print("\n" + "=" * 60)
        print("⚠️ LEGAL WARNING")
        print("=" * 60)
        print("All rights related to this service are reserved.")
        print("Any person who uses this service without authorization shall be")
        print("deemed to have accepted full legal responsibility for any")
        print("resulting consequences.\n")

        print("Personal information may not be used for any commercial")
        print("gain or malicious purpose. Any individual who uses such")
        print("information shall be deemed to have accepted full legal")
        print("responsibility for any consequences arising therefrom.")
        print("=" * 60 + "\n")
    else:
        print(f"[WARNING] The file '{test_image_path}' to be tested was not found.")
        print("Please place the photo you want to test into the project folder and update its name in the code.")
