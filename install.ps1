python -m venv doctalk_venv
Invoke-Expression -Command .\doctalk_venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip cache purge
pip --no-cache-dir install -r requirements.txt