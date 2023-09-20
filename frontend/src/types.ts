export type Run={id:string;config:{model:string};status:string;completed:number;expected_count:number};
export type Score={count:number;baseline:number;candidate:number;delta:number;interval?:{low:number;high:number}};
export type CaseResult={score:number;output:string;task:string;slices:string[];prompt?:string;reason?:string};
export type Pair={case_id:string;delta:number;baseline:CaseResult;candidate:CaseResult};
export type Report={overall:Score;tasks:Record<string,Score>;slices:Record<string,Score>;cases:Pair[];gate:{passed:boolean;failures:{scope?:string;slice?:string;reason:string;observed?:number;threshold?:number}[]};operations:{candidate:{p95_ms:number;total_tokens:number;usage_kinds:string[]}}};
export type BlindPair={case_id:string;A:string;B:string;prompt:string;revision:number;reviewed:boolean};
