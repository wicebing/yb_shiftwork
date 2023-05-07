<script setup>
import {NButton, NDrawer, NDrawerContent, NForm, NFormItemRow, NInput, NSwitch, NTransfer, NDivider } from 'naive-ui'

const useStore = useUserStore()

const columns = ref([
    {
      title: '組別',
      key: 'name'
    },
    {
      title: '優先碼',
      key: 'priority'
    },
    {
      title: '編碼',
      key: 'turn'
    },
    {
      title: 'mod',
      key: 'mod'
    },
    {
      title: '組員',
      key: 'groups'
    },
    {
      title: '變更組員',
      key: 'EditGroup',
    },
    {
      title: 'Edit',
      key: 'Edit',
    },
    {
      title: 'Delete',
      key: '刪',
    }
])

const columnsGroup = ref([
    {
      title: '優先碼',
      key: 'priority'
    },
    {
      title: '編碼',
      key: 'turn'
    },
    {
      title: '姓名',
      key: 'staff_name'
    },
    {
      title: '更新',
      key: 'Edit',
    },
    {
      title: 'Delete',
      key: '刪',
    }
])

const options = ref([
    {
      label: '白',
      value: 'D'
    },
    {
      label: '小夜',
      value: 'A'
    },
    {
      label: '夜',
      value: 'N'
    }
])

const result = reactive ({})
const activeDrawerProjectEdit = ref(false)
const activeDrawerProjectAdd = ref(false)
const activeDrawerGroupEdit = ref(false)
const placementDrawer = ref('right')
const editing = reactive([])
const editingGroup = reactive([])
const errors = ref([])
const resultStaff = reactive ({})
const groupStaff = reactive ({})
const optionsSelectStaff = ref([]);
const oldGroupMembers = ref([]);
const newAddMembers = ref([]);
const specialGroup = ref(false);

const newProject = reactive({
    id: "",
    name: "",
    priority: "",
    turn: "",
    mod: "",
    groups: "",
})

const originalProject = reactive({
    id: "",
    name: "",
    priority: "",
    turn: "",
    mod: "",
    groups: "",
});

const editProject = reactive({
    id: "",
    name: "",
    priority: "",
    turn: "",
    mod: "",
    groups: "",
})

const optionsStaff = computed(() => {
    console.log('resultStaff', resultStaff);
    return Object.values(resultStaff).map((user) => {
        const inOptionsSelectStaff = optionsSelectStaff.value.includes(user.id);
        const hasGroups = user.groups.length > 0;
        return {
            label: user.name,
            value: user.id,
            disabled: hasGroups, // set disabled to true if groups array has elements or if the user is in optionsSelectStaff, otherwise false
        };
    });
});

const optionsStaffSpecial = computed(() => {
    console.log('resultStaff', resultStaff);
    return Object.values(resultStaff).map((user) => {
        return {
            label: user.name,
            value: user.id,
        };
    });
});

function formatGroups(groups) {
    // console.log('formatGroups', user)
    // return groups.map((user) => user.staff)
  return groups.map((group) => `${group.priority}-${group.turn}-${group.staff_name}-${group.staff}`);
}


