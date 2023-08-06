

## 使用说明
https://hcrobots.feishu.cn/docx/doxcnCw5mIUCbo1CGDgt8j026Je

## generate or update requirements.txt
```
pip install pipreqs
pipreqs . --force
```


## 示例脚本

sort 电压电流图
```
python3 main.py chart --prd_type=sort --time_range=1 --robot_id=G27A25S --log_root_dir=/Users/shixukai/Repositories/log-analysis/test/test_data/sort --timestamp="2022-08-24 15:56:00"
```

pick 电压电流图

```
python3 main.py chart --prd_type=pick --time_range=1 --robot_id=474E50 --log_root_dir=/Users/shixukai/Repositories/log-analysis/test/test_data/pick --timestamp="2022-09-03 14:23:59" --plot_show
```

```
python3 main.py chart --prd_type=pick --time_range=1 --robot_id=474E50 --log_root_dir=/Users/shixukai/Repositories/log-analysis/test/test_data/pick --timestamp="2022-09-03 14:23:59" --plot_show
```

日志打包

```
python3 main.py pack --time_range=1 --log_root_dir=/Users/shixukai/Repositories/log-analysis/test/test_data/pick --timestamp="2022-09-03 14:23:59"
```

pyinstaller 打包命令

```
pyinstaller -F -n hc-log-tool --path . main.py
```

### build for and upload pypi
```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

python3 -m build
python3 -m twine upload dist/hc_log_tools-1.* --skip-existing
```
