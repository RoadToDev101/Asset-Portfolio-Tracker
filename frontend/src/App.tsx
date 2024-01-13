import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "@pages/home";
import NotFound from "@pages/NotFound";
import Dashboard from "@pages/dashboard";
import Login from "@pages/authentication/Login";
import Register from "@pages/authentication/Register";
import AuthProvider from "@/context/AuthProvider";
import ProtectedRoute from "@components/ProtectedRoute";
import Portfolio from "@pages/dashboard/Portfolio";
import Overview from "@pages/dashboard/Overview";
import UserAccount from "@pages/dashboard/UserAccount";
import PortfolioDetail from "@pages/dashboard/PortfolioDetail";

// TODO: Apply when implement SuperTokens for authentication
// import SuperTokens, { SuperTokensWrapper } from "supertokens-auth-react";
// import ThirdPartyEmailPassword, {
//   Github,
//   Google,
// } from "supertokens-auth-react/recipe/thirdpartyemailpassword";
// import Session, { SessionAuth } from "supertokens-auth-react/recipe/session";
// import { getSuperTokensRoutesForReactRouterDom } from "supertokens-auth-react/ui";
// import { ThirdPartyEmailPasswordPreBuiltUI } from "supertokens-auth-react/recipe/thirdpartyemailpassword/prebuiltui";
// import * as reactRouterDom from "react-router-dom";

// SuperTokens.init({
//   appInfo: {
//     // learn more about this on https://supertokens.com/docs/thirdpartyemailpassword/appinfo
//     appName: "my-app",
//     apiDomain: "http://localhost:3001",
//     websiteDomain: "http://localhost:3000",
//     apiBasePath: "/auth",
//     websiteBasePath: "/auth",
//   },
//   recipeList: [
//     ThirdPartyEmailPassword.init({
//       signInAndUpFeature: {
//         providers: [Github.init(), Google.init()],
//       },
//     }),
//     Session.init(),
//   ],
// });

// class App extends React.Component {
//   render() {
//     return (
//       <SuperTokensWrapper>
//         <BrowserRouter>
//           <Routes>
//             {getSuperTokensRoutesForReactRouterDom(reactRouterDom, [
//               ThirdPartyEmailPasswordPreBuiltUI,
//             ])}
//             <Route path="/" element={<Home />} />
//             <Route path="*" element={<NotFound />} />
//             <Route
//               path="/dashboard"
//               element={
//                 <SessionAuth>
//                   <Dashboard />
//                 </SessionAuth>
//               }
//             />
//           </Routes>
//         </BrowserRouter>
//       </SuperTokensWrapper>
//     );
//   }
// }

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="flex flex-col min-h-screen">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route
              path="/dashboard/*"
              element={<ProtectedRoute component={Dashboard} />}
            >
              <Route index element={<Overview />} />
              <Route path="portfolio" element={<Portfolio />} />
              <Route path="portfolio/:id" element={<PortfolioDetail />} />
              <Route path="user" element={<UserAccount />} />
              <Route path="*" element={<NotFound />} />
            </Route>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
