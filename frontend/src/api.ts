export async function request<T>(path:string,options:RequestInit={}):Promise<T>{
 const response=await fetch(path,options);const body=await response.json();
 if(!response.ok)throw new Error(body.error||'The request could not be completed');
 return body;
}
