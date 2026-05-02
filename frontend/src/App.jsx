// Import react router
import {Route, Routes} from "react-router-dom"

// Import Index.jsx (everything will be mounted inside btw)
import Index from "./index/Index" 

export default function App() {
  return <Routes>
    <Route path="/" element={<Index/>} />
  </Routes>
}