async function getUser () {
    console.log('getUser')
    errors.value = []
    for (const key in resultStaff) {
        delete resultStaff[key];
    }
    try {
        const { data, pending, refresh, error } = await useFetch('/api/staff/?ordering=NTUHid', {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data',data.value)
            console.log('error',error)
            Object.assign(resultStaff, data.value.results)        
        } else {
            console.log('error',error)
            errors.value.push(error)
            errors.value.push(data.value.results)
        }
    } catch {
        console.log('error',error)
        errors.value.push(error)
    }
}

async function getGroup (groupname) {
    console.log('getGroup:',groupname)
    errors.value = []
    for (const key in groupStaff) {
        delete groupStaff[key];
    }

    try {
        const { data, pending, refresh, error } = await useFetch(`/api/group/?groupname_id=${groupname}`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('getGroupData',data.value)
            Object.assign(groupStaff, data.value.results)
            optionsSelectStaff.value = data.value.results.map((user) => user.staff) // update optionsSelectStaff with the staff ids   
            oldGroupMembers.value = data.value.results.map((user) => user.staff)
            getUser()
            getProject()
        } else {
            console.log('error',error)
            errors.value.push(error)
            errors.value.push(data.value.results)
        }
    } catch {
        console.log('error',error)
        errors.value.push(error)
    }
}

async function getProject () {
    console.log('getProject')
    for (const key in result) {
        delete result[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch('/api/groupname/', {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            },
            params: {
                ordering: "priority,turn",
            },
        })
        console.log('data',data.value)
        console.log('error',error)

        Object.assign(result, data.value.results)
        console.log('result',result)
    } catch (err) {
        console.log('err',err)
    }
}

async function editData(row) {
    console.log("Row:", row)
    console.log("Rowid:", row.id)
    await getGroup(row.id)
    Object.assign(editProject, row)
    Object.assign(originalProject, row); // Store the original data before editing
    console.log("editProject:", editProject)
    activeDrawerProjectEdit.value = true
}

async function editDataGroup(row) {
    console.log("Row:", row)
    console.log("Rowid:", row.id)
    await getGroup(row.id)
    Object.assign(editProject, row)
    Object.assign(originalProject, row); // Store the original data before editing
    console.log("editProject:", editProject)
    activeDrawerGroupEdit.value = true
}

async function deleteData(row) {
    try {
        console.log('deleteData', row)
        const { data, pending, refresh, error } = await useFetch(`/api/groupname/${row.id}`, {
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
    getProject()
    editing = reactive([])
}

async function deleteDataGroup(row,groupname) {
    try {
        console.log('deleteData', row)
        const { data, pending, refresh, error } = await useFetch(`/api/group/${row.id}`, {
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
    getGroup(groupname)
    editingGroup = reactive([])
}

async function addData() {
    errors.value = []
    try {
        console.log('addData')
        console.log('NEWdate',newProject)
        const { data, pending, refresh, error } = await useFetch('/api/groupname/', {
            method: 'POST',
            baseURL:'http://localhost:8000',
            headers: {
            Authorization: `JWT ${useStore.token}`,
            },
            body: {
                name: newProject.name,
                priority: newProject.priority,
                turn: newProject.turn,
            }
        })

        if (data.value) {
            console.log("New staff added:", data.value)
            getProject()
        } else {
            console.log('error',error)
            console.log('errorName',error.value.data)
            errors.value.push(error.value.data)
        }

    } catch (error) {
        console.error('Error deleting data:', error);
    }
}

function switchactiveDrawerProjectAdd() {
    activeDrawerProjectAdd.value = !activeDrawerProjectAdd.value
}

function findStaffIds(optionsSelectStaff, groupStaff) {
  const staffIds = [];
  console.log('findStaffIds:',optionsSelectStaff)
  for (const key in groupStaff) {
    const group = groupStaff[key];
    console.log('findStaffIds=group:',group)
    if (optionsSelectStaff.includes(group.staff)) {
      staffIds.push(group.id);
      console.log('findStaffIds=AAAAAAAAAAAAA')
    } else {
      staffIds.push('n');
      console.log('findStaffIds=bbbbbbbbbbbbb')
    }
  }
  return staffIds;
}

async function updateData() {
    console.log("Updating staff data:", editProject);
    const updatedFields = {}
    for (const key in editProject) {

        if (editProject[key] !== originalProject[key]) {
            updatedFields[key] = editProject[key];
        }        
    }

    try {
        const { data, pending, refresh, error } = await useFetch(`/api/groupname/${editProject.id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedFields),
        });
        
        if (data.value) {
            console.log("Updated successfully:", data.value);
            getProject(); // Refresh the staff list after the update is successful
            activeDrawerProjectEdit.value = false;
        } else {
            console.log('error',error)
            console.log('errorName',error.value.data)
            errors.value.push(error.value.data)
        }
    } catch (error) {
        console.error('Error updating data:', error);
    }
}

async function updateDataGroup(res) {
    try {
        const { data, pending, refresh, error } = await useFetch(`/api/group/${res.id}/`, {
            method: 'PATCH',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
                'Content-Type': 'application/json',
            },
            body: {
                priority: res.priority,
                turn: res.turn,},
        });
        
        if (data.value) {
            console.log("Updated successfully:", data.value);
            getProject(); // Refresh the staff list after the update is successful
            getGroup(res.groupname); // Refresh the staff list after the update is successful
        } else {
            console.log('error',error)
            console.log('errorName',error.value.data)
            errors.value.push(error.value.data)
        }
    } catch (error) {
        console.error('Error updating data:', error);
    }
}

async function AddGroupmenber(groupname) {
    console.log("Updating AddGroupmenber");
    errors.value = []
    for (const member of newAddMembers.value) {
        try {
            console.log('addData')
            console.log('NEWmember to group',member)
            const { data, pending, refresh, error } = await useFetch('/api/group/', {
                method: 'POST',
                baseURL:'http://localhost:8000',
                headers: {
                Authorization: `JWT ${useStore.token}`,
                },
                body: {
                    groupname: groupname,
                    staff: member,
                }
            })

            if (data.value) {
                console.log("New staff added:", data.value)
                getProject()
                getGroup(editProject.id)
                getUser()
            } else {
                console.log('error',error)
                console.log('errorName',error.value.data)
                errors.value.push(error.value.data)
            }

        } catch (error) {
            console.error('Error deleting data:', error);
        }        
    }
}

watch(optionsSelectStaff, (newVal, oldVal) => {
  newAddMembers.value = newVal.filter(member => !oldGroupMembers.value.includes(member))
  console.log("New Members: ", newAddMembers);  
});

onMounted(() => {
    getProject()
    getUser()
})

</script>

<template>
    <n-button dashed type="warning" strong
    @click=switchactiveDrawerProjectAdd
    >
        新增組別
    </n-button>
    <table class="table-auto min-w-full">
        <thead class="bg-gray-50">
            <tr>
                <th v-for="col in columns" class="px-2 py-4 text-xs font-bold text-gray-500 text-left" scope="col">{{ col.title }}</th>
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
                    v-if="!res[col.key] && col.key === 'EditGroup'"
                    secondary
                    type='info'
                    @click= editDataGroup(res)
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

                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key!=='groups'">
                        {{ res[col.key] }}
                    </div>
                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key==='groups'">
                        <tr v-for="member in formatGroups(res[col.key])">
                            <td>{{ member }}</td>
                        </tr>
                    </div>                         
                </td>
            </tr>
        </tbody>
    </table>
    <n-drawer v-model:show="activeDrawerProjectEdit" :width="502" :placement="placementDrawer">
        <n-drawer-content title="專案名稱" closable>
            <n-form>
                <n-form-item-row label="組別代碼">
                    <n-input placeholder="A/B/C/..." v-model:value="editProject.name" />
                </n-form-item-row>
                <n-form-item-row label="優先編碼">
                    <n-input placeholder="0,1,2,..." v-model:value="editProject.priority" />
                </n-form-item-row>
                <n-form-item-row label="順序編碼">
                    <n-input placeholder="0,1,2,..." v-model:value="editProject.turn" />
                </n-form-item-row>

                <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 rounded-xl">
                    <p v-for="error in errors" :key="error">
                        {{ error }}
                    </p>
                </div>
                <n-button type="primary" block secondary strong @click="updateData(editProject)">
                    更正
                </n-button>
            </n-form>
        </n-drawer-content>
    </n-drawer>
    <n-drawer v-model:show="activeDrawerGroupEdit" :width="502" :placement="placementDrawer">
        <n-drawer-content title="專案名稱" closable>
            <n-form>
                <n-switch v-model:value="specialGroup">
                    <template #checked> 
                    特殊編組
                    </template>
                    <template #unchecked>
                    一般編組
                    </template>
                </n-switch>
                <n-form-item-row label="組員">
                    <n-transfer ref="transfer" v-if="!specialGroup"
                    :options="optionsStaff" v-model:value="optionsSelectStaff"
                    source-filterable
                    />
                    <n-transfer ref="transfer" v-if="specialGroup"
                    :options="optionsStaffSpecial" v-model:value="optionsSelectStaff"
                    source-filterable
                    />
                </n-form-item-row>
                <n-button type="primary" block secondary strong @click="AddGroupmenber(editProject.id)">
                    新增組員
                </n-button>

                <table class="table-auto min-w-full">
                    <thead class="bg-gray-50">
                        <tr>
                            <th v-for="col in columnsGroup" class="px-2 py-4 text-xs font-bold text-gray-500 text-left" scope="col">{{ col.title }}</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr v-for="(res, rowIndex) in groupStaff">
                            <td v-for="col in columnsGroup" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                                <n-button 
                                v-if="!res[col.key] && col.key === 'Edit'"
                                secondary
                                type='info'
                                @click= updateDataGroup(res)
                                >
                                    {{ col.title }}
                                </n-button>

                                <n-button 
                                v-if="!res[col.key]  && col.title === 'Delete'"
                                secondary strong type='error'
                                @click=deleteDataGroup(res,editProject.id)
                                :disabled="!editingGroup[rowIndex]"
                                >
                                    {{ col.key }}
                                </n-button>

                                <n-switch v-if="col.title==='Delete'" v-model:value="editingGroup[rowIndex]" />

                                <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key!=='staff_name'">
                                    <n-input placeholder="0,1,2,3..." v-model:value="res[col.key]" />
                                </div>
                                <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key==='staff_name'">
                                    {{ res[col.key] }}
                                </div>                 
                            </td>
                        </tr>
                    </tbody>
                </table>
            </n-form>
        </n-drawer-content>
    </n-drawer>
    <n-drawer v-model:show="activeDrawerProjectAdd" :width="502" :placement="placementDrawer">
        <n-drawer-content title="新增組別" closable>
            <n-form>
                <n-form-item-row label="組別代碼">
                    <n-input placeholder="A/B/C/..." v-model:value="newProject.name" />
                </n-form-item-row>
                <n-form-item-row label="優先編碼">
                    <n-input placeholder="0,1,2,..." v-model:value="newProject.priority" />
                </n-form-item-row>
                <n-form-item-row label="順序編碼">
                    <n-input placeholder="0,1,2,..." v-model:value="newProject.turn" />
                </n-form-item-row>
                <n-form-item-row label="組員">

                </n-form-item-row>
                <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 rounded-xl">
                    <p v-for="error in errors" :key="error">
                        {{ error }}
                    </p>
                </div>
                <n-button type="primary" block secondary strong @click="addData">
                新增
                </n-button>
            </n-form>
        </n-drawer-content>
    </n-drawer>
</template>
