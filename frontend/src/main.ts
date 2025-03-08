import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'

// 创建Vue应用实例
const app = createApp(App)

// 使用Pinia状态管理
app.use(createPinia())

// 使用Vue Router
app.use(router)

// 使用Arco Design组件库
app.use(ArcoVue as any)

// 挂载应用
app.mount('#app')

// 调试信息
console.log('环境变量:', import.meta.env)
console.log('API基础URL:', import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api') 