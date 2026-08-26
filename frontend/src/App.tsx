import { TopNavbar } from "./components/layout/TopNavbar";
import { Sidebar } from "./components/layout/Sidebar";
import { KibanaIframe } from "./components/layout/KibanaIframe";

function App() {
  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      <TopNavbar />
      <Sidebar />
      <KibanaIframe />
    </div>
  );
}

export default App;
