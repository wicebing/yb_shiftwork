<script setup>
import { NButton, NTabs, NTabPane, NSwitch, NDrawer, NDrawerContent, NSelect } from 'naive-ui'
import { NFormItemRow, NInput, NForm, NDatePicker } from 'naive-ui'
const useStore = useUserStore()

const data = ref([])
const columns = ref([
    {
      title: 'NTUHid',
      key: 'NTUHid'
    },
    {
      title: 'name',
      key: 'name'
    },
    {
      title: 'birthday',
      key: 'birthday'
    },
    {
      title: 'AUTHid',
      key: 'AUTHid'
    },
    {
      title: 'Edit',
      key: 'Edit',
    },
    {
      title: '超排減班',
      key: 'Ex/Rx',
    },
    {
      title: 'Delete',
      key: '刪',
    }
])

const columnsExRx = ref([
    {
      title: 'id',
      key: 'id'
    },
    {
      title: 'description',
      key: 'description'
    },
    {
      title: 'credit',
      key: 'credit'
    },
    {
      title: 'Edit',
      key: 'Edit',
    },
])

const columnsAUTH = ref([
    {
      title: 'id',
      key: 'id'
    },
    {
      title: 'username',
      key: 'username'
    },
    {
      title: '員工',
      key: 'is_staff'
    },
    {
      title: '管理者',
      key: 'is_superuser'
    },
    {
      title: 'Edit',
      key: 'Edit',
      render: () => 'Edit'
    },
    {
      title: 'Delete',
      key: '刪',
      render: () => 'Delete'
    }
])

const activeDrawerStaffEdit = ref(false)
const placementDrawer = ref('right')
const activeDrawerStaffAdd = ref(false)
const activeDrawerAUTHEdit = ref(false)
const activeDrawerExRxEdit = ref(false)

const errors = ref([])
const result = reactive ({})
const resultAUTH = reactive ({})
const resultAUTH_nonStaff = reactive ({})
const editing = reactive([])
const editingAUTH = reactive([])
const valueSelect= ref(null)
const extra = reactive ({})
const relax = reactive ({})

const newStaff = reactive({
    NTUHid: "",
    name: "",
    birthday: null,
})

const originalStaff = reactive({
    id: "",
    NTUHid: "",
    name: "",
    birthday: "",
    AUTHid: null
});

const editStaff = reactive({
    id:"",
    NTUHid: "",
    name: "",
    birthday: "",
    AUTHid: null,
})

const editExtraRelax = reactive({
    id:"",
    NTUHid: "",
    name: "",
    birthday: "",
    AUTHid: null,
})

const originalAUTH = reactive({
    id: "",
    username: "",
    password: "",
    email: "",
    is_staff: false,
    is_superuser: false
});

const editAUTH = reactive({
    id: "",
    username: "",
    password: "",
    email: "",
    is_staff: false,
    is_superuser: false
})

const options = computed(() => {
    console.log('ResultAUTH',resultAUTH_nonStaff)
    return Object.values(resultAUTH_nonStaff).map((user) => ({
                        label: user.username,
                        value: user.id
                        }));
})

async function getUset () {
    console.log('getUset')
    errors.value = []
    for (const key in result) {
        delete result[key];
    }
    const { data, pending, refresh, error } = await useFetch('/api/staff/', {
        method: 'GET',
        baseURL:'http://localhost:8000',
        headers: {
            Authorization: `JWT ${useStore.token}` 
        }
    })
    console.log('data',data.value)
    console.log('error',error)
    
    errors.value.push(error)
    errors.value.push(data.value.results)

    Object.assign(result, data.value.results)
}

