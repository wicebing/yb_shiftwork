<script setup>
import { NInput, NButton, NForm, NFormItemRow,NFormItem, NDatePicker, NSwitch } from 'naive-ui'

const useStore = useUserStore()
const editing = ref(false)

function convertDate(editStaff) {
    console.log('convertDate', editStaff.birthday)
  return computed({
    get: () => new Date(editStaff.birthday).getTime(),
    set: (newValue) => (editStaff.birthday = formatDate(new Date(newValue))),
  });
}

</script>
<!-- //v-if=useStore.is_superuser -->
<template> 
  <div class="py-2 px-2" v-if=useStore.isAuthenticated>
    <div class="space-y-4">
      personal
      {{ useStore }}
      <n-form label-placement="left" label-width="auto" inline>
            <n-form-item label="員工權限認證">  
              <span class="text-pink-600 font-semibold"> {{useStore.is_staff}} </span>
            </n-form-item>
            <n-form-item label="管理員權限">  
              <span class="text-pink-600 font-semibold"> {{useStore.is_superuser}} </span>
            </n-form-item>              
      </n-form> 
      <span class="text-pink-600 font-semibold" v-if=!useStore.is_staff> 仍未綁定員工資料, 請等候管理員進行員工認證</span>
      <n-form label-placement="left" label-width="auto">
            <n-form-item-row label="員工編號">    
                <n-input placeholder="NTUHid" v-model:value="useStore.NTUHid" :disabled="!editing" />           
            </n-form-item-row>
            <n-form-item-row label="姓名">  
                <n-input placeholder="姓名" v-model:value="useStore.name" :disabled="!editing" />
            </n-form-item-row>
            <n-form-item-row label="生日">
                <n-date-picker type="date"  v-model:value="convertDate(useStore).value" :disabled="!editing" />  
            </n-form-item-row>
            <n-form-item-row label="登入帳戶名稱" v-if=useStore.is_staff>  
                <n-input placeholder="username" v-model:value="useStore.username" :disabled="!editing"/>
            </n-form-item-row>
            <n-form-item-row label="登入信箱" v-if=useStore.is_staff>  
                <n-input placeholder="email" v-model:value="useStore.email" clearable :disabled="!editing"/>
            </n-form-item-row>
            <n-form-item-row label="修改資料" v-if=useStore.is_staff>  
                <n-switch v-model:value="editing" />
            </n-form-item-row>
      </n-form>
        <n-button type="primary" block secondary strong @click="null" :disabled="!editing" v-if=useStore.is_staff>
            更正個人資料
        </n-button>
        <n-button type="primary" block secondary strong @click="null" :disabled="!editing" v-if=useStore.is_staff>
            修改密碼
        </n-button>           

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