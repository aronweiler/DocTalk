python -m venv doctalk_venv
Invoke-Expression -Command .\doctalk_venv\Scripts\activate
python.exe -m pip install --upgrade pip
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"      
$env:FORCE_CMAKE=1
$env:LLAMA_CUBLAS=1 
pip cache purge
pip --no-cache-dir install -r requirements.txt