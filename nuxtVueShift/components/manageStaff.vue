<script setup>
import { NButton, NTabs, NTabPane, NSwitch, NDrawer, NDrawerContent } from 'naive-ui'
import { NFormItemRow, NInput, NForm, NDatePicker } from 'naive-ui'
const useStore = useUserStore()

const data = ref([])
const columns = ref([
    // {
    //   title: 'id',
    //   key: 'id'
    // },
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
      render: () => 'Edit'
    },
    {
      title: 'Delete',
      key: '刪',
      render: () => 'Delete'
    }
])

const activeDrawer = ref(false)
const placementDrawer = ref('right')

const errors = ref([])
const result = reactive ({})
const resultAUTH = reactive ({})
let editing = reactive([])

const newStaff = reactive({
    NTUHid: "",
    name: "",
    birthday: null,
})

const editStaff = reactive({
    id:"",
    NTUHid: "",
    name: "",
    birthday: "",
    AUTHid: "",
})

async function getUset () {
    console.log('getUset')
    errors.value = []

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
    const { data, pending, refresh, error } = await useFetch('/api/regist/?is_staff=false',{
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

    Object.assign(resultAUTH, data.value.results)
}

function computedDate(rowIndex, colKey) {
  return computed({
    get: () => new Date(result[rowIndex][colKey]).getTime(),
    set: (newValue) => (result[rowIndex][colKey] = new Date(newValue)),
  });
}

function convertDate(dtString) {
    console.log('convertDate', dtString)
  return computed({
    get: () => new Date(dtString).getTime(),
    set: (newValue) => (dtString = formatDate(new Date(newValue))),
  });
}

async function editData(row) {
    console.log("Row:", row)
    Object.assign(editStaff, row)
    console.log("Row:", editStaff)
    activeDrawer.value = true
    // Perform your API call here to update the data
}

async function updateData(rowIndex) {
    console.log("Row:", rowIndex);
    // Perform your API call here to update the data
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

// watch(result, () => {
//   getUset();
// }, { deep: true });

onMounted(() => {
    getUset()
    getAUTH()
})

</script>

<template>
    <div v-if=useStore.isAuthenticated class="flex items-center space-x-4 font-bold font-mono text-left">
        <n-tabs
        class="card-tabs"
        default-value="allStaff"
        size="small"
        animated
        pane-style="padding-left: 4px; padding-right: 4px; box-sizing: border-box;"
        >
            <n-tab-pane name="allStaff" tab="人員總覽">
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
                                v-if="!res[col.key]"
                                secondary
                                :strong="col.title === 'Delete'"
                                :type="col.title === 'Delete' ? 'error' : 'info'"
                                @click="col.title === 'Delete' ? deleteData(res) : editData(res)"
                                >
                                    {{ col.key }}
                                </n-button>

                                <n-switch v-if="col.key==='Edit'" v-model:value="editing[rowIndex]" />

                                <n-date-picker 
                                v-if="col.key==='birthday' && res[col.key]"
                                type="date"
                                :disabled="!editing[rowIndex]"
                                v-model:value="computedDate(rowIndex, col.key).value"
                                />

                                <n-input
                                v-if="col.key!=='birthday' && res[col.key]"
                                type="text"
                                size="small"
                                :readonly="!editing[rowIndex]"
                                v-model:value="res[col.key]"
                                @change="updateData(rowIndex)"
                                />                                    

                                <connectAUTHid v-if="col.key==='AUTHid'" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </n-tab-pane>
            <n-tab-pane name="addnewStaff" tab="新增">
                <n-form>
                    <n-form-item-row label="NTUHid">
                        <n-input placeholder="NTUHid" v-model:value="newStaff.NTUHid" />
                    </n-form-item-row>
                    <n-form-item-row label="name">
                        <n-input placeholder="姓名" v-model:value="newStaff.name" />
                    </n-form-item-row>
                    <n-form-item-row label="birthday">
                        <n-date-picker type="date"  v-model:value="newStaff.birthday" value-format="MM-dd-yyyy" />
                    </n-form-item-row>
                    <n-button type="primary" block secondary strong @click="addData">
                    新增
                    </n-button>
                </n-form>
            </n-tab-pane>
        </n-tabs>
    </div>
    <n-drawer v-model:show="activeDrawer" :width="502" :placement="placementDrawer">
    <n-drawer-content title="人員編輯" closable>
        <n-form-item-row label="NTUHid">    
            <n-input placeholder="NTUHid" v-model:value="editStaff.NTUHid" />           
        </n-form-item-row>
        <n-form-item-row label="name">  
            <n-input placeholder="姓名" v-model:value="editStaff.name" />
        </n-form-item-row>
        <n-form-item-row label="birthday">
            <n-date-picker type="date"  v-model:value="convertDate(editStaff.birthday).value" />  
        </n-form-item-row>
        <n-form-item-row label="註冊帳戶">  
            <n-input placeholder="AUTHid" v-model:value="editStaff.AUTHid"/>
        </n-form-item-row>
    </n-drawer-content>
    </n-drawer>
</template>