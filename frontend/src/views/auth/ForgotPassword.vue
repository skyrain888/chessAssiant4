<template>
  <div class="forgot-password-container">
    <a-card class="forgot-password-card" :bordered="false">
      <template #title>
        <div class="forgot-password-header">
          <h2>忘记密码</h2>
          <p>请输入您的邮箱，我们将发送重置密码链接</p>
        </div>
      </template>
      
      <a-form ref="formRef" :model="form" layout="vertical" @submit="handleSubmit">
        <a-form-item field="email" label="邮箱" :rules="[
          { required: true, message: '请输入邮箱' },
          { type: 'email', message: '请输入有效的邮箱地址' }
        ]">
          <a-input v-model="form.email" placeholder="请输入邮箱" />
        </a-form-item>
        
        <a-form-item>
          <a-button type="primary" html-type="submit" long :loading="loading">发送重置链接</a-button>
        </a-form-item>
        
        <div class="forgot-password-footer">
          <router-link to="/login">返回登录</router-link>
        </div>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Message } from '@arco-design/web-vue'
import http from '@/utils/http'

// 表单数据
const form = reactive({
  email: ''
})

// 表单引用
const formRef = ref(null)

// 状态
const loading = ref(false)

// 提交表单
const handleSubmit = async () => {
  if (formRef.value) {
    try {
      await (formRef.value as any).validate()
      loading.value = true
      
      // 调用忘记密码API
      await http.post('/auth/forgot-password', { email: form.email })
      
      // 显示成功消息
      Message.success('重置密码链接已发送到您的邮箱')
      
      // 清空表单
      form.email = ''
    } catch (err) {
      console.error('表单验证错误:', err)
    } finally {
      loading.value = false
    }
  }
}
</script>

<style scoped>
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.forgot-password-card {
  width: 100%;
  max-width: 420px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.forgot-password-header {
  text-align: center;
  margin-bottom: 24px;
}

.forgot-password-header h2 {
  margin-bottom: 8px;
  font-weight: 600;
  color: #1d2129;
}

.forgot-password-header p {
  color: #86909c;
  margin: 0;
}

.forgot-password-footer {
  margin-top: 16px;
  text-align: center;
}

.forgot-password-footer a {
  color: #165dff;
}
</style> 