async function getAUTH () {
    console.log('getAUTH')
    errors.value = []
    for (const key in resultAUTH) {
        delete resultAUTH[key];
    }
    for (const key in resultAUTH_nonStaff) {
        delete resultAUTH_nonStaff[key];
    }
    const { data, pending, refresh, error } = await useFetch('/api/regist/',{
        method: 'GET',
        baseURL:'http://localhost:8000',
        headers: {
            Authorization: `JWT ${useStore.token}` 
        }
    })

    // const { data } = await useFetch(() => `/api/hello/${count.value}`, { params: { token: 123 } })
    console.log('AUTHdata',data.value)
    console.log('AUTHerror',error)
    
    errors.value.push(error)
    errors.value.push(data.value.results)

    const allUsers = data.value.results;
    const nonAdminUsers = allUsers.filter(user => user.username !== 'admin' && user.username !== 'bing');
    const nonStaffUsers = allUsers.filter(user => !user.is_staff);

    Object.assign(resultAUTH, nonAdminUsers)
    Object.assign(resultAUTH_nonStaff, nonStaffUsers)
    console.log('resultAUTH',resultAUTH)
    console.log('resultAUTH_nonStaff',resultAUTH_nonStaff)
}

function convertDate(editStaff) {
    console.log('convertDate', editStaff.birthday)
  return computed({
    get: () => new Date(editStaff.birthday).getTime(),
    set: (newValue) => (editStaff.birthday = formatDate(new Date(newValue))),
  });
}

async function editData(row) {
    console.log("Row:", row)
    Object.assign(editStaff, row)
    Object.assign(originalStaff, row); // Store the original data before editing
    console.log("Row:", editStaff)
    activeDrawerStaffEdit.value = true
}

async function editExtraRelaxData(row) {
    getExRx(row.NTUHid)
    console.log("Row:", row)
    Object.assign(editExtraRelax, row)
    console.log("Row:", editStaff)
    activeDrawerExRxEdit.value = true
}

async function editAUTHData(row) {
    console.log("Row:", row)
    Object.assign(editAUTH, row)
    Object.assign(originalAUTH, row); // Store the original data before editing
    console.log("Row:", editAUTH)
    activeDrawerAUTHEdit.value = true
}

async function updateAUTHData(editAUTH) {
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
        getAUTH(); // Refresh the staff list after the update is successful
    } catch (error) {
        console.error('Error updating data:', error);
    }
    activeDrawerAUTHEdit.value = false;
}

