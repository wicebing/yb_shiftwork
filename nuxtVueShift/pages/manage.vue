<script setup>

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

</style>