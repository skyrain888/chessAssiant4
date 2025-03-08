<template>
  <div class="login-container">
    <h2 class="text-xl font-bold mb-6">登录</h2>
    <a-form :model="form" @submit="handleSubmit" layout="vertical">
      <a-form-item field="username" label="用户名" :rules="[{ required: true, message: '请输入用户名' }]">
        <a-input v-model="form.username" placeholder="请输入用户名" allow-clear />
      </a-form-item>
      <a-form-item field="password" label="密码" :rules="[{ required: true, message: '请输入密码' }]">
        <a-input-password v-model="form.password" placeholder="请输入密码" allow-clear />
      </a-form-item>
      <div class="flex justify-between items-center mb-4">
        <a-checkbox v-model="rememberMe">记住我</a-checkbox>
        <a-link href="/auth/forgot-password">忘记密码？</a-link>
      </div>
      <a-button type="primary" html-type="submit" long :loading="loading">登录</a-button>
      <div class="mt-4 text-center">
        <span class="text-gray-500">还没有账号？</span>
        <a-link href="/auth/register">立即注册</a-link>
      </div>
    </a-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useNotification } from '@/composables/useNotification'

// 路由
const router = useRouter()

// 状态管理
const userStore = useUserStore()
const { success, error } = useNotification()

// 表单数据
const form = reactive({
  username: '',
  password: ''
})

// 记住我
const rememberMe = ref(false)

// 加载状态
const loading = ref(false)

// 提交表单
const handleSubmit = async () => {
  try {
    loading.value = true
    const result = await userStore.loginAction(form.username, form.password)
    if (result) {
      success('登录成功')
      router.push('/')
    }
  } catch (err) {
    error('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100%;
}
</style> 