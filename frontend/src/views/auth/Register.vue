<template>
  <div class="register-container">
    <a-card class="register-card" :bordered="false">
      <template #title>
        <div class="register-header">
          <h2>注册账号</h2>
          <p>欢迎加入家长助手，请填写以下信息完成注册</p>
        </div>
      </template>
      
      <a-form ref="formRef" :model="form" layout="vertical" @submit="handleSubmit">
        <a-form-item field="username" label="用户名" :rules="[{ required: true, message: '请输入用户名' }]">
          <a-input v-model="form.username" placeholder="请输入用户名" />
        </a-form-item>
        
        <a-form-item field="email" label="邮箱" :rules="[
          { required: true, message: '请输入邮箱' },
          { type: 'email', message: '请输入有效的邮箱地址' }
        ]">
          <a-input v-model="form.email" placeholder="请输入邮箱" />
        </a-form-item>
        
        <a-form-item field="password" label="密码" :rules="[
          { required: true, message: '请输入密码' },
          { minLength: 6, message: '密码长度不能少于6个字符' }
        ]">
          <a-input-password v-model="form.password" placeholder="请输入密码" />
        </a-form-item>
        
        <a-form-item field="confirmPassword" label="确认密码" :rules="[
          { required: true, message: '请确认密码' },
          { validator: validateConfirmPassword, message: '两次输入的密码不一致' }
        ]">
          <a-input-password v-model="form.confirmPassword" placeholder="请确认密码" />
        </a-form-item>
        
        <a-form-item>
          <a-button type="primary" html-type="submit" long :loading="loading">注册</a-button>
        </a-form-item>
        
        <div class="register-footer">
          <span>已有账号？</span>
          <router-link to="/login">立即登录</router-link>
        </div>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Message } from '@arco-design/web-vue'

// 表单数据
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 表单引用
const formRef = ref(null)

// 状态
const loading = ref(false)
const router = useRouter()
const userStore = useUserStore()

// 验证确认密码
const validateConfirmPassword = (value: string) => {
  return value === form.password
}

// 提交表单
const handleSubmit = async () => {
  if (formRef.value) {
    try {
      await (formRef.value as any).validate()
      loading.value = true
      
      // 调用注册API
      const success = await userStore.register({
        username: form.username,
        email: form.email,
        password: form.password
      })
      
      if (success) {
        // 注册成功，跳转到首页
        router.push('/')
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
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.register-card {
  width: 100%;
  max-width: 420px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.register-header {
  text-align: center;
  margin-bottom: 24px;
}

.register-header h2 {
  margin-bottom: 8px;
  font-weight: 600;
  color: #1d2129;
}

.register-header p {
  color: #86909c;
  margin: 0;
}

.register-footer {
  margin-top: 16px;
  text-align: center;
  color: #86909c;
}

.register-footer a {
  color: rgb(var(--primary-6));
  margin-left: 8px;
}
</style> 