<template>
  <div class="forgot-password-container">
    <div class="forgot-password-content">
      <div class="forgot-password-logo">
        <h1 class="app-title">家长助手</h1>
        <p class="app-subtitle">面向学生家长的工具集合平台</p>
      </div>
      
      <a-card class="forgot-password-card" :bordered="false">
        <div class="forgot-password-header">
          <div class="header-title">忘记密码</div>
          <div class="header-divider"></div>
          <p class="header-subtitle">请输入您的邮箱，我们将发送重置密码链接</p>
        </div>
        
        <a-form ref="formRef" :model="form" layout="vertical" @submit="handleSubmit">
          <a-form-item field="email" label="邮箱" :rules="[
            { required: true, message: '请输入邮箱' },
            { type: 'email', message: '请输入有效的邮箱地址' }
          ]">
            <a-input v-model="form.email" placeholder="请输入邮箱" allow-clear>
              <template #prefix>
                <icon-email />
              </template>
            </a-input>
          </a-form-item>
          
          <a-form-item>
            <a-button type="primary" html-type="submit" long :loading="loading" class="submit-button">
              发送重置链接
            </a-button>
          </a-form-item>
          
          <div class="forgot-password-footer">
            <router-link to="/login" class="back-link">
              <icon-left />返回登录
            </router-link>
          </div>
        </a-form>
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Message } from '@arco-design/web-vue'
import { IconEmail, IconLeft } from '@arco-design/web-vue/es/icon'
import { post } from '@/utils/http'

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
      await post('/auth/forgot-password', { email: form.email })
      
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
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
  padding: 20px;
}

.forgot-password-content {
  width: 100%;
  max-width: 420px;
}

.forgot-password-logo {
  text-align: center;
  margin-bottom: 24px;
}

.app-title {
  font-size: 32px;
  font-weight: 600;
  color: #165dff;
  margin: 0 0 8px;
}

.app-subtitle {
  font-size: 16px;
  color: #4e5969;
  margin: 0;
}

.forgot-password-card {
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  background-color: #fff;
  padding-top: 16px;
}

.forgot-password-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 0 24px;
}

.header-title {
  font-size: 22px;
  font-weight: 600;
  color: #1d2129;
  margin-bottom: 16px;
}

.header-divider {
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #165dff, #4080ff);
  margin: 0 auto 16px;
  border-radius: 2px;
}

.header-subtitle {
  color: #86909c;
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
}

.submit-button {
  height: 40px;
  font-size: 16px;
  margin-top: 8px;
  transition: all 0.3s;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 93, 255, 0.4);
}

.forgot-password-footer {
  margin-top: 24px;
  text-align: center;
}

.back-link {
  display: inline-flex;
  align-items: center;
  color: #165dff;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s;
}

.back-link:hover {
  color: #0e42ff;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .forgot-password-container {
    padding: 16px;
  }
  
  .forgot-password-content {
    max-width: 100%;
  }
  
  .app-title {
    font-size: 28px;
  }
  
  .app-subtitle {
    font-size: 14px;
  }
  
  .header-title {
    font-size: 20px;
  }
}
</style> 