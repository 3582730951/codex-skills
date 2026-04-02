# Python Shop

一个使用 Flask 构建的购物网站 MVP。

## 功能

- 首页商品目录
- 搜索与分类筛选
- 商品详情页
- Session 购物车
- 结账表单
- SQLite 订单持久化

## 运行方式

```bash
cd /workspace/python-shop
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python run.py
```

浏览器访问：

```text
http://127.0.0.1:5000
```

## 说明

- 这是首个可交付版本，没有接入真实支付。
- 订单会保存到 `shop/data/shop.db`。
