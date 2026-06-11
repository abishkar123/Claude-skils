import { parseSections } from "./api.js";

const TONE = {
  OBJECTIVE: "tone-accent",
  "CAPACITY CHECK": "tone-capacity",
  "RISKS & OVERLOAD": "tone-risk",
  "SUCCESS CRITERIA": "tone-success",
  STATE: "tone-state",
  "CONNECTOR USAGE NOTE": "tone-connector",
};

export function PlanCards({ text }) {
  const cards = parseSections(text);
  return (
    <div className="plan">
      {cards.map((card, i) => (
        <section key={i} className={`card ${TONE[card.title] || ""}`}>
          <h3>{card.title}</h3>
          <pre>{card.body}</pre>
        </section>
      ))}
    </div>
  );
}

export function Message({ msg }) {
  if (msg.role === "user") {
    return <div className="msg msg-user">{msg.text}</div>;
  }
  if (msg.error) {
    return <div className="msg msg-error">⚠ {msg.text}</div>;
  }
  return (
    <div className="msg msg-agent">
      {msg.intent && <span className="intent-chip">{msg.intent}</span>}
      <PlanCards text={msg.text} />
    </div>
  );
}

export function ConnectorPanel({ connectors, onToggle }) {
  return (
    <div className="connectors">
      <h2>Connectors</h2>
      <p className="hint">
        Least-privilege, session-only grants. Nothing is read until a real MCP
        connector is wired in <em>and</em> you authorize it here.
      </p>
      {connectors.map((c) => (
        <label key={c.name} className={`connector ${c.available ? "" : "unavailable"}`}>
          <input
            type="checkbox"
            checked={c.authorized}
            onChange={(e) => onToggle(c.name, e.target.checked)}
          />
          <span className="connector-name">{c.name}</span>
          <span className={`risk risk-${c.risk}`}>{c.risk}</span>
          <span className="connector-meta">
            {c.available ? c.scope : "not detected — manual fallback active"}
          </span>
        </label>
      ))}
    </div>
  );
}

export const EXAMPLES = [
  "Plan my week: ~30 focused hours. Ship the auth feature, prep Thursday's design review, 3 gym sessions. Last week I overcommitted.",
  "Plan my weekend — low energy, errands piled up, want one learning block.",
  "Plan tomorrow: 4 meetings 10–12 and 2–3, peak focus in the morning.",
  "Build a 90-day plan to get good at system design. 5h/week, mid-level backend dev.",
  "Turn this into promotion evidence: shipped retry layer, checkout errors 2.1%→0.3%.",
  "Run my monthly review: shipped payments work, missed the blog post, gym streak broke week 3.",
  "Which connectors would help my productivity system?",
];
