<script setup>
import { NInput, NButton, NForm, NFormItemRow,NFormItem, NDatePicker, NSwitch, NDrawer, NDrawerContent } from 'naive-ui'

const useStore = useUserStore()
const editing = ref(false)
const editingPW = ref(false)
const placementDrawer = ref('right')
const newPW = ref('')

const originalStaff = reactive({
    staff_id: "",
    NTUHid: "",
    name: "",
    birthday: "",
});

const editStaff = reactive({
    staff_id:"",
    NTUHid: "",
    name: "",
    birthday: "",
})

const originalAUTH = reactive({
    id: "",
    username: "",
    password: "",
    email: "",

});

const editAUTH = reactive({
    id: "",
    username: "",
    password: "",
    email: "",
})

async function editData(useStore) {
    console.log("useStore:", useStore)
    Object.assign(editStaff, useStore)
    Object.assign(originalStaff, useStore); // Store the original data before editing
    console.log("useStore:", editStaff)
    activeDrawerStaffEdit.value = true
}

async function editAUTHData(useStore) {
    console.log("useAUTHStore:", useStore)
    Object.assign(editAUTH, useStore)
    Object.assign(originalAUTH, useStore); // Store the original data before editing
    console.log("useAUTHStore:", editAUTH)
    activeDrawerAUTHEdit.value = true
}

async function editAUTHPW() {
  editingPW.value = true
}

function convertDate(editStaff) {
    console.log('convertDate', editStaff.birthday)
  return computed({
    get: () => new Date(editStaff.birthday).getTime(),
    set: (newValue) => (editStaff.birthday = formatDate(new Date(newValue))),
  });
}

async function updateEditData() {
  editData(useStore)
  editAUTHData(useStore)
}

async function updateAllData() {
  updateAUTHData(useStore)
  updateStaffData(useStore)
  editing.value = false
}

async function updateAUTHData(useStore) {
    Object.assign(editAUTH, useStore)
    console.log("Updating staff data:", editAUTH);
    const updatedFields = {}
    for (const key in editAUTH) {
        if (editAUTH[key] !== originalAUTH[key]) {
            updatedFields[key] = editAUTH[key];
        }        
    }
    console.log('updatedFields', updatedFields)

    try {
        const { data, pending, refresh, error } = await useFetch(`/api/regist/${editAUTH.id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedFields),
        });

        console.log("Updated AUTH successfully:", data.value);
    } catch (error) {
        console.error('Error updating data:', error);
    }
}

async function updateStaffData(useStore) {
    Object.assign(editStaff, useStore)
    console.log("Updating staff data:", editStaff);
    const updatedFields = {}
    for (const key in editStaff) {
        if (editStaff[key] !== originalStaff[key]) {
            updatedFields[key] = editStaff[key];
        }        
    }
    console.log(`/api/staff/${editStaff.staff_id}/`)
    try {
        const { data, pending, refresh, error } = await useFetch(`/api/staff/${editStaff.staff_id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedFields),
        });

        console.log("Updated Staff successfully:", data.value);
        console.log("Updated Staff error:", error.value);
        getUset(); // Refresh the staff list after the update is successful
    } catch (error) {
        console.error('Error updating data:', error);
    }
}

async function updateAUTHpw() {
    console.log("Updating staff PW:");
    try {
        const { data, pending, refresh, error } = await useFetch(`/api/regist/${editAUTH.id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: {
              "password": newPW.value
            }
        });

        console.log("Updated AUTH PW successfully:", data.value);
        editingPW.value = false
    } catch (error) {
        console.error('Error updating PW data:', error);
    }
}

</script>
<!-- //v-if=useStore.is_superuser -->
<template> 
  <div class="py-2 px-2" v-if=useStore.isAuthenticated>
    <div class="space-y-4">
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
                <n-switch v-model:value="editing" @update:value="updateEditData"/>
            </n-form-item-row>
      </n-form>
      <n-button type="primary" block secondary strong @click="updateAllData" :disabled="!editing" v-if=useStore.is_staff>
          更正個人資料
      </n-button>
      <n-button type="primary" block secondary strong @click="editAUTHPW" :disabled="!editing" v-if=useStore.is_staff>
          修改密碼
      </n-button>
      <n-drawer v-model:show="editingPW" :width="502" :placement="placementDrawer">
        <n-drawer-content title="新增人員" closable>
            <n-form>
              <n-form-item-row label="password">
                    <n-input placeholder="密碼" v-model:value="newPW" />
              </n-form-item-row>
              <n-button type="primary" block secondary strong @click="updateAUTHpw()">
                    修改密碼
              </n-button>  
            </n-form>
        </n-drawer-content>
      </n-drawer>

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