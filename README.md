<h1 align="center">ranDC- Ransomware Detection using ML and GMMHMM</h1>
<p align="center">
  <a href="#features">Features</a> |
  <a href="#installation">Installation</a> |
  <a href="#usage">Usage</a> 
  <a href="#paper">Research Paper</a>
</p>

# Research Paper
<a href="https://ieeexplore.ieee.org/document/10225001">IEEE CSR 2023, Italy</a>

# Features

- ranDC framework is trained on Machine Learning (ML) and Hidden Markov Model with Gaussian Emmission (GMMHMM).
- Network traffic dumps can be tested to check if it contains Ransomware/Malware traffic.
- Decision Tree Classifer predictions are validated using GMMHMM.
- Final state classifcation is done based on the <i>classification_percentage</i>.
- For more details, read the paper <a href="https://ieeexplore.ieee.org/document/10225001">Link</a>.

# Installation
- First clone the repository or download the zip file: <br>
<code> git clone https://github.com/amanonearth/ranDC.git </code><br>
- Navigate to the directory<br>
<code> cd ranDC </code><br>
- Create a virtual enviroment<br>
<code> python -m venv venv </code> <br>
- Activate virtual enviroment<br>
  - For windows:
  <code> .\venv\Scripts\activate </code> <br>
  - For Unix*:
  <code> source venv/bin/activate </code> <br>
- Install the requirements <br>
<code> pip install -r REQUIREMENTS.txt </code> <br>
- Run the run.py file: <br>
<code> python app.py </code>

# Usage
- Once the flask server is up and running<br>
- Upload a pcap file from the home page<br>
<img src="images/upload.png" alt="upload-image"></a>
- Get the result.<br>
<img src="images/result.png" alt="result-image"></a>
