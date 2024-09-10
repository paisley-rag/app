import { Router, Route, Switch } from "wouter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Navigation } from "./components/Navigation.tsx";
import { PageLogin } from "./components/pages/PageLogin.tsx";
import { PageKnowledgeBases } from "./components/pages/PageKnowledgeBases.tsx";
import { PageKnowledgeBase } from "./components/pages/PageKnowledgeBase.tsx";
import { PageChatbots } from "./components/pages/PageChatbots.tsx";
import { PageChatbot } from "./components/pages/PageChatbot.tsx";
import { PageCreateChatbot } from "./components/pages/PageCreateChatbot.tsx";
import { PageHistory } from "./components/pages/PageHistory.tsx";
import { PageLineChart } from "./components/pages/PageLineChart.tsx";
import { ProtectedRoute } from "./components/ProtectedRoute.tsx";
import { useAuth } from './auth';
// import { DataTableDemo } from "./components/pages/DataTableDemo.tsx"; // testing only

const queryClient = new QueryClient();

interface Route {
  path: string;
  component: React.ComponentType;
};

const routes: Route[] = [
  { path: "/knowledge-bases", component: PageKnowledgeBases },
  { path: "/knowledge-bases/:id", component: PageKnowledgeBase },
  { path: "/chatbots", component: PageChatbots },
  { path: "/chatbots/create", component: PageCreateChatbot },
  { path: "/chatbots/:id", component: PageChatbot },
  { path: "/history", component: PageHistory },
  { path: "/metrics", component: PageLineChart }
];

function App() {
  const { token } = useAuth();
  return (
    <QueryClientProvider client={queryClient}>
      <Route path="/login" component={PageLogin} />
      <Navigation />
      <main className="ml-60 p-6">
        <Router>
          <Switch>
            <ProtectedRoute>
            {routes.map((route) => (
              <Route
                key={route.path}
                path={route.path}
                component={() => (
                    <route.component />
                  )}
                  />
                ))}
            </ProtectedRoute>
            <Route>{ token ? null : <PageLogin/> }</Route>
          </Switch>
        </Router>
      </main>
    </QueryClientProvider>
  );
}

export default App;