async function updateData(editStaff) {
    console.log("Updating staff data:", editStaff);
    const updatedFields = {}
    const updateAUTH = ref(false)
    const originAUTHid = ref(null)
    const editAUTHid = ref(null)
    for (const key in editStaff) {
        originAUTHid.value = originalStaff.AUTHid
        editAUTHid.value = editStaff.AUTHid
        if (editStaff[key] !== originalStaff[key]) {
            updatedFields[key] = editStaff[key];
            if (key === 'AUTHid') {
                updateAUTH.value=true
                console.log('updateAUTHkey', key)
            }
            console.log('key', key)
        }        
    }

    try {
        const { data, pending, refresh, error } = await useFetch(`/api/staff/${editStaff.id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedFields),
        });

        console.log("Updated successfully:", data.value);
        getUset(); // Refresh the staff list after the update is successful
    } catch (error) {
        console.error('Error updating data:', error);
    }

    if (updateAUTH.value) {
        console.log('updateAUTH 3333', updateAUTH.value, editAUTHid.value, `/api/regist/${originAUTHid.value}/`)

        try{
            const { data:dataU, pending:pendingU, refresh:refreshU, error:errorU } = await useFetch(`/api/regist/${editAUTHid.value}/`,{
                method: 'PATCH',
                baseURL:'http://localhost:8000',
                headers: {
                    Authorization: `JWT ${useStore.token}` 
                },
                body: {
                    is_staff: true,
                    }
            })

            console.log("Updated AUTH successfully:", dataU.value);
            console.log("Updated AUTH ERROR:", errorU.value);            
        } catch (error) {
            console.error('Error updating AUTH:', error);
        }

        try{
            const { data:dataD, pending:pendingD, refresh:refreshD, error:errorD } = await useFetch(`/api/regist/${originAUTHid.value}/`,{
                method: 'PATCH',
                baseURL:'http://localhost:8000',
                headers: {
                    Authorization: `JWT ${useStore.token}` 
                },
                body: {
                    is_staff: false,
                    }
            })

            console.log("Remove AUTH successfully:", dataD.value);
            console.log("Remove AUTH ERROR:", errorD.value);    
        } catch (error) {
            console.error('Error updating Remove:', error);
        }
    }
    getAUTH()
    activeDrawerStaffEdit.value = false;
}

async function deleteData(row) {
    try {
        console.log('deleteData', row)
        const { data, pending, refresh, error } = await useFetch(`/api/staff/${row.id}`, {
        method: 'DELETE',
        baseURL: 'http://localhost:8000',
        headers: {
            Authorization: `JWT ${useStore.token}`,
        },
        })

        console.log('deleteData', row)
        console.log('Deleted successfully')
        console.log('Error: ', error.value)
    } catch (error) {
        console.error('Error deleting data:', error);
    }
    getUset()
    editing = reactive([])
}

async function deleteAUTHData(row) {
    try {
        console.log('deleteAUTHData', row)
        const { data, pending, refresh, error } = await useFetch(`/api/regist/${row.id}`, {
        method: 'DELETE',
        baseURL: 'http://localhost:8000',
        headers: {
            Authorization: `JWT ${useStore.token}`,
        },
        })

        console.log('Deleted AUTH successfully')
        console.log('Error: ', error.value)
    } catch (error) {
        console.error('Error deleting data:', error);
    }
    getAUTH()
    editingAUTH = reactive([])
}



async function getExtra (NTUH_id) {
    console.log('getExtra')
    for (const key in extra) {
        delete extra[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch(`/api/staffExtra/?staff_id=${NTUH_id}`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data project',data.value)
            Object.assign(extra, data.value.results)
            console.log('result project',extra)
        } else {
            console.log('error',error)
        }
    } catch (err) {
        console.log('err',err)
    }
}

async function getRelax (NTUH_id) {
    console.log('getRelax')
    for (const key in relax) {
        delete relax[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch(`/api/staffRelax/?staff_id=${NTUH_id}`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data project',data.value)
            Object.assign(relax, data.value.results)
            console.log('result project',relax)
        } else {
            console.log('error',error)
        }
    } catch (err) {
        console.log('err',err)
    }
}

async function updateExtraData(row) {
    console.log("Updating staff data:", row);

    try {
        const { data, pending, refresh, error } = await useFetch(`/api/staffExtra/${row.id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: {'credit': row.credit,}
        });

        console.log("Updated successfully:", data.value);
        // getExtra(row.NTUHid); // Refresh the staff list after the update is successful
    } catch (error) {
        console.error('Error updating data:', error);
    }
    activeDrawerStaffEdit.value = false;
}

function getExRx(NTUHid) {
    console.log('getExRx')
    getExtra(NTUHid)
    getRelax(NTUHid)
}

