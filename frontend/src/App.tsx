import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "@components/Home";
import NotFound from "@components/NotFound";
import Dashboard from "@components/Dashboard";
import Login from "@components/Authentication/Login";
import Register from "@components/Authentication/Register";
import AuthProvider from "@/context/AuthProvider";
import ProtectedRoute from "@components/ProtectedRoute";

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
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/dashboard"
            element={<ProtectedRoute component={Dashboard} />}
          />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
