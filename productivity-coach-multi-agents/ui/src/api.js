async function json(res) {
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `${res.status} ${res.statusText}`);
  }
  return res.json();
}

export const api = {
  status: () => fetch("/api/status").then(json),
  connectors: () => fetch("/api/connectors").then(json),
  setAuthorized: (connector, authorized) =>
    fetch("/api/connectors/authorize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ connector, authorized }),
    }).then(json),
  ask: (request, deepQa) =>
    fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ request, deep_qa: deepQa }),
    }).then(json),
};

// Section headers of the universal output frame, used to render plan cards.
export const SECTIONS = [
  "OBJECTIVE",
  "INPUTS USED",
  "ASSUMPTIONS",
  "PRIORITIZED ACTIONS",
  "CAPACITY CHECK",
  "RISKS & OVERLOAD",
  "TRADEOFFS",
  "SUCCESS CRITERIA",
  "REVIEW CHECKPOINT",
  "MANUAL FALLBACK",
  "STATE",
];

// Split an agent answer into [{title, body}] cards; unmatched text becomes a
// leading "RESPONSE" card so nothing is ever dropped.
export function parseSections(text) {
  const note = text.split("--- Connector Usage Note ---");
  const main = note[0];
  const lines = main.split("\n");
  const cards = [];
  let current = { title: "RESPONSE", body: [] };
  for (const line of lines) {
    const header = SECTIONS.find((s) =>
      line.trimStart().toUpperCase().startsWith(s)
    );
    if (header) {
      if (current.body.join("").trim()) cards.push(current);
      const rest = line.trimStart().slice(header.length).replace(/^[:\s-]+/, "");
      current = { title: header, body: rest ? [rest] : [] };
    } else {
      current.body.push(line);
    }
  }
  if (current.body.join("").trim()) cards.push(current);
  if (note[1]) cards.push({ title: "CONNECTOR USAGE NOTE", body: note[1].split("\n") });
  return cards.map((c) => ({ title: c.title, body: c.body.join("\n").trim() }));
}
