import React,{useState} from 'react';
import type {Report} from './types';
const percent=(n:number)=>(n*100).toFixed(1)+'%';
const delta=(n:number)=>(n>=0?'+':'')+(n*100).toFixed(1)+' pp';
export function Comparison({data}:{data:Report}){
 const [slice,setSlice]=useState('all');
 const [regressions,setRegressions]=useState(false);
 const cases=data.cases.filter(p=>(slice==='all'||p.baseline.slices?.includes(slice))&&(!regressions||p.delta<0));
 return <>
  <section className={'decision '+(data.gate.passed?'pass':'blocked')} aria-label="Release decision">
   <div><span className="eyebrow">RELEASE DECISION</span><h2>{data.gate.passed?'Ready for review':'Release blocked'}</h2><p>{data.gate.passed?'Every configured quality and operating gate passed.':'Review the failing requirements before promoting this candidate.'}</p></div>
   <span className="decision-mark" aria-hidden="true">{data.gate.passed?'✓':'!'}</span>
  </section>
  <div className="metric-grid">
   <article><span className="eyebrow">CANDIDATE QUALITY</span><strong>{percent(data.overall.candidate)}</strong><p>Baseline {percent(data.overall.baseline)}</p></article>
   <article><span className="eyebrow">PAIRED CHANGE</span><strong>{delta(data.overall.delta)}</strong><p>95% bootstrap: {delta(data.overall.interval?.low??0)} to {delta(data.overall.interval?.high??0)}</p></article>
   <article><span className="eyebrow">P95 LATENCY</span><strong>{data.operations.candidate.p95_ms.toFixed(0)} <small>ms</small></strong><p>{data.operations.candidate.total_tokens.toLocaleString()} usage units · {data.operations.candidate.usage_kinds.join(', ')}</p></article>
  </div>
  {data.gate.failures.length>0&&<section className="panel findings"><h3>Requirements to resolve</h3><ul>{data.gate.failures.map((f,i)=><li key={i}><span className="dot"/>{f.slice?<button className="text-button" onClick={()=>setSlice(f.slice!)}>{f.slice}</button>:<b>{f.scope||'overall'}</b>}<span>{f.reason}</span>{f.observed!==undefined&&<small>{f.observed.toFixed(3)} / threshold {f.threshold?.toFixed(3)}</small>}</li>)}</ul></section>}
  <section className="panel"><div className="section-title"><h3>Quality by task</h3><span>Higher is better · paired cases</span></div><div className="table-scroll"><table><thead><tr><th>Task</th><th>Cases</th><th>Baseline</th><th>Candidate</th><th>Change</th></tr></thead><tbody>{Object.entries(data.tasks).map(([task,s])=><tr key={task}><th scope="row">{task}</th><td>{s.count}</td><td>{percent(s.baseline)}</td><td>{percent(s.candidate)}</td><td className={s.delta<0?'negative':'positive'}>{delta(s.delta)}</td></tr>)}</tbody></table></div></section>
  <section className="examples" aria-label="Concrete examples"><div className="section-title"><h3>Evidence, case by case</h3><span>{cases.length} examples</span></div><div className="filters"><label>Slice <select value={slice} onChange={e=>setSlice(e.target.value)}><option value="all">All slices</option>{Object.keys(data.slices).map(s=><option key={s}>{s}</option>)}</select></label><label className="checkbox"><input type="checkbox" checked={regressions} onChange={e=>setRegressions(e.target.checked)}/> Regressions only</label></div>
  {cases.length===0?<p className="empty">No examples match these filters.</p>:cases.map(p=><article className="case panel" key={p.case_id}><div className="section-title"><h4>{p.case_id}</h4><span className={p.delta<0?'negative':'positive'}>{delta(p.delta)}</span></div><p className="case-prompt">{p.baseline.prompt}</p><div className="output-grid"><div><span className="eyebrow">BASELINE · {percent(p.baseline.score)}</span><pre>{p.baseline.output||'(empty response)'}</pre></div><div><span className="eyebrow">CANDIDATE · {percent(p.candidate.score)}</span><pre>{p.candidate.output||'(empty response)'}</pre></div></div></article>)}</section>
 </>;
}
