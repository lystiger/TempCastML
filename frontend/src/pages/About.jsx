const FEATURES = [
  {
    title: "Data ingestion",
    desc: "A Python collector reads an ESP32-S3 / DHT sensor over serial and logs clean, timestamped readings.",
  },
  {
    title: "API",
    desc: "A FastAPI service exposes the latest reading, historical data, and ML-powered forecasts over REST.",
  },
  {
    title: "Frontend",
    desc: "This React + Vite dashboard visualizes live telemetry, trends, and predictions with clear data-quality signals.",
  },
  {
    title: "Machine learning",
    desc: "An LSTM trained on historical time series predicts near-term indoor temperature trends.",
  },
  {
    title: "Embedded inference",
    desc: "The trained model is compressed for TinyML deployment back onto the ESP32-S3 for on-device prediction.",
  },
];

const STACK = ["ESP32-S3", "Arduino / C++", "FastAPI", "SQLite", "React", "Vite", "LSTM", "TinyML"];

const TEAM = [
  {
    initials: "HL",
    name: "Hung Lee",
    role: "Lead · Embedded & low-level engineering",
    desc: "Circuit design, sensor firmware, and on-device TinyML deployment.",
  },
  {
    initials: "HA",
    name: "Hung Anh",
    role: "Frontend engineering",
    desc: "Dashboard design, data visualization, and the web experience.",
  },
];

export default function About() {
  return (
    <>
      <div className="page-head">
        <div>
          <span className="eyebrow">
            <b>03</b> / About
          </span>
          <h1 className="page-title">About TempCastML</h1>
          <p className="page-sub">
            A TinyML-powered system that forecasts indoor temperature trends from
            real-time sensor data — from the ESP32-S3 all the way to on-device inference.
          </p>
        </div>
      </div>

      <div className="grid dash-grid">
        <section className="panel panel--pad col-6 rise rise-1">
          <span className="eyebrow">How it works</span>
          <div style={{ marginTop: 12 }}>
            {FEATURES.map((f, i) => (
              <div className="feature" key={f.title}>
                <span className="feature__idx">{String(i + 1).padStart(2, "0")}</span>
                <div>
                  <div className="feature__b">{f.title}</div>
                  <div className="feature__d">{f.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        <div className="col-6" style={{ display: "grid", gap: 18, alignContent: "start" }}>
          <section className="panel panel--pad rise rise-2">
            <span className="eyebrow">Pipeline</span>
            <p className="footer__chain" style={{ marginTop: 12, fontSize: 13, lineHeight: 2 }}>
              <b>sensor</b> → <b>serial / ingestion</b> → <b>database / API</b> →{" "}
              <b>dashboard</b> → <b>ML model</b> → <b>ESP32 deployment</b>
            </p>
            <span className="eyebrow" style={{ marginTop: 20, display: "inline-flex" }}>
              Stack
            </span>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 12 }}>
              {STACK.map((s) => (
                <span key={s} className="pill mono" style={{ fontSize: 12 }}>
                  {s}
                </span>
              ))}
            </div>
          </section>

          <section className="panel panel--pad rise rise-3">
            <span className="eyebrow">Team</span>
            <div style={{ display: "grid", gap: 18, marginTop: 14 }}>
              {TEAM.map((p) => (
                <div className="person" key={p.name}>
                  <span className="person__avatar">{p.initials}</span>
                  <div>
                    <div className="feature__b">{p.name}</div>
                    <div className="mono" style={{ fontSize: 11.5, color: "var(--accent)", letterSpacing: "0.04em" }}>
                      {p.role}
                    </div>
                    <div className="feature__d" style={{ marginTop: 4 }}>
                      {p.desc}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </>
  );
}
