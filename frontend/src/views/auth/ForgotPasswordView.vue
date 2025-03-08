<template>
  <div class="forgot-password-container">
    <h2 class="text-xl font-bold mb-6">忘记密码</h2>
    <a-form :model="form" @submit="handleSubmit" layout="vertical">
      <a-form-item field="email" label="邮箱" :rules="[
        { required: true, message: '请输入邮箱' },
        { type: 'email', message: '请输入有效的邮箱地址' }
      ]">
        <a-input v-model="form.email" placeholder="请输入注册时使用的邮箱" allow-clear />
      </a-form-item>
      <a-button type="primary" html-type="submit" long :loading="loading">发送重置链接</a-button>
      <div class="mt-4 text-center">
        <a-link href="/auth/login">返回登录</a-link>
      </div>
    </a-form>

    <a-result
      v-if="submitted"
      status="success"
      title="重置链接已发送"
      sub-title="请检查您的邮箱，按照邮件中的指引重置密码。"
    >
      <template #extra>
        <a-button type="primary" @click="goToLogin">返回登录</a-button>
      </template>
    </a-result>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from '@/composables/useNotification'
import { resetPassword } from '@/services/authService'

// 路由
const router = useRouter()

// 通知
const { success, error } = useNotification()

// 表单数据
const form = reactive({
  email: ''
})

// 状态
const loading = ref(false)
const submitted = ref(false)

// 提交表单
const handleSubmit = async () => {
  try {
    loading.value = true
    await resetPassword({ email: form.email })
    success('重置链接已发送到您的邮箱')
    submitted.value = true
  } catch (err) {
    error('发送重置链接失败，请检查邮箱是否正确')
  } finally {
    loading.value = false
  }
}

// 返回登录页
const goToLogin = () => {
  router.push('/auth/login')
}
</script>

<style scoped>
.forgot-password-container {
  width: 100%;
}
</style> 