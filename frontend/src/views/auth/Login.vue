<template>
  <div class="login-container">
    <div class="login-content">
      <div class="login-logo">
        <h1 class="app-title">家长助手</h1>
        <p class="app-subtitle">面向学生家长的工具集合平台</p>
      </div>
      
      <a-card class="login-card" :bordered="false">
        <div class="login-header">
          <div class="header-title">登录账号</div>
          <div class="header-divider"></div>
          <p class="header-subtitle">欢迎回到家长助手，请登录您的账号</p>
        </div>
        
        <a-form ref="formRef" :model="form" layout="vertical" @submit="handleSubmit">
          <a-form-item field="email" label="邮箱" :rules="[
            { required: true, message: '请输入邮箱' },
            { type: 'email', message: '请输入有效的邮箱地址' }
          ]">
            <a-input v-model="form.email" placeholder="请输入邮箱" allow-clear>
              <template #prefix>
                <icon-user />
              </template>
            </a-input>
          </a-form-item>
          
          <a-form-item field="password" label="密码" :rules="[
            { required: true, message: '请输入密码' }
          ]">
            <a-input-password v-model="form.password" placeholder="请输入密码" allow-clear>
              <template #prefix>
                <icon-lock />
              </template>
            </a-input-password>
          </a-form-item>
          
          <div class="login-options">
            <a-checkbox v-model="form.remember">记住我</a-checkbox>
            <router-link to="/forgot-password" class="forgot-password">忘记密码？</router-link>
          </div>
          
          <a-form-item>
            <a-button type="primary" html-type="submit" long :loading="loading" class="login-button">
              登录
            </a-button>
          </a-form-item>
          
          <div class="login-footer">
            <span>还没有账号？</span>
            <router-link to="/register" class="register-link">立即注册</router-link>
          </div>
        </a-form>
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Message } from '@arco-design/web-vue'
import { IconUser, IconLock } from '@arco-design/web-vue/es/icon'

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
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
  padding: 20px;
}

.login-content {
  width: 100%;
  max-width: 420px;
}

.login-logo {
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

.login-card {
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  background-color: #fff;
  padding-top: 16px;
}

.login-header {
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

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.forgot-password {
  color: #165dff;
  font-size: 14px;
  transition: color 0.3s;
}

.forgot-password:hover {
  color: #0e42ff;
  text-decoration: underline;
}

.login-button {
  height: 40px;
  font-size: 16px;
  margin-top: 8px;
  transition: all 0.3s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 93, 255, 0.4);
}

.login-footer {
  margin-top: 24px;
  text-align: center;
  color: #86909c;
  font-size: 14px;
}

.register-link {
  color: #165dff;
  margin-left: 8px;
  font-weight: 500;
  transition: color 0.3s;
}

.register-link:hover {
  color: #0e42ff;
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-container {
    padding: 16px;
  }
  
  .login-content {
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