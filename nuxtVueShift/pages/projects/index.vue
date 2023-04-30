<script setup>
import { NTabs, NTabPane, } from 'naive-ui'

const useStore = useUserStore()

onMounted(() => {

})

</script>
<!-- //v-if=useStore.is_superuser -->
<template> 
  <div class="py-2 px-2" v-if=useStore.isAuthenticated>
    <div class="space-y-4">
        <ShiftProjects />
    </div>
  </div>
</template>

<style scoped>
</style>