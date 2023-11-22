import React, { useState } from "react";
import type { BlindPair } from "./types";
export function Review({
  pair,
  onSave,
}: {
  pair: BlindPair;
  onSave: (
    choice: string,
    note: string,
    revision: number
  ) => Promise<{ revision: number }>;
}) {
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");
  const [revision, setRevision] = useState(pair.revision);
  async function choose(choice: string) {
    setBusy(true);
    setError("");
    try {
      const result = await onSave(choice, note, revision);
      setRevision(result.revision);
      setSaved(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not save review");
    } finally {
      setBusy(false);
    }
  }
  return (
    <article className="panel review-card">
      <div className="section-title">
        <h3>{pair.case_id}</h3>
        <span>{pair.reviewed ? "Previously reviewed" : "Awaiting review"}</span>
      </div>
      <p className="case-prompt">{pair.prompt}</p>
      <div className="output-grid">
        <div>
          <span className="eyebrow">RESPONSE A</span>
          <pre>{pair.A || "(empty response)"}</pre>
        </div>
        <div>
          <span className="eyebrow">RESPONSE B</span>
          <pre>{pair.B || "(empty response)"}</pre>
        </div>
      </div>
      <label className="note">
        Reason for your preference{" "}
        <textarea
          value={note}
          maxLength={4000}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Correctness, completeness, clarity…"
        />
      </label>
      <div className="vote-buttons">
        <button disabled={busy} onClick={() => choose("A")}>
          Prefer A
        </button>
        <button disabled={busy} onClick={() => choose("B")}>
          Prefer B
        </button>
        <button
          disabled={busy}
          className="secondary"
          onClick={() => choose("tie")}
        >
          Tie
        </button>
        <button
          disabled={busy}
          className="secondary"
          onClick={() => choose("skip")}
        >
          Skip
        </button>
      </div>
      {saved && (
        <p role="status" className="positive">
          Review saved
        </p>
      )}
      {error && (
        <p role="alert" className="negative">
          {error}
        </p>
      )}
    </article>
  );
}
