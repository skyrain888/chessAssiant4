<template>
  <div class="auth-layout">
    <div class="auth-container">
      <div class="auth-logo">
        <router-link to="/">
          <h1>家长助手</h1>
          <p>面向学生家长的工具集合平台</p>
        </router-link>
      </div>
      
      <router-view />
      
      <div class="auth-footer">
        <p>© {{ new Date().getFullYear() }} 家长助手 - 保留所有权利</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.auth-container {
  width: 100%;
  max-width: 420px;
  padding: 40px 0;
}

.auth-logo {
  text-align: center;
  margin-bottom: 40px;
}

.auth-logo a {
  text-decoration: none;
}

.auth-logo h1 {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 600;
  color: #165dff;
}

.auth-logo p {
  margin: 0;
  color: #86909c;
  font-size: 14px;
}

.auth-footer {
  margin-top: 40px;
  text-align: center;
  color: #86909c;
  font-size: 14px;
}
</style> 