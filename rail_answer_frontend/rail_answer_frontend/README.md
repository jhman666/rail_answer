# Rail Answer Frontend

Vue 3 + Vite 前端，用于铁路 Text-to-SQL Agent。

## 启动

```bash
npm install
npm run dev
```

默认访问：`http://localhost:5173`

## 后端接口约定

前端会请求：

```http
POST /api/query
Content-Type: application/json
```

请求体：

```json
{
  "query": "查询1号线有多少辆车"
}
```

期望响应：

```json
{
  "query": "查询1号线有多少辆车",
  "sql": "SELECT ...",
  "result": [
    {"车辆数量": 16}
  ],
  "error": ""
}
```

Vite 已配置代理，将 `/api` 转发到 `http://127.0.0.1:8000`。
如果你的 FastAPI 地址不同，请修改 `vite.config.js` 中的 `target`。
