from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

def run_script(script_name):
    print(f"Running {script_name}...")
    try:
        result = subprocess.run(["python", script_name], check=True, capture_output=True, text=True)
        print(f"{script_name} completed successfully.")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(f"Exit code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False, e.stderr

@app.route('/run-job', methods=['GET'])
def job():
    results = {}
    success, output = run_script("scrape_tw_data.py")
    results['scrape_tw_data'] = {'success': success, 'output': output}
    
    if success:
        success, output = run_script("extract_newdata.py")
        results['extract_newdata'] = {'success': success, 'output': output}
    else:
        results['extract_newdata'] = {'success': False, 'output': "Skipped due to error in scrape_tw_data.py"}
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)