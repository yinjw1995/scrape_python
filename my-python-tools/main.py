import schedule
import time
import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    try:
        result = subprocess.run(["python", script_name], check=True, capture_output=True, text=True)
        print(f"{script_name} completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(f"Exit code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False

def job():
    # 运行 scrape_tw_data.py 脚本
    if run_script("scrape_tw_data.py"):
        # 只有在 scrape_tw_data.py 成功运行后才运行 extract_newdata.py
        run_script("extract_newdata.py")
    else:
        print("Skipping extract_newdata.py due to error in scrape_tw_data.py")

# 设置每15分钟运行一次任务
schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    print("Once first.")
    job()  # 立即运行一次任务
    
    print("Starting the scheduler. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(1)