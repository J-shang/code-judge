
import concurrent.futures
import time
import requests
from tqdm import tqdm

def worker(batch_data):
    submissions = [
        {
            "type": "lean",
            "solution": proof,
        }
        for proof in batch_data
    ]
    data = {
        'type': 'batch',
        "submissions": submissions
    }
    response = requests.post("http://0.0.0.0:8088/run/long-batch", json=data)
    result = response.json()
    return result

# --- 主程序 ---
if __name__ == "__main__":
    print("主程序：开始。")

    from datasets import load_dataset
    dataset = load_dataset("Goedel-LM/Lean-workbook-proofs", split="train"+ f"[:1000]")
    data_list = [dataset[i:i+8]['full_proof'] for i in range(0, 1000, 8)]
    
    # 定义 work 数量
    num_workers = 10
    start_time = time.time()

    # 使用 with 语句可以确保线程池在使用完毕后被正确关闭
    # max_workers=10 指定了线程池中最多同时运行10个线程
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        print(f"主程序：向线程池提交 {1000 / 8} 个任务。")
        futures = [executor.submit(worker, batch_data) for batch_data in data_list]
        print("主程序：所有任务均已提交。")
        results = []
        # as_completed 方法会在每个任务完成时返回对应的 future 对象
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            try:
                # 调用 future.result() 可以获取任务的返回值
                # 如果任务执行过程中发生异常，这里会重新抛出该异常
                results.append(future.result())
            except Exception as exc:
                print(f"主程序：一个任务在执行时产生了异常: {exc}")

    # with 语句块结束时，程序会自动等待线程池中的所有任务都执行完毕
    # 所以这里不需要手动调用 join()
    print("\n主程序：所有任务均已执行完毕。程序结束。用时：", time.time() - start_time, "秒")

    import json
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
