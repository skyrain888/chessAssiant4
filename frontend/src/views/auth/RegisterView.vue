<template>
  <div class="register-container">
    <h2 class="text-xl font-bold mb-6">注册</h2>
    <a-form :model="form" @submit="handleSubmit" layout="vertical">
      <a-form-item field="username" label="用户名" :rules="[{ required: true, message: '请输入用户名' }]">
        <a-input v-model="form.username" placeholder="请输入用户名" allow-clear />
      </a-form-item>
      <a-form-item field="email" label="邮箱" :rules="[
        { required: true, message: '请输入邮箱' },
        { type: 'email', message: '请输入有效的邮箱地址' }
      ]">
        <a-input v-model="form.email" placeholder="请输入邮箱" allow-clear />
      </a-form-item>
      <a-form-item field="name" label="姓名">
        <a-input v-model="form.name" placeholder="请输入姓名" allow-clear />
      </a-form-item>
      <a-form-item field="password" label="密码" :rules="[
        { required: true, message: '请输入密码' },
        { minLength: 6, message: '密码长度不能少于6位' }
      ]">
        <a-input-password v-model="form.password" placeholder="请输入密码" allow-clear />
      </a-form-item>
      <a-form-item field="confirmPassword" label="确认密码" :rules="[
        { required: true, message: '请确认密码' },
        { validator: validateConfirmPassword, message: '两次输入的密码不一致' }
      ]">
        <a-input-password v-model="form.confirmPassword" placeholder="请确认密码" allow-clear />
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model="form.agreement" :rules="[{ type: 'boolean', true: true, message: '请同意用户协议' }]">
          我已阅读并同意
          <a-link>用户协议</a-link>
          和
          <a-link>隐私政策</a-link>
        </a-checkbox>
      </a-form-item>
      <a-button type="primary" html-type="submit" long :loading="loading">注册</a-button>
      <div class="mt-4 text-center">
        <span class="text-gray-500">已有账号？</span>
        <a-link href="/auth/login">立即登录</a-link>
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
  email: '',
  name: '',
  password: '',
  confirmPassword: '',
  agreement: false
})

// 加载状态
const loading = ref(false)

// 验证确认密码
const validateConfirmPassword = (value: string) => {
  return form.password === value
}

// 提交表单
const handleSubmit = async () => {
  if (!form.agreement) {
    error('请同意用户协议和隐私政策')
    return
  }

  try {
    loading.value = true
    const result = await userStore.registerAction(
      form.username,
      form.password,
      form.email,
      form.name || undefined
    )
    if (result) {
      success('注册成功')
      router.push('/')
    }
  } catch (err) {
    error('注册失败，请检查输入信息')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  width: 100%;
}
</style> 