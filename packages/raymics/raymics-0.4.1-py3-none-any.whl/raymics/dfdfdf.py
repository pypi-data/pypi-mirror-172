import tqdm
import os
import redis



def tqdm_callback(bar: tqdm.tqdm):
    bar.update()
    task_id = os.environ.get("TASK_ID")
    n = bar.format_dict.get("n", 0)
    total = bar.format_dict.get("total", 0)

    value = {
        "n": n,
        "total": total
    }
    print("value = ", value)