async function updateRelaxData(row) {
    console.log("Updating staff data:", row);

    try {
        const { data, pending, refresh, error } = await useFetch(`/api/staffRelax/${row.id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: {'credit': row.credit,}
        });

        console.log("Updated successfully:", data.value);
        // getRelax(row.NTUHid); // Refresh the staff list after the update is successful
    } catch (error) {
        console.error('Error updating data:', error);
    }
    activeDrawerStaffEdit.value = false;
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

async function addData() {
  try {
    console.log('addData')
    console.log('NEWdate',newStaff)
    const { data, pending, refresh, error } = await useFetch('/api/staff/', {
        method: 'POST',
        baseURL:'http://localhost:8000',
        headers: {
        Authorization: `JWT ${useStore.token}`,
        },
        body: {
            id: newStaff.NTUHid,
            NTUHid: newStaff.NTUHid,
            name: newStaff.name,
            birthday: formatDate(new Date(newStaff.birthday)),
        }
    })

    console.log("New staff added:", data.value)
    console.log('error',error)
    console.log('error',error._object.detail)
    // console.log('2222222', row)
    // if (data.value) {
    //   console.log('Deleted successfully');
    // } else {
    //   console.log('Error: ', error.value);
    // }
  } catch (error) {
    console.error('Error deleting data:', error);
  }
  getUset()
}

async function switchAddStaff(){
    activeDrawerStaffAdd.value = true
}



onMounted(() => {
    getUset()
    getAUTH()
})

</script>

<template>
    <div v-if=useStore.isAuthenticated class="flex items-center space-x-4 font-bold font-mono text-left">
        <n-tabs
        type="segment"
        class="card-tabs"
        default-value="allStaff"
        size="small"
        animated
        pane-style="padding-left: 4px; padding-right: 4px; box-sizing: border-box;"
        >
            <n-tab-pane name="allStaff" tab="人員總覽">
                <n-button dashed type="warning" strong
                @click=switchAddStaff
                >
                    新增員工
                </n-button>
                <table class="table-auto min-w-full">
                    <thead class="bg-gray-50">
                        <tr>
                            <th v-for="col in columns" class="px-2 py-4 text-xs font-bold text-gray-500" scope="col">{{ col.title }}</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr v-for="(res, rowIndex) in result">
                            <td v-for="col in columns" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                                <n-button 
                                v-if="!res[col.key] && col.title === 'Edit'"
                                secondary
                                type='info'
                                @click= editData(res)
                                >
                                    {{ col.key }}
                                </n-button>

                                <n-button 
                                v-if="!res[col.key] && col.key === 'Ex/Rx'"
                                secondary
                                type='warning'
                                @click= editExtraRelaxData(res)
                                >
                                    {{ col.key }}
                                </n-button>

                                <n-button 
                                v-if="!res[col.key]  && col.title === 'Delete'"
                                secondary strong type='error'
                                @click=deleteData(res)
                                :disabled="!editing[rowIndex]"
                                >
                                    {{ col.key }}
                                </n-button>

                                <n-switch v-if="col.title==='Delete'" v-model:value="editing[rowIndex]" />

                                <div v-if=res[col.key]>
                                    {{ res[col.key] }}
                                </div>                              
                            </td>
                        </tr>
                    </tbody>
                </table>
            </n-tab-pane>

            <n-tab-pane name="allAUTH" tab="註冊用戶總覽">
                <table class="table-auto min-w-full">
                    <thead class="bg-gray-50">
                        <tr>
                            <th v-for="col in columnsAUTH" class="px-2 py-4 text-xs font-bold text-gray-500" scope="col">{{ col.title }}</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr v-for="(res, rowIndex) in resultAUTH">
                            <td v-for="col in columnsAUTH" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                                <n-button 
                                v-if="!res[col.key] && col.title === 'Edit'"
                                secondary
                                type='info'
                                @click= editAUTHData(res)
                                >
                                    {{ col.key }}
                                </n-button>

                                <n-button 
                                v-if="!res[col.key]  && col.title === 'Delete'"
                                secondary strong type='error'
                                @click=deleteAUTHData(res)
                                :disabled="!editingAUTH[rowIndex]"
                                >
                                    {{ col.key }}
                                </n-button>

                                <n-switch v-if="col.title==='Delete'" v-model:value="editingAUTH[rowIndex]" />

                                <div v-if=res[col.key]>
                                    {{ res[col.key] }}
                                </div>                              
                            </td>
                        </tr>
                    </tbody>
                </table>
            </n-tab-pane>

        </n-tabs>
    </div>
    <n-drawer v-model:show="activeDrawerStaffEdit" :width="502" :placement="placementDrawer">
        <n-drawer-content title="人員編輯" closable>
            <n-form>
                <n-form-item-row label="NTUHid">    
                    <n-input placeholder="NTUHid" v-model:value="editStaff.NTUHid" disabled="true"/>           
                </n-form-item-row>
                <n-form-item-row label="name">  
                    <n-input placeholder="姓名" v-model:value="editStaff.name" />
                </n-form-item-row>
                <n-form-item-row label="birthday">
                    <n-date-picker type="date"  v-model:value="convertDate(editStaff).value" />  
                </n-form-item-row>
                <n-form-item-row label="註冊帳戶">  
                    <n-input placeholder="AUTHid" v-model:value="editStaff.AUTHid" clearable/>
                    <n-select v-model:value="editStaff.AUTHid" :options="options" />
                </n-form-item-row>
                <n-button type="primary" block secondary strong @click="updateData(editStaff)">
                    更正
                </n-button>       
            </n-form>
        </n-drawer-content>
    </n-drawer>
    <n-drawer v-model:show="activeDrawerExRxEdit" :width="502" :placement="placementDrawer">
        <n-drawer-content title="超排減班編輯" closable>
            <n-form >
                <span class="text-pink-600 font-semibold text-lg">
                    {{ editExtraRelax.name}} - {{ editExtraRelax.NTUHid }}   
                </span>
                <n-form-item-row label="超排設定">
                    <table class="table-auto min-w-full">
                        <thead class="bg-gray-50">
                            <tr>
                                <th v-for="col in columnsExRx" class="px-2 py-4 text-xs font-bold text-gray-500" scope="col">{{ col.title }}</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="(res, rowIndex) in extra">
                                <td v-for="col in columnsExRx" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                                    <n-button 
                                    v-if="!res[col.key] && col.title === 'Edit'"
                                    secondary
                                    type='info'
                                    @click= updateExtraData(res)
                                    >
                                        {{ col.key }}
                                    </n-button>

                                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key!=='credit'">
                                        {{ res[col.key] }}
                                    </div>
                                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key==='credit'">
                                        <n-input placeholder="credit" v-model:value="res[col.key]" />
                                    </div>                              
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </n-form-item-row>
                <n-form-item-row label="減班設定">
                    <table class="table-auto min-w-full">
                        <thead class="bg-gray-50">
                            <tr>
                                <th v-for="col in columnsExRx" class="px-2 py-4 text-xs font-bold text-gray-500" scope="col">{{ col.title }}</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="(res, rowIndex) in relax">
                                <td v-for="col in columnsExRx" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                                    <n-button 
                                    v-if="!res[col.key] && col.title === 'Edit'"
                                    secondary
                                    type='info'
                                    @click= updateRelaxData(res)
                                    >
                                        {{ col.key }}
                                    </n-button>

                                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key!=='credit'">
                                        {{ res[col.key] }}
                                    </div>
                                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key==='credit'">
                                        <n-input placeholder="credit" v-model:value="res[col.key]" />
                                    </div>                          
                                </td>
                            </tr>
                        </tbody>
                    </table>                     
                </n-form-item-row>
  
            </n-form>
        </n-drawer-content>
    </n-drawer>
    <n-drawer v-model:show="activeDrawerAUTHEdit" :width="502" :placement="placementDrawer">
        <n-drawer-content title="人員編輯" closable>
            <n-form>
                <n-form-item-row label="username">  
                    <n-input placeholder="用戶帳號" v-model:value="editAUTH.username" />
                </n-form-item-row>
                <n-form-item-row label="Email">
                    <n-input placeholder="信箱" v-model:value="editAUTH.email" />
                </n-form-item-row>
                <n-form-item-row label="password">
                    <n-input placeholder="密碼" v-model:value="editAUTH.password" />
                </n-form-item-row>
                <n-form-item-row label="員工認證"> 
                    {{ editAUTH.is_staff }}
                    <n-switch v-model:value="editAUTH.is_staff" />
                </n-form-item-row>
                <n-form-item-row label="管理員"> 
                    {{ editAUTH.is_superuser }} 
                    <n-switch v-model:value="editAUTH.is_superuser" />
                </n-form-item-row>
                <n-button type="primary" block secondary strong @click="updateAUTHData(editAUTH)">
                    更正
                </n-button>       
            </n-form>
        </n-drawer-content>
    </n-drawer>
    <n-drawer v-model:show="activeDrawerStaffAdd" :width="502" :placement="placementDrawer">
        <n-drawer-content title="新增人員" closable>
            <n-form>
                <n-form-item-row label="NTUHid">
                    <n-input placeholder="NTUHid" v-model:value="newStaff.NTUHid" />
                </n-form-item-row>
                <n-form-item-row label="name">
                    <n-input placeholder="姓名" v-model:value="newStaff.name" />
                </n-form-item-row>
                <n-form-item-row label="birthday">
                    <n-date-picker type="date"  v-model:value="newStaff.birthday" />
                </n-form-item-row>
                <n-button type="primary" block secondary strong @click="addData">
                新增
                </n-button>
            </n-form>
        </n-drawer-content>
    </n-drawer>
</template>