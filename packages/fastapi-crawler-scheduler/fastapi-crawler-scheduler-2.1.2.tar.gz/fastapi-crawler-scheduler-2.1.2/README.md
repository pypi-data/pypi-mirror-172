*********

# fastapi_crawler_scheduler

*********

## 使用

*********

```python
from fastapi import FastAPI
from fastapi_crawler_scheduler import TaskScheduler

app = FastAPI()

task_scheduler = TaskScheduler(
    app=app,
    ssl=False,
    project_name="project_name",
    server_name="server_name",
    redis_username='redis_username',
    redis_password='redis_password',
    redis_host="127.0.0.1",
    redis_port=6379,
    thread_pool_size=50,
)
```

### 添加|更新任务 - add_task

#### interval类型

```python
def add_spider(**crawler_info):
    print(f"add_spider = {crawler_info}")
    print("add_spider")


trigger = 'interval'
crawler_info = {
    "topic": "interval insert_task",
    "title_handler_name": "interval insert_task",
    "seconds": 4,
}
job_id = 'job_1'
task_scheduler.add_task(
    func=add_spider,
    job_id=job_id,
    trigger=trigger,
    crawler_info=crawler_info,
    seconds=4
)
```

#### date类型

```python
def add_spider(**crawler_info):
    print(f"add_spider = {crawler_info}")
    print("add_spider")


trigger = 'date'
crawler_info = {
    "topic": "date insert_task",
    "title_handler_name": "date insert_task",
    "run_date": "2022-10-03 11:30:00",
}
job_id = 'job_1'
run_date = '2022-10-03 11:30:00'
task_scheduler.add_task(
    func=add_spider,
    job_id=job_id,
    trigger=trigger,
    crawler_info=crawler_info,
    run_date=run_date,
)
```

#### cron类型

```python
def add_spider(**crawler_info):
    print(f"add_spider = {crawler_info}")
    print("add_spider")


job_id = 'job_1'
trigger = 'cron'
minute = '*/2'
crawler_info = {
    "topic": "cron update_task",
    "title_handler_name": "cron update_task",
    "minute": minute,
}
task_scheduler.add_task(
    func=add_spider,
    job_id=job_id,
    trigger=trigger,
    crawler_info=crawler_info,
    minute=minute,
)
```

### 删除任务 - delete_task

```python
job_id = 'job_1'
task_scheduler.delete_task(job_id=job_id)
```

### 查看任务

```python
# 查看该项目的所有键
task_scheduler.show_all_redis_key()
# 查看该项目的所进程
task_scheduler.show_all_redis_nodes()
# 查看该项目的所有加载过的任务
task_scheduler.show_all_redis_tasks()
# 查看该项目使用的apscheduler.get_jobs()方法获得的所有任务
task_scheduler.show_all_scheduler_get_jobs()
# 查看该项目的apscheduler存储redis的所有任务
task_scheduler.show_all_apscheduler_stores_jobs()
# 查看该项目的的apscheduler存储redis的所有任务的run_ttimes
task_scheduler.show_all_redis_apscheduler_run_times()
# 查看该项目的所有任务不存在apscheduler存储redis的所有任务
task_scheduler.show_all_task_not_in_stores_jobs()
# 查看该项目的任务没有执行的项目（不包含只执行过一次的项目）
task_scheduler.show_all_task_not_in_stores_run_times()
task_scheduler.clear_project_keys()
```
### 请求redis 脏数据   慎用
```python
task_scheduler.clear_project_keys()
```


安装
============
Pypi
----

    $ pip install fastapi-crawler-scheduler

