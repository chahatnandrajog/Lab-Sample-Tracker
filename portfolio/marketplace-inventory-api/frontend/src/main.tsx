import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";
type Product = {sku:string;name:string;available:number};
const API=import.meta.env.VITE_API_URL||"http://localhost:8000";
function App(){
  const [products,setProducts]=useState<Product[]>([]);
  const [sku,setSku]=useState("");
  const [qty,setQty]=useState(1);
  const [message,setMessage]=useState("");
  async function refresh(){
    try {
      const response=await fetch(API+"/products");
      if(!response.ok) throw Error("Unable to load products");
      setProducts(await response.json());
    }catch(error){setMessage(String(error));}
  }
  useEffect(()=>{void refresh();},[]);
  async function reserve(event:React.FormEvent<HTMLFormElement>){
    event.preventDefault();
    const response=await fetch(API+"/reservations",{
      method:"POST",
      headers:{"Content-Type":"application/json","Idempotency-Key":crypto.randomUUID()},
      body:JSON.stringify({sku,quantity:qty})
    });
    const body=await response.json();
    setMessage(response.ok?"Reserved "+qty+" of "+sku:(body.detail||"Request failed"));
    if(response.ok) await refresh();
  }
  return <main>
    <h1>Inventory Console</h1><p>Transactional stock reservation system</p>
    <section><h2>Available inventory</h2><table><thead><tr><th>SKU</th><th>Item</th><th>Available</th></tr></thead>
    <tbody>{products.map(p=><tr key={p.sku}><td>{p.sku}</td><td>{p.name}</td><td>{p.available}</td></tr>)}</tbody></table></section>
    <section><h2>Reserve product</h2><form onSubmit={reserve}>
    <label>Product <select required value={sku} onChange={e=>setSku(e.target.value)}>
    <option value="">Choose SKU</option>{products.map(p=><option value={p.sku} key={p.sku}>{p.name}</option>)}</select></label>
    <label>Quantity <input type="number" min="1" value={qty} onChange={e=>setQty(Number(e.target.value))}/></label>
    <button type="submit">Reserve</button></form><p role="status">{message}</p></section>
  </main>;
}
createRoot(document.getElementById("root")!).render(<React.StrictMode><App/></React.StrictMode>);
