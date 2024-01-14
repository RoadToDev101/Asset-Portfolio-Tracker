import { Outlet } from "react-router-dom";
import DashboardNav from "./DashboardNav";

const Dashboard = () => {
  return (
    <>
      <div className="flex w-full min-h-screen">
        <DashboardNav />
        <Outlet />
      </div>
    </>
  );
};

export default Dashboard;
