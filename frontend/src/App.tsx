import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Home from "./pages/home/Home";
import Blogs from "./pages/home/Blogs";
import Course from "./pages/home/Course";
import TestSeries from "./pages/home/TestSeries";
import StudyMaterial from "./pages/home/StudyMaterial";
import BatchPages from "./pages/Batches/BatchPages";
import BatchDetails from "./pages/Batches/BatchDetails";
import LibraryPage from "./pages/Library/LibraryPage";
import StorePage from "./pages/Store/StorePage";
import TseriesPage from "./pages/TestSeries/TseriesPage";


import Study from "./pages/Dashboard/Study";
import Profile from "./pages/Dashboard/Profile";
import Purchases from "./pages/Dashboard/Purchases";
import ChatsPage from "./pages/Chats/ChatsPages";
import UpcomingPage from "./pages/Study/UpcomingPage";
import ProtectedRoute from "./components/ProtectedRoute";
import LiveClassesPage from "./pages/Study/LiveClassesPage";

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          <Route path="/blogs" element={<Blogs />} />
          <Route path="/course" element={<Course />} />
          <Route path="/test-series-free" element={<TestSeries />} />
          <Route path="/weekly-schedule" element={<UpcomingPage />} />
          <Route path="/study-material" element={<StudyMaterial />} />

          {/* Auth routes removed as requested */}

          {/* Main Pages Routes (Protected) */}
          <Route element={<ProtectedRoute />}>
            <Route path="/batches" element={<BatchPages />} />
            <Route path="/batches/:id" element={<BatchDetails />} />
            <Route path="/library" element={<LibraryPage />} />
            <Route path="/store" element={<StorePage />} />
            <Route path="/test-series" element={<TseriesPage />} />
            <Route path="/chats" element={<ChatsPage />} />

            {/* Dashboard Routes (Protected) */}
            <Route path="/study" element={<Study />} />
            <Route path="/live-classes" element={<LiveClassesPage />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/purchases" element={<Purchases />} />
          </Route>

          {/* Redirect from /home to root */}
          <Route path="/home" element={<Navigate to="/" replace />} />

          {/* Catch all route - redirect to root */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
