import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom';
import CheckTokenStatus from '../helpers/CheckTokenStatus'
export default function useAuthOrRedirect(url="/login") {
  console.log("Checking auth status...")
  const navigate = useNavigate();
  useEffect(() => {
    if (CheckTokenStatus() === false){
      // TODO: Update store since user is not logged in
       navigate(url)
    }
  }, [navigate, url]);
}


