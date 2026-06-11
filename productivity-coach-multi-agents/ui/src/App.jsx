import { useEffect, useRef, useState } from "react";
import { api } from "./api.js";
import { ConnectorPanel, EXAMPLES, Message } from "./components.jsx";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [deepQa, setDeepQa] = useState(true);
  const [connectors, setConnectors] = useState([]);
  const [status, setStatus] = useState(null);
  const endRef = useRef(null);

  useEffect(() => {
    api.status().then(setStatus).catch(() => setStatus(null));
    refreshConnectors();
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy]);

  function refreshConnectors() {
    api.connectors().then(setConnectors).catch(() => setConnectors([]));
  }

  async function toggleConnector(name, authorized) {
    await api.setAuthorized(name, authorized).catch(() => {});
    refreshConnectors();
  }

  async function send(text) {
    const request = (text ?? input).trim();
    if (!request || busy) return;
    setInput("");
    setBusy(true);
    setMessages((m) => [...m, { role: "user", text: request }]);
    try {
      const res = await api.ask(request, deepQa);
      setMessages((m) => [
        ...m,
        { role: "agent", intent: res.intent, text: res.output },
      ]);
    } catch (e) {
      setMessages((m) => [...m, { role: "agent", error: true, text: e.message }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="layout">
      <aside className="sidebar">
        <header>
          <h1>
            productivity-coach
            <span> Multi Agents</span>
          </h1>
          {status && (
            <div className="status">
              <span className="dot ok" /> {status.model}
              <span className={`dot ${status.api_key_present ? "ok" : "bad"}`} />
              API key {status.api_key_present ? "set" : "missing"}
              <span className={`dot ${status.storage_connected ? "ok" : "off"}`} />
              storage {status.storage_connected ? "MongoDB" : "paste-back"}
            </div>
          )}
        </header>

        <ConnectorPanel connectors={connectors} onToggle={toggleConnector} />

        <div className="options">
          <label>
            <input
              type="checkbox"
              checked={deepQa}
              onChange={(e) => setDeepQa(e.target.checked)}
            />
            Deep QA review (extra model pass)
          </label>
        </div>

        <div className="examples">
          <h2>Try one</h2>
          {EXAMPLES.map((ex) => (
            <button key={ex} onClick={() => send(ex)} disabled={busy}>
              {ex}
            </button>
          ))}
        </div>
      </aside>

      <main className="chat">
        <div className="messages">
          {messages.length === 0 && (
            <div className="empty">
              Ask for a weekly plan, a weekend plan, today's execution plan, a
              30/60/90 skill roadmap, promotion evidence, or a review.
              <br />
              Manual mode by default — nothing is read or stored without your
              say-so.
            </div>
          )}
          {messages.map((msg, i) => (
            <Message key={i} msg={msg} />
          ))}
          {busy && <div className="msg msg-agent thinking">agents working…</div>}
          <div ref={endRef} />
        </div>

        <form
          className="composer"
          onSubmit={(e) => {
            e.preventDefault();
            send();
          }}
        >
          <textarea
            value={input}
            placeholder="Plan my week: 30 focused hours, ship auth, 3 gym sessions…"
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
            rows={2}
          />
          <button type="submit" disabled={busy || !input.trim()}>
            {busy ? "…" : "Send"}
          </button>
        </form>
      </main>
    </div>
  );
}
