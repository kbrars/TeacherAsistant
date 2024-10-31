    import { useQuasar } from "quasar"
    export default function useNotify(){
      const $q=useQuasar()
      const notifyError =(message)=>{
        $q.notify({
          type: 'negative',
          message: message || "Giris Yapılamadi"
        })
      }
      return{
        notifyError
      }
    }

