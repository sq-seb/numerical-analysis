import { useQuery } from "@tanstack/react-query"

export default function App() {
  // idk, logic
  const {data, isLoading} = useQuery({
    queryKey: ["fetch1"],
    queryFn: async () => {
      const res = await fetch('http://localhost:5000');
      return res.json();
    }
  })

  // Return App component
  return (
    <>
      <h1>{!isLoading ? data.message : "Loading..."}</h1>
    </>
  )
}