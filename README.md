# aiudate

> AIUDATE 是一个对正常中文描述日期区间的解读，返回 (datetime.date(), datetime.date()) 格式输出

```python
from aiudate.drange import get_date_range

get_date_range("给我一下昨天的数据")
get_date_range("去年3月1日到现在的数据")
get_date_range("上周一到本周三的数据")
```

### 安装方法

1. 直接使用pip3安装
```bash
pip3 install aiudate
```
2. 指明地址
```bash
pip3 install -i https://pypi.org/simple/simple aiudate
```
3. 直接下载，本地安装
代码即为短小，基本没什么依赖
