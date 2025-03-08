<template>
  <div class="register-container">
    <div class="register-content">
      <div class="register-logo">
        <h1 class="app-title">家长助手</h1>
        <p class="app-subtitle">面向学生家长的工具集合平台</p>
      </div>
      
      <a-card class="register-card" :bordered="false">
        <div class="register-header">
          <div class="header-title">注册账号</div>
          <div class="header-divider"></div>
          <p class="header-subtitle">欢迎加入家长助手，请填写以下信息完成注册</p>
        </div>
        
        <a-form ref="formRef" :model="form" layout="vertical" @submit="handleSubmit">
          <a-form-item field="username" label="用户名" :rules="[{ required: true, message: '请输入用户名' }]">
            <a-input v-model="form.username" placeholder="请输入用户名" allow-clear>
              <template #prefix>
                <icon-user />
              </template>
            </a-input>
          </a-form-item>
          
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
          
          <a-form-item field="password" label="密码" :rules="[
            { required: true, message: '请输入密码' },
            { minLength: 6, message: '密码长度不能少于6个字符' }
          ]">
            <a-input-password v-model="form.password" placeholder="请输入密码" allow-clear>
              <template #prefix>
                <icon-lock />
              </template>
            </a-input-password>
          </a-form-item>
          
          <a-form-item field="confirmPassword" label="确认密码" :rules="[
            { required: true, message: '请确认密码' },
            { validator: validateConfirmPassword, message: '两次输入的密码不一致' }
          ]">
            <a-input-password v-model="form.confirmPassword" placeholder="请确认密码" allow-clear>
              <template #prefix>
                <icon-check />
              </template>
            </a-input-password>
          </a-form-item>
          
          <a-form-item>
            <a-button type="primary" html-type="submit" long :loading="loading" class="register-button">
              注册
            </a-button>
          </a-form-item>
          
          <div class="register-footer">
            <span>已有账号？</span>
            <router-link to="/login" class="login-link">立即登录</router-link>
          </div>
        </a-form>
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Message } from '@arco-design/web-vue'
import { IconUser, IconLock, IconEmail, IconCheck } from '@arco-design/web-vue/es/icon'

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
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
  padding: 20px;
}

.register-content {
  width: 100%;
  max-width: 420px;
}

.register-logo {
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

.register-card {
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  background-color: #fff;
  padding-top: 16px;
}

.register-header {
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

.register-button {
  height: 40px;
  font-size: 16px;
  margin-top: 8px;
  transition: all 0.3s;
}

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 93, 255, 0.4);
}

.register-footer {
  margin-top: 24px;
  text-align: center;
  color: #86909c;
  font-size: 14px;
}

.login-link {
  color: #165dff;
  margin-left: 8px;
  font-weight: 500;
  transition: color 0.3s;
}

.login-link:hover {
  color: #0e42ff;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .register-container {
    padding: 16px;
  }
  
  .register-content {
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