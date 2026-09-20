<script setup>
import { computed, ref } from 'vue'

const query = ref('查询各线路的故障次数，并按故障次数从高到低排序')
const loading = ref(false)
const sql = ref('')
const result = ref([])
const error = ref('')
const elapsed = ref(null)



const columns = computed(() => {
  if (!Array.isArray(result.value) || result.value.length === 0) return []
  return Object.keys(result.value[0])
})

async function ask() {
  const text = query.value.trim()
  if (!text || loading.value) return

  loading.value = true
  error.value = ''
  sql.value = ''
  result.value = []
  elapsed.value = null

  const start = performance.now()

  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: text }),
    })

    let data
    try {
      data = await response.json()
    } catch {
      throw new Error(`后端返回了非 JSON 响应（HTTP ${response.status}）`)
    }

    if (!response.ok) {
      throw new Error(data?.detail || data?.error || `请求失败（HTTP ${response.status}）`)
    }

    sql.value = data.sql || ''
    result.value = Array.isArray(data.result) ? data.result : []
    error.value = data.error || ''
  } catch (e) {
    error.value = e?.message || '请求失败，请检查后端服务是否启动。'
  } finally {
    elapsed.value = Math.round(performance.now() - start)
    loading.value = false
  }
}



function clearAll() {
  query.value = ''
  sql.value = ''
  result.value = []
  error.value = ''
  elapsed.value = null
}

async function copySql() {
  if (!sql.value) return
  await navigator.clipboard.writeText(sql.value)
}

function onKeydown(event) {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    ask()
  }
}
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">RA</div>
        <div>
          <h1>Rail Answer</h1>
          <p>轨道交通智能问数</p>
        </div>
      </div>


      <div class="side-card">
        <div class="status-row">
          <span class="status-dot"></span>
          <span>Text-to-SQL Agent</span>
        </div>
        <p>自然语言 → 元数据召回 → SQL 生成 → 校验 → 查询结果</p>
      </div>
    </aside>

    <main class="main">
      <header class="topbar">
        <div>
          <p class="eyebrow">Railway Data Assistant</p>
          <h2>铁路数据智能查询</h2>
        </div>
        <div class="top-actions">
          <span class="badge">MySQL</span>
          <span class="badge">Qdrant</span>
          <span class="badge">Elasticsearch</span>
        </div>
      </header>

      <section class="query-card">
        <div class="query-head">
          <div>
            <h3>输入你的问题</h3>
            <p>支持车辆、线路、设备、故障、报警和健康度查询。</p>
          </div>
          <button class="text-btn" type="button" @click="clearAll">清空</button>
        </div>

        <textarea
          v-model="query"
          rows="4"
          placeholder="例如：查询各线路的故障次数，并按故障次数从高到低排序"
          @keydown="onKeydown"
        ></textarea>

        <div class="query-footer">
          <span>Ctrl / ⌘ + Enter 快速查询</span>
          <button class="primary-btn" type="button" :disabled="loading || !query.trim()" @click="ask">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? '正在查询...' : '开始查询' }}
          </button>
        </div>
      </section>

      <div v-if="error" class="error-card">
        <strong>查询失败</strong>
        <span>{{ error }}</span>
      </div>

      <section class="content-grid">
        <article class="panel sql-panel">
          <div class="panel-head">
            <div>
              <p class="panel-kicker">Generated SQL</p>
              <h3>生成 SQL</h3>
            </div>
            <button class="ghost-btn" type="button" :disabled="!sql" @click="copySql">复制 SQL</button>
          </div>

          <pre v-if="sql" class="sql-box"><code>{{ sql }}</code></pre>
          <div v-else class="empty-state">
            <div class="empty-icon">SQL</div>
            <p>提交问题后，这里会显示 Agent 生成的 SQL。</p>
          </div>
        </article>

        <article class="panel result-panel">
          <div class="panel-head">
            <div>
              <p class="panel-kicker">Query Result</p>
              <h3>查询结果</h3>
            </div>
            <div class="result-meta">
              <span v-if="elapsed !== null">{{ elapsed }} ms</span>
              <span>{{ result.length }} 行</span>
            </div>
          </div>

          <div v-if="result.length" class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th v-for="column in columns" :key="column">{{ column }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in result" :key="index">
                  <td v-for="column in columns" :key="column">
                    {{ row[column] ?? '—' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="empty-state result-empty">
            <div class="empty-icon">DATA</div>
            <p>查询结果会以表格形式展示在这里。</p>
          </div>
        </article>
      </section>
    </main>
  </div>
</template>
