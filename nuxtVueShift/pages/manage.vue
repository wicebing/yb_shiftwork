<script setup>
import { NTabs, NTabPane } from 'naive-ui'

const useStore = useUserStore()
</script>
<!-- //v-if=useStore.is_superuser -->
<template> 
  <div class="py-2 px-2" v-if=useStore.isAuthenticated>
    <div class="space-y-4">
      <manageStaff />
    </div>
  </div>
</template>

<style scoped>
.n-layout-sider {
  background: rgba(214, 213, 132, 0.342);
}
.n-layout-content {
  background: rgba(255, 254, 184, 0.308);
}
</style>