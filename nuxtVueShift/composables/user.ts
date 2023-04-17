export const useUserStore = definePiniaStore('useUserStore', {
    const user = reactive({
        isAuthenticated: false,
        email: null,
        token: null
    })

    const initStore = () => {
        user.isAuthenticated = false
        if (localStorage.getItem('user.token')) {
            user.isAuthenticated = true
            user.email = localStorage.getItem('user.email')
            user.token = localStorage.getItem('user.token')

            console.log('Initialized user:', user)
        }
    }

    const setToken = (token: string, email: string) => {
        console.log('Setting token:', token, email)
        user.isAuthenticated = true
        user.email = email
        user.token = token
        localStorage.setItem('user.token', token)
        localStorage.setItem('user.email', email)
    }   

    const removeToken = () => {
        console.log('Removing token')
        user.isAuthenticated = false
        user.email = null
        user.token = null
        localStorage.removeItem('user.token')
        localStorage.removeItem('user.email')
    }

    return {
        user,
        initStore,
        setToken,
        removeToken
    }
})
    
//     {
//     id: 'user',
//     state: () => ({
//         user:{
//             isAuthenticated: false,
//             email: null,
//             token: null
//         }
//     }),
//     getters: {
//         isAuthenticated: (state) => state.isAuthenticated,
//         name: (state) => state.name,
//         email: (state) => state.email,
//         token: (state) => state.token
//     },
//     actions: {
//         initStore() {
//             this.user.isAuthenticated false
//             if (localStorage.gerItem('user.token')) {
//                 this.user.isAuthenticated = true
//                 this.user.email = localStorage.getItem('user.email')
//                 this.user.token = localStorage.getItem('user.token')

//                 console.log('Initialized user:', this.user)
//             }
//         },
//         setToken(token, email) {
//             console.log('Setting token:', token, email)
//             this.user.isAuthenticated = true
//             this.user.email = email
//             this.user.token = token
//             localStorage.setItem('user.token', token)
//             localStorage.setItem('user.email', email)
//         },
//         removeToken() {
//             console.log('Removing token')
//             this.user.isAuthenticated = false
//             this.user.email = null
//             this.user.token = null
//             localStorage.removeItem('user.token')
//             localStorage.removeItem('user.email')
//         }
//     }
// })

