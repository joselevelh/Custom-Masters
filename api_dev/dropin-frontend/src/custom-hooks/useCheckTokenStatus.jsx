import { useEffect } from 'react';
import CheckTokenStatus from '../helpers/CheckTokenStatus'
export default function useCheckTokenStatus() {
  useEffect(() => {
    CheckTokenStatus()
  }, []);
}


