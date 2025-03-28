# cinex-backend

### Development Setup

1. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **After installing a new Dependecy**:
   - Run the following command to add your newly installed dependencies:
     ```bash
     pip3 freeze > requirements.txt
     ```

4. **Run the Application**:
   - Use either of the following commands:
     ```bash
     python app.py
     ```
     **OR**
     ```bash
     python3 app.py  
     ```
   - The app will be available at `http://127.0.0.1:5000/`.

---