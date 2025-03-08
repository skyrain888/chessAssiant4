<template>
  <div class="login-container">
    <a-card class="login-card" :bordered="false">
      <template #title>
        <div class="login-header">
          <h2>登录账号</h2>
          <p>欢迎回到家长助手，请登录您的账号</p>
        </div>
      </template>
      
      <a-form ref="formRef" :model="form" layout="vertical" @submit="handleSubmit">
        <a-form-item field="email" label="邮箱" :rules="[
          { required: true, message: '请输入邮箱' },
          { type: 'email', message: '请输入有效的邮箱地址' }
        ]">
          <a-input v-model="form.email" placeholder="请输入邮箱" />
        </a-form-item>
        
        <a-form-item field="password" label="密码" :rules="[
          { required: true, message: '请输入密码' }
        ]">
          <a-input-password v-model="form.password" placeholder="请输入密码" />
        </a-form-item>
        
        <div class="login-options">
          <a-checkbox v-model="form.remember">记住我</a-checkbox>
          <router-link to="/forgot-password" class="forgot-password">忘记密码？</router-link>
        </div>
        
        <a-form-item>
          <a-button type="primary" html-type="submit" long :loading="loading">登录</a-button>
        </a-form-item>
        
        <div class="login-footer">
          <span>还没有账号？</span>
          <router-link to="/register">立即注册</router-link>
        </div>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Message } from '@arco-design/web-vue'

// 表单数据
const form = reactive({
  email: '',
  password: '',
  remember: false
})

// 表单引用
const formRef = ref(null)

// 状态
const loading = ref(false)
const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 提交表单
const handleSubmit = async () => {
  if (formRef.value) {
    try {
      await (formRef.value as any).validate()
      loading.value = true
      
      // 调用登录API
      const success = await userStore.login(form.email, form.password)
      
      if (success) {
        // 登录成功，跳转到首页或重定向页面
        const redirectPath = route.query.redirect as string || '/'
        router.push(redirectPath)
      }
    } catch (err) {
      console.error('表单验证错误:', err)
    } finally {
      loading.value = false
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 100%;
  max-width: 420px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.login-header {
  text-align: center;
  margin-bottom: 24px;
}

.login-header h2 {
  margin-bottom: 8px;
  font-weight: 600;
  color: #1d2129;
}

.login-header p {
  color: #86909c;
  margin: 0;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.forgot-password {
  color: #165dff;
  font-size: 14px;
}

.login-footer {
  margin-top: 16px;
  text-align: center;
  color: #86909c;
}

.login-footer a {
  color: #165dff;
  margin-left: 8px;
}
</style> 