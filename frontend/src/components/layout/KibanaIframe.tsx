export function KibanaIframe() {
  return (
    <div className="flex-1 w-full h-full bg-background pt-14">
      <iframe
        src="https://127.0.0.1:64297/"
        className="w-full h-full border-none"
        title="Kibana Telemetry Dashboard"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
      />
    </div>
  );
}
