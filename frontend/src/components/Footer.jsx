export function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__inner">
        <span>© {new Date().getFullYear()} TempCastML — TinyML temperature forecasting</span>
        <span className="footer__chain">
          <b>sensor</b> → <b>ingest</b> → <b>API</b> → <b>dashboard</b> → <b>ESP32</b>
        </span>
      </div>
    </footer>
  );
}
